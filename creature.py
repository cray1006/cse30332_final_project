# Christopher Ray & Dinh Do
# Creature Battler - Final Project
# creature.py


import sys, pygame, math, time, os
from pygame.locals import *

class fireball(pygame.sprite.Sprite):
	def __init__(self, player, x, y, gs = None):
		self.gs = gs
		self.image = pygame.image.load('fireball.png')

		if(player != 0):
			self.image = pygame.transform.flip(self.image, 1, 0)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)
		self.player = player

	def move(self):
		if(self.player == 0):
			self.rect = self.rect.move(75, 0)
		else:
			self.rect = self.rect.move(-75, 0)


class pyro(pygame.sprite.Sprite):
	def __init__(self, player, x, y, gs = None):
		self.gs = gs
		self.image = pygame.image.load('pyroblast.png')

		if(player != 0):
			self.image = pygame.transform.flip(self.image, 1, 0)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		color = self.image.get_at((10,10))
		self.image.set_colorkey(color)
		self.player = player

	def move(self):
		if(self.player == 0):
			self.rect = self.rect.move(75, 0)
		else:
			self.rect = self.rect.move(-75, 0)

class ice(pygame.sprite.Sprite):
	def __init__(self, player, x, y, gs = None):
		self.gs = gs
		self.image = pygame.image.load('ice_lance.png')

		if(player != 0):
			self.image = pygame.transform.flip(self.image, 1, 0)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)
		self.player = player

	def move(self):
		if(self.player == 0):
			self.rect = self.rect.move(75, 0)
		else:
			self.rect = self.rect.move(-75, 0)


class freeze(pygame.sprite.Sprite):
	def __init__(self, player, x, y, gs = None):
		self.gs = gs
		self.image = pygame.image.load('freeze.png')

		if(player != 0):
			self.image = pygame.transform.flip(self.image, 1, 0)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)
		self.player = player

	def move(self):
		if(self.player == 0):
			self.rect = self.rect.move(75, 0)
		else:
			self.rect = self.rect.move(-75, 0)


class vine(pygame.sprite.Sprite):
	def __init__(self, player, x, y, gs = None):
		self.gs = gs
		self.image = pygame.image.load('vine_whip.png')

		if(player != 0):
			self.image = pygame.transform.flip(self.image, 1, 0)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)
		self.player = player

	def move(self):
		if(self.player == 0):
			self.rect = self.rect.move(75, 0)
		else:
			self.rect = self.rect.move(-75, 0)


class giga(pygame.sprite.Sprite):
	def __init__(self, player, x, y, gs = None):
		self.gs = gs
		self.image = pygame.image.load('giga_drain.png')

		if(player != 0):
			self.image = pygame.transform.flip(self.image, 1, 0)

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)
		self.player = player

	def move(self):
		if(self.player == 0):
			self.rect = self.rect.move(75, 0)
		else:
			self.rect = self.rect.move(-75, 0)
	
		
