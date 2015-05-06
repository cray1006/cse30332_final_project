# Christopher Ray & Dinh Do
# Creature Battler - Final Project
# creature.py

# Placeholder values! feel free to change

import sys, pygame, math, time, os
from pygame.locals import *

#class 

class Water(pygame.sprite.Sprite):
	def __init__(self, player, gs = None):
		self.gs = gs
		self.health = 100
		self.currentHealth = 100
		self.MP = 100
		self.Attack = .5
		self.Defense = 2
		self.move = 1
		self.state = "normal"	#"normal", "frozen", or "drain"
		self.player = player

		if(self.player == 0):
			self.image = pygame.image.load('water_back.png')
			self.rect = self.image.get_rect()
			self.rect.x = 200
			self.rect.y = 221
		else:
			self.image = pygame.image.load('water_front.png')
			self.rect = self.image.get_rect()
			self.rect.x = 450
			self.rect.y = 221
		
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)

	def move(self, direction):
		if(self.player == 0):
			if((direction == "left") and (self.rect.x > 100)):
				self.rect.x -= 100
			elif((direction == "right") and (self.rect.x < 300)):
				self.rect.x += 100
		else:
			if((direction == "left") and (self.rect.x > 350)):
				self.rect.x -= 100
			elif((direction == "right") and (self.rect.x < 550)):
				self.rect.x += 100

	def primary(self):
		

class Fire(pygame.sprite.Sprite):
	def __init__(self, player, gs = None):
		self.gs = gs
		self.health = 100
		self.currentHealth = 100
		self.MP = 100
		self.Attack = 1.5
		self.Defense = 1
		self.move = 2
		self.state = "normal"
		self.player = player

		if(self.player == 0):
			self.image = pygame.image.load('fire_back.png')
			self.rect = self.image.get_rect()
			self.rect.x = 200
			self.rect.y = 221
		else:
			self.image = pygame.image.load('fire_front.png')
			self.rect = self.image.get_rect()
			self.rect.x = 450
			self.rect.y = 221
		
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)

	def move(self, direction):
		if(self.player == 0):
			if((direction == "left") and (self.rect.x > 100)):
				self.rect.x -= 100
			elif((direction == "right") and (self.rect.x < 300)):
				self.rect.x += 100
		else:
			if((direction == "left") and (self.rect.x > 350)):
				self.rect.x -= 100
			elif((direction == "right") and (self.rect.x < 550)):
				self.rect.x += 100

class Grass(pygame.sprite.Sprite):
	def __init__(self, player, gs = None):
		self.gs = gs
		self.health = 200
		self.currentHealth = 100
		self.MP = 100
		self.Attack = 1
		self.Defense = 0
		self.move = 2
		self.state = "normal"
		self.player = player

		if(self.player == 0):
			self.image = pygame.image.load('grass_back.png')
			self.rect = self.image.get_rect()
			self.rect.x = 200
			self.rect.y = 221
		else:
			self.image = pygame.image.load('grass_front.png')
			self.rect = self.image.get_rect()
			self.rect.x = 450
			self.rect.y = 221
		
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)

	def move(self, direction):
		if(self.player == 0):
			if((direction == "left") and (self.rect.x > 100)):
				self.rect.x -= 100
			elif((direction == "right") and (self.rect.x < 300)):
				self.rect.x += 100
		else:
			if((direction == "left") and (self.rect.x > 350)):
				self.rect.x -= 100
			elif((direction == "right") and (self.rect.x < 550)):
				self.rect.x += 100
