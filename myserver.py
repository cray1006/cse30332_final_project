# Christopher Ray  &  Dinh Do
# Creature Battler - Final Project
# server.py

import sys
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue


class serverProtocol(Protocol):
	def __init__(self, F):
		self.F = F
		self.id = None
		self.state = 'start'

	def connectionMade(self):
		self.id = self.F.count
		self.transport.write(str(self.F.count))
		if self.F.count == 1:
			self.F.players[0].state = 'connected'
			self.state = 'connected'
			
		
	def dataReceived(self, data):
		print "Data received from " + str(self.id) + ": " + data
		if self.state == 'battle':
			if self.id == 0:
				self.F.players[1].transport.write(data)
			else:
				self.F.players[0].transport.write(data)

		elif self.state == 'connected':
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
		
		

class serverFactory(Factory):
	def __init__(self):
		self.players = [None] * 2
		self.count = -1
		
	def buildProtocol(self, addr):
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

