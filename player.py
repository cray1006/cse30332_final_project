# Christopher Ray  &  Dinh Do
# Creature Battler - Final Project
# player.py


import sys, pygame, math
from pygame.locals import *
from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall


class Player:
	def __init__(self, P):
   		self.creature = P
   		self.eCreature = None
		self.id = None
		self.state = 'start'

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
		print "RECEIVED: " + str(data)
		if self.state == 'start':
			if data == 'Opponent Connected':
				self.player.state = 'connected'
			elif data == '1':
				self.player.id = data
			elif data == '2':
				self.player.id = data
				self.player.state = 'connected'

		#elif state == 'connected':
			


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
		pygame.key.set_repeat(1,50)

		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)
		

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
						self.player = Player('G')
						g = 0
						break
					elif mx < 442:
						print "WATER CREATURE SELECTED!"		
						self.player = Player('W')
						g = 0
						break	
					elif mx < 640:
						print "FIRE CREATURE SELECTED!"		
						self.player = Player('F')
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
		self.CFactory = commandConnFactory(self.player)
		reactor.connectTCP('student02.cse.nd.edu', 40020, self.CFactory)
		lc = LoopingCall(self.gameloop)
		lc.start(1)
		reactor.run()


	def gameloop(self):
		#print str(self.player.state)
		if self.player.state == "connected":
			print "Both Players are connected!"
			self.state = 'connected'

		if self.state == 'connected':
			print "GAMEPLAY START!"
			white = 255,255,255
			self.screen.fill(white)
			title = self.myfont.render("Start Gameplay!", 1, (23,57,100))
			self.screen.blit(title, (220, 230))
			pygame.display.flip()
		


if __name__ == '__main__':
	g = Gamespace()	
	g.main()

