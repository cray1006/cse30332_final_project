# Christopher Ray  &  Dinh Do
# Creature Battler - Final Project
# player.py


import sys, pygame, math, time
from pygame.locals import *
from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
import creature


# Player Class
class Player:
	def __init__(self, P):
   		self.cid = P		# Creature ID: Grass / Water / Fire
		self.oid = None 	# Opponent ID: Grass / Water / Fire 
		self.creature = None  	# User Creature class
		self.ecreature = None	# Opponent creature class
		self.id = None		# id is index of server protocol list
		self.state = 'start'
		self.turn = None	# second player to connect gets first turn

	def tick(self):
		return


class commandConnProtocol(Protocol):
	def __init__(self, player):
		self.player = player
		self.state = 'start'

	def connectionMade(self):
		print 'Connection Made!' 
		return

	def dataReceived(self, data):
		if self.state == 'start':
			if data == 'Opponent Connected':
				self.player.state = 'connected'
				self.state = 'connected'
			elif data == '0':
				self.player.id = data
				self.player.turn = 1
			elif data == '1':
				self.player.id = data
				self.player.state = 'connected'
				self.state = 'connected'
				self.player.turn = 0

		elif self.state == 'connected':
			print "Opponent type is " + data
			self.player.oid = str(data)
			if data == 'Water':
				self.player.ecreature = creature.Water(1)
			elif data == 'Grass':
				self.player.ecreature = creature.Grass(1)
			elif data == 'Fire':
				self.player.ecreature = creature.Fire(1)
			self.state = 'battle'
			self.player.state = 'battle'

		elif self.state == 'battle':
			if data == 'switch':
				self.player.turn = 1
			elif data == 'quit':
				self.player.state = 'quit'

	def switchTurn(self):
		self.transport.write('T')
			


class commandConnFactory(ClientFactory):
	def __init__(self, p):
		self.p = p

	def buildProtocol(self, addr):
		self.CPro = commandConnProtocol(self.p)
		return self.CPro


