# Christopher Ray & Dinh Do
# Creature Battler - Final Project
# CSE 30332
# 7 May 2015

# player.py
#Class definition for Creature Battler Players and for the game space


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
	def __init__(self, P, screen):	#defining __init
   		self.cid = P		# Creature ID: Grass / Water / Fire
		self.oid = None 	# Opponent ID: Grass / Water / Fire 
		self.creature = None  	# User Creature class
		self.ecreature = None	# Opponent creature class
		self.id = None		# id is index of server protocol list
		self.state = 'start'
		self.turn = None	# second player to connect gets first turn
		self.screen = screen

	def tick(self):	#tick function
		return


class commandConnProtocol(Protocol):	#class definition for command connection
	def __init__(self, player):	#defining __init__
		self.player = player	
		self.state = 'start'

	def connectionMade(self):	#let user know a connection was made
		print 'Connection Made!' 
		return

	def dataReceived(self, data):	#defining dataReceived handler
		if self.state == 'start':	#if player is in start state...	
			if data == '0':
				self.player.id = data	#setting player ID and turn
				self.player.turn = 1
			elif data == '1':
				self.player.id = data
				self.player.state = 'connected'	#setting player state to connected
				self.player.turn = 0
				self.transport.write (str(self.player.cid))	#sending data to opponent player
			else:	#setting information about the opponent's creature
				if data == 'Water':
					self.player.ecreature = creature.Water(1)	
					self.player.oid = str(data)
				elif data == 'Grass':
					self.player.ecreature = creature.Grass(1)	
					self.player.oid = str(data)
				elif data == 'Fire':
					self.player.ecreature = creature.Fire(1)
					self.player.oid = str(data)
				self.transport.write (str(self.player.cid))	#sending data to opponent player
				self.state = 'battle'	#setting states
				self.player.state = 'battle'

		elif self.state == 'connected':	#if we are in the connected state...
			print "Opponent type is " + data	#letting user know what the opponent is playing
			self.player.oid = str(data)	#setting information about the opponent's creature
			if data == 'Water':
				self.player.ecreature = creature.Water(1)
			elif data == 'Grass':
				self.player.ecreature = creature.Grass(1)
			elif data == 'Fire':
				self.player.ecreature = creature.Fire(1)
			self.state = 'battle'	#changin states
			self.player.state = 'battle'

		elif self.state == 'battle':	#if we are in the battle state...
			if data == 'quit':	#opponent has quit the game, so change state accordingly
				self.player.state = 'quit'
			else:	#interpreting the opponents moves, which have been broadcast across the connection, as commands to the enemy creauture
				if data == 'primary':
					self.player.ecreature.primary(self.player.creature, self.player.screen)
				elif data == 'ultimate':
					self.player.ecreature.ultimate(self.player.creature, self.player.screen)
				elif data == 'right':
					self.player.ecreature.move("right", self.player.creature)
				elif data == 'left':
					self.player.ecreature.move("left", self.player.creature)	

				self.player.turn = 1	#changing turns		


class commandConnFactory(ClientFactory):	#defining command connection factory
	def __init__(self, p):	#defining init
		self.p = p

	def buildProtocol(self, addr):	#building the command connection protocol
		self.CPro = commandConnProtocol(self.p)
		return self.CPro


