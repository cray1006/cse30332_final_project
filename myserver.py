# Christopher Ray  &  Dinh Do
# Creature Battler - Final Project
# server.py

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue


class serverProtocol(LineReceiver):
	def __init__(self, F):
		self.F = F
		self.id = None
		self.state = 'start'

	def connectionMade(self):
		self.id = len(self.F.players)-1
		self.transport.write(str(len(self.F.players)-1))
		print "Connection #" + str(len(self.F.players))
		if len(self.F.players) > 1:
			self.F.players[0].transport.write('Opponent Connected')
			self.F.players[0].state = 'connected'
			self.state = 'connected'
			


	def switch(self):
		self.transport.write('switch')

	def dataReceived(self, data):

		if self.state == 'battle':
			if data == 'T':
			# Switch turns, notify other player
				print data
				print "Server ID = " + str(self.id)
				if self.id == 0:
					self.F.players[1].switch()
				else:
					self.F.players[0].switch()
		elif self.state == 'connected':
			if data == "Fire" or data == "Water" or data == "Grass":
				print data
				if self.id == 0:
					self.F.players[1].transport.write(data)
				else:
					self.F.players[0].transport.write(data)
				self.state = 'battle'
			

	def connectionLost(self, reason):
		# if connection is lost, notify other player
		if self.id == 0:
			self.F.players[1].transport.write('quit')
		else:
			self.F.players[0].transport.write('quit')


class serverFactory(Factory):
	def __init__(self):
		self.players = []
		
	def buildProtocol(self, addr):
		s = serverProtocol(self)
		self.players.append(s)
		return s


# Listen at port 40020, for command connection
sF = serverFactory()
reactor.listenTCP(40020,sF)
reactor.run()