class Gamespace:
	def __init__(self):
		# Basic Initialization
		self.state = 'intro'
		pygame.init()
		self.myfont = pygame.font.SysFont("monospace",50)
		self.myfont2 = pygame.font.SysFont("monospace",25)
		self.myfont3 = pygame.font.SysFont("monospace",20)
		pygame.key.set_repeat(1,50)

		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)

		# initialize backgrounds / images
		self.arenabackground = pygame.image.load('battlearena.png')
		self.arenaRect = self.arenabackground.get_rect()
		self.oppturn = pygame.image.load('oppturn.png')
		self.oppturnRect = self.oppturn.get_rect()
		self.oppturnRect.y = 200
		self.yourturn = pygame.image.load('yourturn.png')
		self.yourturnRect = self.yourturn.get_rect()
		self.yourturnRect.y = 344
		

		# Title Screen
		g = 1
		self.screen.fill(self.black)
		image = pygame.image.load('selection.png')	
		rect = image.get_rect()
		title = self.myfont.render("CREATURE BATTLERS!", 1, (255,255,255))
		inst = self.myfont2.render("<Press Any Key to Continue>", 1, (200,200,200))
		self.screen.blit(image, rect)
		self.screen.blit(inst, (220, 230))
		self.screen.blit(title, (140,200))
		pygame.display.flip()

		while g:
			events = pygame.event.get()
			for event in events:
				if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
					g = 0
					break
				
				elif event.type == QUIT:
					pygame.display.quit()
					pygame.quit()
					sys.exit()
		

		# Creature Selection Screen 
		# Set up Player Object
		self.screen.fill(self.black)
		select = self.myfont.render("Select a Creature!", 1, (255,255,255))
		image = pygame.image.load('selection2.png')	
		rect = image.get_rect()
		self.screen.blit(image, rect)
		self.screen.blit(select, (200, 100))
		pygame.display.flip()	
		
		g = 1	
		while g:

			events = pygame.event.get()
			for event in events:

				if event.type == MOUSEBUTTONDOWN:
					mx, my = pygame.mouse.get_pos()	
					if mx < 205:
						print "GRASS CREATURE SELECTED!"		
						self.player = Player('Grass')
						self.player.creature = creature.Grass(0)
						self.bar = pygame.image.load('grassbar.png')
						self.barRect = self.bar.get_rect()
						self.barRect.y = 372
						g = 0
						break
					elif mx < 442:
						print "WATER CREATURE SELECTED!"		
						self.player = Player('Water')
						self.player.creature = creature.Water(0)
						self.bar = pygame.image.load('waterbar.png')
						self.barRect = self.bar.get_rect()
						self.barRect.y = 372
						g = 0
						break	
					elif mx < 640:
						print "FIRE CREATURE SELECTED!"		
						self.player = Player('Fire')
						self.player.creature = creature.Fire(0)
						self.bar = pygame.image.load('firebar.png')
						self.barRect = self.bar.get_rect()
						self.barRect.y = 372
						g = 0
						break	

				elif event.type == QUIT:	
					sys.exit()
	
		self.screen.fill(self.black)
		image = pygame.image.load('selection.png')	
		rect = image.get_rect()
		title = self.myfont.render("Waiting for Opponent!", 1, (255,255,255))
		self.screen.blit(image, rect)
		self.screen.blit(title, (140,200))
		pygame.display.flip()	
		


	def main(self):
		self.cType = self.myfont2.render(self.player.cid, 1, (250, 250, 250))
		self.CFactory = commandConnFactory(self.player)
		reactor.connectTCP('student02.cse.nd.edu', 40020, self.CFactory)
		lc = LoopingCall(self.gameloop)		
		lc.start(.5)
		reactor.run()
		sys.exit()
		return


	def gameloop(self):

		self.oType = self.myfont2.render(self.player.oid, 1, (250, 250, 250))

		# Check if other player is connected.
		# If connected, start battle mode
		if self.player.state == 'connected':
			self.CFactory.CPro.transport.write(str(self.player.cid))


		elif self.player.state == 'battle':
			
			self.screen.fill(self.black)
			self.screen.blit(self.arenabackground, self.arenaRect)
			self.screen.blit(self.cType, (133,21))
			self.screen.blit(self.oType, (395,21))

			# display creatures HERE
			self.screen.blit(self.player.creature.image, self.player.creature.rect)
			self.screen.blit(self.player.ecreature.image, self.player.ecreature.rect)
			########################
			
			self.displayStats()
			self.screen.blit(self.bar, self.barRect)
			
			if self.player.creature.currentHealth <= 0 or self.player.ecreature.currentHealth <=0:
				self.player.state = 'gameover'
		
			elif self.player.turn == 0:
				self.screen.blit(self.oppturn, self.oppturnRect)
				events = pygame.event.get()
				for e in events:
					if e.type == QUIT:
						reactor.stop()
						return
			else:
				self.screen.blit(self.yourturn, self.yourturnRect)
				
				events = pygame.event.get()
				for e in events:
					if e.type == MOUSEBUTTONDOWN:
						# Check which move is selected
						mx, my = pygame.mouse.get_pos()	
						
						if mx < 320 and my > 372 and my < 425.5:
							self.player.turn = 0
							print "Attack!"
						elif mx < 320 and my > 426 and my < 479.5:
							self.player.turn = 0
							print "Ultimate Attack!"
						elif mx > 339 and mx < 474.7 and my > 427.49 and my < 480:							
							self.player.turn = 0
							print 'Forwards!'
						elif mx > 477.5 and my > 427.49:
							self.player.turn = 0
							print 'Backwards!'
			
						if self.player.turn == 0:
							break;

					if e.type == QUIT:
						reactor.stop()
						return

				if self.player.turn == 0:
					self.CFactory.CPro.switchTurn()

		elif self.player.state == 'quit':
			self.screen.fill(self.black)
			title = self.myfont.render("Opponent Forfeited. YOU WIN!", 1, (255,255,255))
			self.screen.blit(title, (50,200))
			pygame.display.flip()
			time.sleep(4)
			reactor.stop()
			return

		# Game stops and exits after a player wins
		elif self.player.state == 'gameover':
			self.screen.fill(self.black)
			self.screen.blit(self.arenabackground, self.arenaRect)
			self.screen.blit(self.cType, (133,21))
			self.screen.blit(self.oType, (395,21))

			# display creatures HERE
			self.screen.blit(self.player.creature.image, self.player.creature.rect)
			self.screen.blit(self.player.ecreature.image, self.player.ecreature.rect)
			########################
			
			self.displayStats()	

			if self.player.creature.currentHealth > self.player.ecreature.currentHealth:
				title = self.myfont.render("Congratulations! YOU WIN!", 1, (255,255,255))
			else:
				title = self.myfont.render("Better luck next time!", 1, (255,255,255))

			self.screen.blit(title, (50,200))
			self.screen.blit(self.bar, self.barRect)
			pygame.display.flip()
			time.sleep(4)
			reactor.stop()
			return
			

		pygame.display.flip()
			

	def displayStats(self):
		h = str(self.player.creature.currentHealth) + "/" + str(self.player.creature.health)
		Health = self.myfont3.render(str(h), 1, (250,250,250))
		MP = self.myfont3.render(str(self.player.creature.MP), 1, (250,250,250))
		Attack = self.myfont3.render(str(self.player.creature.Attack), 1, (250,250,250))
		Defense = self.myfont3.render(str(self.player.creature.Defense), 1, (250,250,250))
		self.screen.blit(Health, (140, 42))
		self.screen.blit(MP, (119,66))
		self.screen.blit(Attack, (271,42))
		self.screen.blit(Defense, (287,66))

		h = str(self.player.ecreature.currentHealth) + "/" + str(self.player.ecreature.health)
		Health = self.myfont3.render(str(h), 1, (250,250,250))
		MP = self.myfont3.render(str(self.player.ecreature.MP), 1, (250,250,250))
		Attack = self.myfont3.render(str(self.player.ecreature.Attack), 1, (250,250,250))
		Defense = self.myfont3.render(str(self.player.ecreature.Defense), 1, (250,250,250))
		self.screen.blit(Health, (406,42))
		self.screen.blit(MP, (381,66))
		self.screen.blit(Attack, (543,42))
		self.screen.blit(Defense, (543,66))
			
		
			

		
		


if __name__ == '__main__':
	g = Gamespace()	
	g.main()
	

