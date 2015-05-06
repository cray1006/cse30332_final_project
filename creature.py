# Christopher Ray & Dinh Do
# Creature Battler - Final Project
# creature.py

# Placeholder values! feel free to change

import sys, pygame, math, time, os
from pygame.locals import *

class fireball(pygame.sprite.Sprite):
	def __init__(self, player, x, y, gs = None):
		self.gs = gs
		self.image = pygame.image.load('fireball.png')

		if(player != 0):
			self.image = pygame.transform.flip(self.image, 1, 0)

		self.rect = self.image.get_rect()
		self.rex.x = x
		self.rect.y = y
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)
		self.player = player

	def move(self):
		if(self.player == 0):
			self.rect = self.rect.move(100, 0)
		else:
			self.rect = self.rect.move(-100, 0)


class pyro(pygame.sprite.Sprite):
	def __init__(self, player, x, y, gs = None):
		self.gs = gs
		self.image = pygame.image.load('pyroblast.png')

		if(player != 0):
			self.image = pygame.transform.flip(self.image, 1, 0)

		self.rect = self.image.get_rect()
		self.rex.x = x
		self.rect.y = y
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)
		self.player = player

	def move(self):
		if(self.player == 0):
			self.rect = self.rect.move(100, 0)
		else:
			self.rect = self.rect.move(-100, 0)

class ice(pygame.sprite.Sprite):
	def __init__(self, player, x, y, gs = None):
		self.gs = gs
		self.image = pygame.image.load('ice_lance.png')

		if(player != 0):
			self.image = pygame.transform.flip(self.image, 1, 0)

		self.rect = self.image.get_rect()
		self.rex.x = x
		self.rect.y = y
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)
		self.player = player

	def move(self):
		if(self.player == 0):
			self.rect = self.rect.move(100, 0)
		else:
			self.rect = self.rect.move(-100, 0)


class freeze(pygame.sprite.Sprite):
	def __init__(self, player, x, y, gs = None):
		self.gs = gs
		self.image = pygame.image.load('freeze.png')

		if(player != 0):
			self.image = pygame.transform.flip(self.image, 1, 0)

		self.rect = self.image.get_rect()
		self.rex.x = x
		self.rect.y = y
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)
		self.player = player

	def move(self):
		if(self.player == 0):
			self.rect = self.rect.move(100, 0)
		else:
			self.rect = self.rect.move(-100, 0)


class vine(pygame.sprite.Sprite):
	def __init__(self, player, x, y, gs = None):
		self.gs = gs
		self.image = pygame.image.load('vine_whip.png')

		if(player != 0):
			self.image = pygame.transform.flip(self.image, 1, 0)

		self.rect = self.image.get_rect()
		self.rex.x = x
		self.rect.y = y
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)
		self.player = player

	def move(self):
		if(self.player == 0):
			self.rect = self.rect.move(100, 0)
		else:
			self.rect = self.rect.move(-100, 0)


class giga(pygame.sprite.Sprite):
	def __init__(self, player, x, y, gs = None):
		self.gs = gs
		self.image = pygame.image.load('giga_drain.png')

		if(player != 0):
			self.image = pygame.transform.flip(self.image, 1, 0)

		self.rect = self.image.get_rect()
		self.rex.x = x
		self.rect.y = y
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)
		self.player = player

	def move(self):
		if(self.player == 0):
			self.rect = self.rect.move(100, 0)
		else:
			self.rect = self.rect.move(-100, 0)
	
		
class Water(pygame.sprite.Sprite):
	def __init__(self, player, gs = None):
		self.gs = gs
		self.health = 100
		self.currentHealth = 100
		self.MP = 100
		self.Attack = 0.1
		self.Defense = 2
		self.move = 1
		self.state = "normal"	#"normal", "frozen", or "drain"
		self.frozen = 0
		self.drain = 0
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
		if(self.state != "frozen"):
			if(self.player == 0):
				if((direction == "left") and (self.rect.x > 100)):
					self.rect = self.rect.move(-100, 0)
				elif((direction == "right") and (self.rect.x < 300)):
					self.rect = self.rect.move(100, 0)
			else:
				if((direction == "left") and (self.rect.x > 350)):
					self.rect = self.rect.move(-100, 0)
				elif((direction == "right") and (self.rect.x < 550)):
					self.rect = self.rect.move(100, 0)

	def is_hit(self, attack, damage):
		if((attack == "primary") or (attack == "pyro")):
			self.health -= (damage - (10 / self.Defense))
		elif(attack == "freeze"):
			self.state = "frozen"
			self.frozen = 0
		elif(attack == "giga"):
			self.state = "drain"
			self.drain = 0

	def primary(self, enemy, screen):
		lance = ice(self.player, self.rect.centerx, self.rect.centery, self.gs)
		base = 10
		damage = base + (base * self.Attack)
		i = 0
		while(i < 3):
			lance.move()
			screen.blit(lance.image, lance.rect)
			pygame.display.flip()
			if(pygame.sprite.collide_rect(lance, enemy)):
				enemy.is_hit("primary", damage)
				break

	def ultimate(self, enemy, screen):
		if(self.MP >= 50):
			self.MP -= 50
			f = freeze(self.player, self.rect.centerx, self.rect.centery, self.gs)
			base = 0
			damage = base + (base * self.Attack)
			i = 0
			while(i < 2):
				f.move()
				screen.blit(f.image, f.rect)
				pygame.display.flip()
				if(pygame.sprite.collide_rect(f, enemy)):
					enemy.is_hit("freeze")
					break
				
	def update(self, enemy):
		if(self.state == "drain"):
			self.health -= 10
			if(enemy.health < 200):
				enemy.health += 10

				if(enemy.health >= 200):
					enemy.health = 200

			if(self.drain < 3):
				self.drain += 1
			else:
				self.state = "normal"

		if(self.health <= 0):
			return 1
		else:
			if(self.MP < 100):
				self.MP += 25
				if(self.MP >= 100):
					self.MP = 100
			
			if(self.state == "frozen"):
				if(self.frozen < 1):
					self.frozen += 1
				else:
					self.state = "normal"

				