class Water(pygame.sprite.Sprite):
	def __init__(self, player, gs = None):
		pygame.mixer.init()
		self.gs = gs
		self.health = 100
		self.currentHealth = 100
		self.MP = 0
		self.Attack = 1.3
		self.Defense = 2
		self.state = "normal"	#"normal", "frozen", or "drain"
		self.frozen = 0
		self.drain = 0
		self.player = player
		self.idle = 0
		self.recharge = 0

		if(self.player == 0):
			self.image = pygame.image.load('water_back.png')
			self.rect = self.image.get_rect()
			self.rect.x = 200
			self.rect.y = 177
		else:
			self.image = pygame.image.load('water_front.png')
			self.rect = self.image.get_rect()
			self.rect.x = 376
			self.rect.y = 177
		
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)

	def move(self, direction, enemy):
		if(self.state != "frozen"):
			if(self.player == 0):
				if((direction == "left") and (self.rect.x > 100)):
					self.rect = self.rect.move(-100, 0)
				elif((direction == "right") and (self.rect.x < 300)):
					self.rect = self.rect.move(100, 0)
			else:
				if((direction == "left") and (self.rect.x < 476)):
					self.rect = self.rect.move(100, 0)
				elif((direction == "right") and (self.rect.x > 276)):
					self.rect = self.rect.move(-100, 0)
	
		self.update(enemy)

	def is_hit(self, attack, damage):
		if((attack == "primary") or (attack == "pyro")):
			self.currentHealth -= (damage - (10 / self.Defense))
		elif(attack == "freeze"):
			self.state = "frozen"
			self.frozen = 0
		elif(attack == "giga"):
			self.state = "drain"
			self.drain = 0

	def primary(self, enemy, screen):
		if(self.state != "frozen"):
			cast = pygame.mixer.Sound('./music/ice_cast.ogg')
			hit = pygame.mixer.Sound('./music/ice_hit.ogg')
			cast.play()
			lance = ice(self.player, self.rect.centerx, self.rect.centery, self.gs)
			base = 15
			damage = (base * self.Attack)
			i = 0
			while(i < 2):
				i += 1
				lance.move()
				screen.blit(lance.image, lance.rect)
				pygame.display.flip()
				if(pygame.sprite.collide_rect(lance, enemy)):
					hit.play()
					enemy.is_hit("primary", damage)
					break
		
		self.update(enemy)

	def ultimate(self, enemy, screen):
		if((self.MP >= 100) and (self.state != "frozen")):
			cast = pygame.mixer.Sound('./music/ice_cast.ogg')
			hit = pygame.mixer.Sound('./music/ice_hit.ogg')
			cast.play()
			self.MP -= 100
			f = freeze(self.player, self.rect.centerx, self.rect.centery, self.gs)
			base = 0
			damage = (base * self.Attack)
			i = 0
			while(i < 2):
				i += 1
				f.move()
				screen.blit(f.image, f.rect)
				pygame.display.flip()
				if(pygame.sprite.collide_rect(f, enemy)):
					hit.play()
					enemy.is_hit("freeze", damage)
					break

		self.update(enemy)

	def update(self, enemy):
		drain_sound = pygame.mixer.Sound('./music/drain_sound.ogg')
		freeze_sound = pygame.mixer.Sound('./music/freeze.ogg')
		if(self.state == "drain"):
			self.currentHealth -= 5
			if(enemy.currentHealth < 150):
				enemy.currentHealth += 5

				if(enemy.currentHealth >= 150):
					enemy.currentHealth = 150

			if(self.drain < 3):
				drain_sound.play()
				self.drain += 1
			else:
				self.state = "normal"

		
		if(self.MP <= 0):
			self.recharge = 1
		
		if(self.recharge == 1):
			self.MP += 25
			if(self.MP >= 100):
				self.MP = 100
				self.recharge = 0
		
		if(self.state == "frozen"):
			if(self.frozen < 1):
				freeze_sound.play()
				self.frozen += 1
			else:
				self.state = "normal"
		
				
	def tick(self):
		if(self.idle == 0):
			self.rect = self.rect.move(0, 5)
			self.idle  = 1
		elif(self.idle == 1):
			self.rect = self.rect.move(0, -5)
			self.idle = 2
		elif(self.idle == 2):
			self.rect = self.rect.move(0, -5)
			self.idle = 3
		elif(self.idle == 3):
			self.rect = self.rect.move(0, 5)
			self.idle = 0

				