class Gamespace:	#defining the gamespace
	def __init__(self):
		# Basic Initialization
		self.state = 'intro'
		pygame.init()	#initializing pygame and pygame mixer
		pygame.mixer.init()
		pygame.mixer.music.load('./music/title.wav')	#loading music that will loop in the background
		pygame.mixer.music.play(-1, 0.0)
		self.myfont = pygame.font.SysFont("monospace",30)	#defining fonts
		self.myfont2 = pygame.font.SysFont("monospace",20)
		self.myfont3 = pygame.font.SysFont("monospace",15)
		pygame.key.set_repeat(1,50)

		self.size = self.width, self.height = 640, 480	#defining window size
		self.black = 0, 0, 0	
		self.screen = pygame.display.set_mode(self.size)	#creating screen

		# initialize backgrounds / images
		self.arenabackground = pygame.image.load('battlearena.png')	#arena background image
		self.arenaRect = self.arenabackground.get_rect()	#arena background image rect
		self.oppturn = pygame.image.load('oppturn.png')	#opponent turn banner image
		self.oppturnRect = self.oppturn.get_rect()	#opponent turn banner rect
		self.oppturnRect.y = 380	#position opponent turn banner
		self.yourturn = pygame.image.load('yourturn.png')	#player turn banner image
		self.yourturnRect = self.yourturn.get_rect()	#player turn image rect
		self.yourturnRect.y = 344	#position player turn banner
		

		# Title Screen
		g = 1
		self.screen.fill(self.black)
		image = pygame.image.load('selection2.png')	#title screen background image
		rect = image.get_rect()
		title = self.myfont.render("CREATURE BATTLERS!", 1, (255,255,255))	#title
		inst = self.myfont2.render("<Press Any Key to Continue>", 1, (200,200,200))
		self.screen.blit(image, rect)	#displaying title screen
		self.screen.blit(inst, (220, 230))
		self.screen.blit(title, (140,200))
		pygame.display.flip()

		while g:	#checking for mouseclicks or key presses in order to proceed to the next screen (can also quit)
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
		select = self.myfont.render("Select a Creature!", 1, (255,255,255))	#prompt for the user
		image = pygame.image.load('selection.png')	#selection screen background image
		rect = image.get_rect()
		self.screen.blit(image, rect)	#displaying the selection screen
		self.screen.blit(select, (200, 100))
		pygame.display.flip()	
		
		g = 1	
		while g:	#checking for mouse clicks or a quit
			events = pygame.event.get()
			for event in events:
				# initialize player creature based on selection (clicking in a certain area selects the creature)
				if event.type == MOUSEBUTTONDOWN:
					mx, my = pygame.mouse.get_pos()	
					if mx < 205:
						print "GRASS CREATURE SELECTED!"		
						self.player = Player('Grass', self.screen)	#initialzing player, creature, and UI images
						self.player.creature = creature.Grass(0)
						self.bar = pygame.image.load('grassbar.png')
						self.barRect = self.bar.get_rect()
						self.barRect.y = 372
						g = 0
						break
					elif mx < 442:
						print "WATER CREATURE SELECTED!"		
						self.player = Player('Water', self.screen)
						self.player.creature = creature.Water(0)
						self.bar = pygame.image.load('waterbar.png')
						self.barRect = self.bar.get_rect()
						self.barRect.y = 372
						g = 0
						break	
					elif mx < 640:
						print "FIRE CREATURE SELECTED!"		
						self.player = Player('Fire', self.screen)
						self.player.creature = creature.Fire(0)
						self.bar = pygame.image.load('firebar.png')
						self.barRect = self.bar.get_rect()
						self.barRect.y = 372
						g = 0
						break	

				elif event.type == QUIT:	
					sys.exit()
	
		self.screen.fill(self.black) #display waiting screen until opponent connects
		image = pygame.image.load('selection2.png')	
		rect = image.get_rect()
		title = self.myfont.render("Waiting for Opponent!", 1, (255,255,255))
		self.screen.blit(image, rect)
		self.screen.blit(title, (140,200))
		pygame.display.flip()	
		


	def main(self):	#defining main function
		self.cType = self.myfont2.render(self.player.cid, 1, (250, 250, 250))	#defining font
		self.CFactory = commandConnFactory(self.player)	#defining factory
		reactor.connectTCP('student02.cse.nd.edu', 40020, self.CFactory)	#connecting to the server
		lc = LoopingCall(self.gameloop)	#setting up game loop and reactor	
		lc.start(.5)
		reactor.run()
		sys.exit()
		return


	def gameloop(self):	#defining game loop function
		self.oType = self.myfont2.render(self.player.oid, 1, (250, 250, 250))
		mp = 0

		if self.player.state == 'battle':
			# display background
			self.screen.fill(self.black)
			self.screen.blit(self.arenabackground, self.arenaRect)
			self.screen.blit(self.cType, (133,21))
			self.screen.blit(self.oType, (395,21))

			# display creatures here
			self.screen.blit(self.player.creature.image, self.player.creature.rect)
			self.screen.blit(self.player.ecreature.image, self.player.ecreature.rect)
			
			# display stats and options menu
			self.displayStats()
			self.screen.blit(self.bar, self.barRect)
			
			# Check if gameover
			if self.player.creature.currentHealth <= 0 or self.player.ecreature.currentHealth <=0:
				self.player.state = 'gameover'
		
			# Check turn and process input based on turn selection
			elif self.player.turn == 0:	#this is the opponent's turn (input to enemy creature coming in across the network)
				self.screen.blit(self.oppturn, self.oppturnRect)	#displaying game
				events = pygame.event.get()
				for e in events:	#checking if the player quits
					if e.type == QUIT:
						reactor.stop()
						return
			else:
				self.screen.blit(self.yourturn, self.yourturnRect)	#displaying game
				
				events = pygame.event.get()
				for e in events:	#checking for events
					if e.type == MOUSEBUTTONDOWN:
						# Check which move is selected
						# based on mouse position
						mx, my = pygame.mouse.get_pos()	
						
						if mx < 320 and my > 372 and my < 425.5:	#primary attack selected
							self.player.turn = 0	#change turns
							self.player.creature.primary(self.player.ecreature, self.screen)	#use primary attack
							self.CFactory.CPro.transport.write('primary')	#send information to other player
						elif mx < 320 and my > 426 and my < 479.5:	#ultimate attack selected
							if self.player.creature.MP >= 100:	#check if creature can actually use ultimate
								self.player.turn = 0
								self.player.creature.ultimate(self.player.ecreature, self.screen)	#use attack
								self.CFactory.CPro.transport.write('ultimate')	#send info to other player
							else:	#display error message, not enough MP
								msg = pygame.image.load('mpmsg.png')
								mrect = msg.get_rect()
								mrect.y = 200
								self.screen.blit(msg, mrect)
								mp = 1
								break
						elif mx > 339 and mx < 474.7 and my > 427.49 and my < 480:  #move right				
							self.player.turn = 0
							self.player.creature.move("right", self.player.ecreature)	#move the sprite
							self.CFactory.CPro.transport.write('right')	#send info to other player
						elif mx > 477.5 and my > 427.49:	#move left
							self.player.turn = 0
							self.player.creature.move("left", self.player.ecreature)
							self.CFactory.CPro.transport.write('left')
			
						if self.player.turn == 0:
							break;

					if e.type == QUIT:
						reactor.stop()
						return

				self.player.creature.tick()	#idle animations

		# if opponent disconnects
		elif self.player.state == 'quit':
			self.screen.fill(self.black)	#display forfeit screen 
			title = self.myfont.render("Opponent Forfeited. \nYOU WIN!", 1, (255,255,255))	
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

			# display creatures here
			self.screen.blit(self.player.creature.image, self.player.creature.rect)
			self.screen.blit(self.player.ecreature.image, self.player.ecreature.rect)
			
			self.displayStats()	

			# Check who the winner is
			if self.player.creature.currentHealth > self.player.ecreature.currentHealth:
				msg = pygame.image.load('won.png')
				mrect = msg.get_rect()
				mrect.y = 200
			else:
				msg = pygame.image.load('lost.png')

			mrect = msg.get_rect()	#display victory or defeat banners
			mrect.y = 200
			self.screen.blit(msg, mrect)
			self.screen.blit(self.bar, self.barRect)
			pygame.display.flip()
			time.sleep(4)
			reactor.stop()
			return
			

		pygame.display.flip()
		if mp == 1:
			time.sleep(2)
			

	# Function to Display Battle Stats
	def displayStats(self):
		#player creature stats
		h = str(int(self.player.creature.currentHealth)) + "/" + str(self.player.creature.health)
		Health = self.myfont3.render(str(h), 1, (250,250,250))
		mp = str(self.player.creature.MP) + "/100"
		MP = self.myfont3.render(mp, 1, (250,250,250))
		Attack = self.myfont3.render(str(self.player.creature.Attack), 1, (250,250,250))
		Defense = self.myfont3.render(str(self.player.creature.Defense), 1, (250,250,250))
		self.screen.blit(Health, (140, 42))
		self.screen.blit(MP, (119,66))
		self.screen.blit(Attack, (271,42))
		self.screen.blit(Defense, (287,66))

		#opponent creature's stats
		h = str(int(self.player.ecreature.currentHealth)) + "/" + str(self.player.ecreature.health)
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
