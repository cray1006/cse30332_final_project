# Christopher Ray & Dinh Do
# Creature Battler - Final Project
# CSE 30332
# 7 May 2015

# server.py
#class definition for game server

import sys
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue


class serverProtocol(Protocol):	#class definition for server protocol
	def __init__(self, F):	#defining init
		self.F = F
		self.id = None
		self.state = 'start'

	def connectionMade(self):	#defining connectMade handler
		self.id = self.F.count	#creating id for connected player
		self.transport.write(str(self.F.count))	#sending ID information to player	
		if self.F.count == 1:
			self.F.players[0].state = 'connected'
			self.state = 'connected'
			
		
	def dataReceived(self, data):	#defining dataReceived handler
		print "Data received from " + str(self.id) + ": " + data
		if self.state == 'battle':
			# send opponent's move to other player
			if self.id == 0:
				self.F.players[1].transport.write(data)
			else:
				self.F.players[0].transport.write(data)

		elif self.state == 'connected':
			# send the opponent's creature type to other player
			if data == "Fire" or data == "Water" or data == "Grass":
				
				if self.id == 0:
					self.F.players[1].transport.write(data)
				else:
					self.F.players[0].transport.write(data)
				self.state = 'battle'
			

	def connectionLost(self, reason):
		# if connection is lost, notify other player
		if self.id == 0 and self.F.players[1] is not None:
			self.F.players[1].transport.write('quit')
		elif self.F.players[0] is not None:
			self.F.players[0].transport.write('quit')			

		self.F.players[self.id] = None
		self.F.count = -1
		
		

class serverFactory(Factory):	#defining server factory
	def __init__(self):
		self.players = [None] * 2	#initializing player array
		self.count = -1
		
	def buildProtocol(self, addr):	#building protocol
		s = serverProtocol(self)
		self.count += 1
		self.players[self.count] = s
		return s


if __name__ == '__main__':
# Listen at port 40020, for command connection
	sF = serverFactory()
	port = reactor.listenTCP(40020,sF)
	reactor.run()
	sys.exit()

