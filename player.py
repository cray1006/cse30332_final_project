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


class Player:
	def __init__(self, P):
   		self.creature = P
   		self.eCreature = None

	def tick(self):
		return


class commandConnProtocol(Protocol):
	def __init__(self, player):
		self.player = player
		self.state = 'start'

	def connectionMade(self):
		print 'Command Connection Made!' 
		return

	#def dataReceived(self, data):
		if data == "Opponent Connected":
			self.state = 'connected'

	#check if opponent has connected
	def checkPlayer(self):
		if self.state == 'connected':
			return 1
		else:
			return 0
		

		


class commandConnFactory(ClientFactory):
	def __init__(self, p):
		self.p = p

	def buildProtocol(self, addr):
		self.CPro = commandConnProtocol(self.p)
		return self.CPro

class Gamespace:
	def main(self):
		# Basic Initialization
		#player = Player()
		pygame.init()
		myfont = pygame.font.SysFont("monospace",50)
		myfont2 = pygame.font.SysFont("monospace",25)
		pygame.key.set_repeat(1,50)

		self.size = self.width, self.height = 640, 480
		self.black = 0, 0, 0
		self.screen = pygame.display.set_mode(self.size)
		

		# Title Screen
		g = 1
		while g:
			events = pygame.event.get()
			for event in events:
				if event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
					g = 0
					break
				
				elif event.type == QUIT:
					sys.exit()
		
				else:
					self.screen.fill(self.black)
					image = pygame.image.load('selection.png')	
					rect = image.get_rect()
					title = myfont.render("CREATURE BATTLERS!", 1, (255,255,255))
					inst = myfont2.render("<Press Any Key to Continue>", 1, (200,200,200))
					self.screen.blit(image, rect)
					self.screen.blit(inst, (220, 230))
					self.screen.blit(title, (140,200))
					pygame.display.flip()

		# Creature Selection Screen 
		# Set up Player Object
		g = 1	
		while g:
			self.screen.fill(self.black)
			select = myfont.render("Select a Creature!", 1, (255,255,255))
			image = pygame.image.load('selection2.png')	
			rect = image.get_rect()
			self.screen.blit(image, rect)
			self.screen.blit(select, (200, 100))
			pygame.display.flip()	

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

		# Set up Game Objects
		#background = 		
		#Cfactory = commandConnFactory(self.player)
		#reactor.connectTCP('student00.cse.nd.edu', 40020, Cfactory)
		#reactor.run()

		# Check if opponent has connected to server
		#cp = Cfactory.CPro
		#while not cp.checkPlayer():
		while 1:		
			self.screen.fill(self.black)
			image = pygame.image.load('selection.png')	
			rect = image.get_rect()
			title = myfont.render("Waiting for Opponent!", 1, (255,255,255))
			self.screen.blit(image, rect)
			self.screen.blit(title, (140,200))
			pygame.display.flip()

			events = pygame.event.get()
			for event in events:
				if event.type == QUIT:
					sys.exit()
			

			

		# Start Game Loop

		
		


if __name__ == '__main__':
	g = Gamespace()
	g.main()

