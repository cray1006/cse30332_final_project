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
			self.playersConnected()
			

	def playersConnected(self):
		for i in self.F.players:
			i.transport.write("Opponent Connected")
			return

			

	


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
