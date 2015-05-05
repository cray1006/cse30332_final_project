# Christopher Ray  &  Dinh Do
# Creature Battler - Final Project
# server.py

import sys
from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.defer import Deferred

#2 connections:  P1 (port 40020) and P2 (40021)

queue = DeferredQueue()
p1Connected = 0
p2Connected = 0
p1Trans = None
p2Trans = None

def send_p1(data):
	p1Trans.transport.write(data)

def send_p2(data):
	p2Trans.transport.write(data)


class P1(Protocol):
	def __init__(self):
		global p1Connected
		global p1Trans = self
		p1Connected = 1

	def connectionMade(self):
		if(p1Connected and p2Connected):
			self.transport.write("ready")
		else:
			self.transport.write("wait")
			i = 0
			while(not(p1Connected and p2Connected)):
				i += 1
			self.transport.write("ready")			

	def dataReceived(self, data):
		if(p2Trans == None):
			i = 0
			while(p2Trans == None):
				i += 1
			queue.put(data)
			d = queue.get()
			d.addCallback(send_p2)
		else:
			queue.put(data)
			d = queue.get()
			d.addCallback(send_p2)

	def connectionLost(self, reason):
		print "Player 1 connection lost:  " + str(reason)

	def connectionFailed(self, reason):
		print "Player 1 connection failed:  " + str(reason)

			
class P1Factory(Factory):
	def buildProtocol(self, addr):
		return P1()


class P2(Protocol):
	def __init__(self):
		global p2Connected
		global p2Trans = self
		p2Connected = 1

	def connectionMade(self):
		if(p1Connected and p2Connected):
			self.transport.write("ready")
		else:
			self.transport.write("wait")
			i = 0
			while(not(p1Connected and p2Connected)):
				i += 1
			self.transport.write("ready")			

	def dataReceived(self, data):
		if(p1Trans == None):
			i = 0
			while(p1Trans == None):
				i += 1
			queue.put(data)
			d = queue.get()
			d.addCallback(send_p1)
		else:
			queue.put(data)
			d = queue.get()
			d.addCallback(send_p1)

	def connectionLost(self, reason):
		print "Player 2 connection lost:  " + str(reason)

	def connectionFailed(self, reason):
		print "Player 2 connection failed:  " + str(reason)

			
class P2Factory(Factory):
	def buildProtocol(self, addr):
		return P2()


# Listen at port 40020, for command connection
p1 = P1Factory()
p2 = P2Factory()
reactor.listenTCP(40020,p1)
reactor.listenTCP(40021,p2)
reactor.run()