class Fire(pygame.sprite.Sprite):
	def __init__(self, player, gs = None):
		self.gs = gs
		self.health = 100
		self.currentHealth = 100
		self.MP = 100
		self.Attack = .5
		self.Defense = 1.5
		self.move = 2
		self.state = "normal"
		self.player = player
		self.frozen = 0
		self.drain = 0

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
		if(self.state != "frozen"):
			if(self.player == 0):
				if((direction == "left") and (self.rect.x > 100)):
					self.rect = self.rect.move(-100, 0)
				elif((direction == "right") and (self.rect.x < 300)):
					self.rect = self.rect.move(100, 0)
			else:
				if((direction == "left") and (self.rect.x > 350)):
					self.rect = self.rect.move(-100, 0)
				elif((direction == "right") and (self.rect.x < 550)):
					self.rect = self.rect.move(100, 0)

	def is_hit(self, attack, damage):
		if((attack == "primary") or (attack == "pyro")):
			self.health -= (damage - (10 / self.Defense))
		elif(attack == "freeze"):
			self.state = "frozen"
			self.frozen = 0
		elif(attack == "giga"):
			self.state = "drain"
			self.drain = 0

	def primary(self, enemy, screen):
		fb = fireball(self.player, self.rect.centerx, self.rect.centery, self.gs)
		base = 10
		damage = base + (base * self.Attack)
		i = 0
		while(i < 3):
			fb.move()
			screen.blit(fb.image, fb.rect)
			pygame.display.flip()
			if(pygame.sprite.collide_rect(fb, enemy)):
				enemy.is_hit("primary", damage)
				break

	def ultimate(self, enemy, screen):
		if(self.MP >= 100):
			self.MP -= 100
			pb = pyro(self.player, self.rect.centerx, self.rect.centery, self.gs)
			base = 50
			damage = base + (10 * self.Attack)
			i = 0
			while(i < 2):
				pb.move()
				screen.blit(pb.image, pb.rect)
				pygame.display.flip()
				if(pygame.sprite.collide_rect(pb, enemy)):
					enemy.is_hit("pyro")
					break
				
	def update(self, enemy):
		if(self.state == "drain"):
			self.health -= 10
			if(enemy.health < 200):
				enemy.health += 10
				if(enemy.health >= 200):
					enemy.health = 200

			if(self.drain < 3):
				self.drain += 1
			else:
				self.state = "normal"

		if(self.health <= 0):
			return 1
		else:
			if(self.MP < 100):
				self.MP += 25
				if(self.MP >= 100):
					self.MP = 100
			
			if(self.state == "frozen"):
				if(self.frozen < 1):
					self.frozen += 1
				else:
					self.state = "normal"

class Grass(pygame.sprite.Sprite):
	def __init__(self, player, gs = None):
		self.gs = gs
		self.health = 200
		self.currentHealth = 100
		self.MP = 100
		self.Attack = 1
		self.Defense = 1
		self.move = 2
		self.state = "normal"
		self.player = player
		self.frozen = 0
		self.drain = 0

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
		if(self.state != "frozen"):
			if(self.player == 0):
				if((direction == "left") and (self.rect.x > 100)):
					self.rect = self.rect.move(-100, 0)
				elif((direction == "right") and (self.rect.x < 300)):
					self.rect = self.rect.move(100, 0)
			else:
				if((direction == "left") and (self.rect.x > 350)):
					self.rect = self.rect.move(-100, 0)
				elif((direction == "right") and (self.rect.x < 550)):
					self.rect = self.rect.move(100, 0)

	def is_hit(self, attack, damage):
		if((attack == "primary") or (attack == "pyro")):
			self.health -= (damage - (10 / self.Defense))
		elif(attack == "freeze"):
			self.state = "frozen"
			self.frozen = 0
		elif(attack == "giga"):
			self.state = "drain"
			self.drain = 0

	def primary(self, enemy, screen):
		whip = vine(self.player, self.rect.centerx, self.rect.centery, self.gs)
		base = 10
		damage = base + (base * self.Attack)
		i = 0
		while(i < 3):
			whip.move()
			screen.blit(whip.image, whip.rect)
			pygame.display.flip()
			if(pygame.sprite.collide_rect(whip, enemy)):
				enemy.is_hit("primary", damage)
				break

	def ultimate(self, enemy, screen):
		if(self.MP >= 100):
			self.MP -= 100
			gd = giga(self.player, self.rect.centerx, self.rect.centery, self.gs)
			base = 0
			damage = base + (base * self.Attack)
			i = 0
			while(i < 2):
				gd.move()
				screen.blit(gd.image, gd.rect)
				pygame.display.flip()
				if(pygame.sprite.collide_rect(gd, enemy)):
					enemy.is_hit("giga")
					break
				
	def update(self, enemy):
		if(self.state == "drain"):
			self.health -= 10
			if(enemy.health < 200):
				enemy.health += 10
				
				if(enemy.health >= 200):
					enemy.health = 200

			if(self.drain < 3):
				self.drain += 1
			else:
				self.state = "normal"

		if(self.health <= 0):
			return 1
		else:
			if(self.MP < 100):
				self.MP += 25
			
			if(self.state == "frozen"):
				if(self.frozen < 1):
					self.frozen += 1
				else:
					self.state = "normal"