class Fire(pygame.sprite.Sprite):
	def __init__(self, player, gs = None):
		self.gs = gs
		self.health = 100
		self.currentHealth = 100
		self.MP = 0
		self.Attack = 1.7
		self.Defense = 1.5
		self.state = "normal"
		self.player = player
		self.frozen = 0
		self.drain = 0
		self.idle = 0
		self.recharge = 0

		if(self.player == 0):
			self.image = pygame.image.load('fire_back.png')
			self.rect = self.image.get_rect()
			self.rect.x = 200
			self.rect.y = 177
		else:
			self.image = pygame.image.load('fire_front.png')
			self.rect = self.image.get_rect()
			self.rect.x = 376
			self.rect.y = 177
		
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)

	def move(self, direction, enemy):
		if(self.state != "frozen"):
			if(self.player == 0):
				if((direction == "left") and (self.rect.x > 100)):
					self.rect = self.rect.move(-100, 0)
				elif((direction == "right") and (self.rect.x < 300)):
					self.rect = self.rect.move(100, 0)
			else:
				if((direction == "left") and (self.rect.x < 476)):
					self.rect = self.rect.move(100, 0)
				elif((direction == "right") and (self.rect.x > 276)):
					self.rect = self.rect.move(-100, 0)

		self.update(enemy)

	def is_hit(self, attack, damage):
		if((attack == "primary") or (attack == "pyro")):
			self.currentHealth -= (damage - (10 / self.Defense))
		elif(attack == "freeze"):
			self.state = "frozen"
			self.frozen = 0
		elif(attack == "giga"):
			self.state = "drain"
			self.drain = 0

	def update(self, enemy):
		drain_sound = pygame.mixer.Sound('./music/drain_sound.ogg')
		freeze_sound = pygame.mixer.Sound('./music/freeze.ogg')
		if(self.state == "drain"):
			self.currentHealth -= 5
			if(enemy.currentHealth < 150):
				enemy.currentHealth += 5

				if(enemy.currentHealth >= 150):
					enemy.currentHealth = 150

			if(self.drain < 3):
				drain_sound.play()
				self.drain += 1
			else:
				self.state = "normal"

		
		if(self.MP <= 0):
			self.recharge = 1
		
		if(self.recharge == 1):
			self.MP += 10
			if(self.MP >= 100):
				self.MP = 100
				self.recharge = 0
		
		if(self.state == "frozen"):
			if(self.frozen < 1):
				freeze_sound.play()
				self.frozen += 1
			else:
				self.state = "normal"

	def primary(self, enemy, screen):
		if(self.state != "frozen"):
			cast = pygame.mixer.Sound('./music/fireball.ogg')
			hit = pygame.mixer.Sound('./music/fire_impact.ogg')
			cast.play()
			fb = fireball(self.player, self.rect.centerx, self.rect.centery, self.gs)
			base = 15
			damage = (base * self.Attack)
			i = 0
			while(i < 2):
				i += 1
				fb.move()
				screen.blit(fb.image, fb.rect)
				pygame.display.flip()
				if(pygame.sprite.collide_rect(fb, enemy)):
					hit.play()
					enemy.is_hit("primary", damage)
					break

		self.update(enemy)

	def ultimate(self, enemy, screen):
		if((self.MP >= 100) and (self.state != "freeze")):
			cast = pygame.mixer.Sound('./music/fireball.ogg')
			hit = pygame.mixer.Sound('./music/fire_impact.ogg')
			cast.play()
			self.MP -= 100
			pb = pyro(self.player, self.rect.centerx, self.rect.centery, self.gs)
			base = 30
			damage = (base * self.Attack)
			i = 0
			while(i < 2):
				i += 1
				pb.move()
				screen.blit(pb.image, pb.rect)
				pygame.display.flip()
				if(pygame.sprite.collide_rect(pb, enemy)):
					hit.play()
					enemy.is_hit("pyro", damage)
					break

		self.update(enemy)
				
	def tick(self):
		if(self.idle == 0):
			self.rect = self.rect.move(0, 5)
			self.idle  = 1
		elif(self.idle == 1):
			self.rect = self.rect.move(0, -5)
			self.idle = 2
		elif(self.idle == 2):
			self.rect = self.rect.move(0, -5)
			self.idle = 3
		elif(self.idle == 3):
			self.rect = self.rect.move(0, 5)
			self.idle = 0


