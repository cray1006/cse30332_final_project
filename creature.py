# Christopher Ray & Dinh Do
# Creature Battler - Final Project
# creature.py

# Placeholder values! feel free to change

import sys, pygame, math, time
from pygame.locals import *

class Water:
	def __init__(self, player):
		self.health = 100
		self.currentHealth = 100
		self.MP = 100
		self.Attack = .5
		self.Defense = 2
		self.move = 1
		self.state = "normal"	#"normal", "frozen", or "drain"

		if(player == 0):
			self.image = pygame.image.load('water_back.png')
			self.rect = self.image.get_rect()
			self.rect.x = 272
			self.rect.y = 221
		else:
			self.image = pygame.image.load('water_front.png')
			self.rect = self.image.get_rect()
			self.rect.x = 373
			self.rect.y = 221
		
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)

class Fire:
	def __init__(self):
		self.health = 100
		self.currentHealth = 100
		self.MP = 100
		self.Attack = 1.5
		self.Defense = 1
		self.move = 2
		self.state = "normal"

		if(player == 0):
			self.image = pygame.image.load('fire_back.png')
			self.rect = self.image.get_rect()
			self.rect.x = 272
			self.rect.y = 221
		else:
			self.image = pygame.image.load('fire_front.png')
			self.rect = self.image.get_rect()
			self.rect.x = 373
			self.rect.y = 221
		
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)

class Grass:
	def __init__(self):
		self.health = 200
		self.currentHealth = 100
		self.MP = 100
		self.Attack = 1
		self.Defense = 0
		self.move = 2
		self.state = "normal"

		if(player == 0):
			self.image = pygame.image.load('grass_back.png')
			self.rect = self.image.get_rect()
			self.rect.x = 272
			self.rect.y = 221
		else:
			self.image = pygame.image.load('grass_front.png')
			self.rect = self.image.get_rect()
			self.rect.x = 373
			self.rect.y = 221
		
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)