class Grass(pygame.sprite.Sprite):
	def __init__(self, player, gs = None):
		self.gs = gs
		self.health = 150
		self.currentHealth = 150
		self.MP = 0
		self.Attack = 1
		self.Defense = 1
		self.state = "normal"
		self.player = player
		self.frozen = 0
		self.drain = 0
		self.idle = 0
		self.recharge = 0

		if(self.player == 0):
			self.image = pygame.image.load('grass_back.png')
			self.rect = self.image.get_rect()
			self.rect.x = 200
			self.rect.y = 177
		else:
			self.image = pygame.image.load('grass_front.png')
			self.rect = self.image.get_rect()
			self.rect.x = 376
			self.rect.y = 177
		
		color = self.image.get_at((0,0))
		self.image.set_colorkey(color)

	def move(self, direction, enemy):
		if(self.state != "frozen"):
			if(self.player == 0):
				if((direction == "left") and (self.rect.x > 100)):
					self.rect = self.rect.move(-100, 0)
				elif((direction == "right") and (self.rect.x < 300)):
					self.rect = self.rect.move(100, 0)
			else:
				if((direction == "left") and (self.rect.x < 476)):
					self.rect = self.rect.move(100, 0)
				elif((direction == "right") and (self.rect.x > 276)):
					self.rect = self.rect.move(-100, 0)

		self.update(enemy)

	def is_hit(self, attack, damage):
		if((attack == "primary") or (attack == "pyro")):
			self.currentHealth -= (damage - (10 / self.Defense))
		elif(attack == "freeze"):
			self.state = "frozen"
			self.frozen = 0
		elif(attack == "giga"):
			self.state = "drain"
			self.drain = 0

	def primary(self, enemy, screen):
		if(self.state != "frozen"):
			cast = pygame.mixer.Sound('./music/whip.ogg')
			hit = pygame.mixer.Sound('./music/whip_impact.ogg')
			cast.play()
			whip = vine(self.player, self.rect.centerx, self.rect.centery, self.gs)
			base = 15
			damage = (base * self.Attack)
			i = 0
			while(i < 2):
				i += 1
				whip.move()
				screen.blit(whip.image, whip.rect)
				pygame.display.flip()
				if(pygame.sprite.collide_rect(whip, enemy)):
					hit.play()
					enemy.is_hit("primary", damage)
					break
		self.update(enemy)

	def ultimate(self, enemy, screen):
		if((self.MP >= 100) and (self.state != "freeze")):
			cast = pygame.mixer.Sound('./music/giga.ogg')
			hit = pygame.mixer.Sound('./music/giga_hit.ogg')
			cast.play()
			self.MP -= 100
			gd = giga(self.player, self.rect.centerx, self.rect.centery, self.gs)
			base = 0
			damage = (base * self.Attack)
			i = 0
			while(i < 2):
				i += 1
				gd.move()
				screen.blit(gd.image, gd.rect)
				pygame.display.flip()
				if(pygame.sprite.collide_rect(gd, enemy)):
					hit.play()
					enemy.is_hit("giga", damage)
					break
		self.update(enemy)

	def update(self, enemy):
		drain_sound = pygame.mixer.Sound('./music/drain_sound.ogg')
		freeze_sound = pygame.mixer.Sound('./music/freeze.ogg')
		if(self.state == "drain"):
			self.currentHealth -= 5
			if(enemy.currentHealth < 150):
				enemy.currentHealth += 5

				if(enemy.currentHealth >= 150):
					enemy.currentHealth = 150

			if(self.drain < 3):
				drain_sound.play()
				self.drain += 1
			else:
				self.state = "normal"

		
		if(self.MP <= 0):
			self.recharge = 1
		
		if(self.recharge == 1):
			self.MP += 25
			if(self.MP >= 100):
				self.MP = 100
				self.recharge = 0
		
		if(self.state == "frozen"):
			if(self.frozen < 1):
				freeze_sound.play()
				self.frozen += 1
			else:
				self.state = "normal"
				
	def tick(self):
		if(self.idle == 0):
			self.rect = self.rect.move(0, 5)
			self.idle  = 1
		elif(self.idle == 1):
			self.rect = self.rect.move(0, -5)
			self.idle = 2
		elif(self.idle == 2):
			self.rect = self.rect.move(0, -5)
			self.idle = 3
		elif(self.idle == 3):
			self.rect = self.rect.move(0, 5)
			self.idle = 0
