#!/usr/bin/env python
import sys
import random
import mylogging
from gitagent.msg import *
import time

class Core:
	def __init__(self, willingness, ID):
		#willingness - [theta, delta]
		self.willingness = willingness

		#start always in idle
		self.state = 0

		#agent name (unique -- it has to uniquely point to some agent)
		self.ID = ID

		#This could be an array, in which each element represents health over some dimension
		self.health = self.check_health()

		print self.willingness
		print self.state

	#This function can perform some 'health' analysis on the state of different parts of the system.
	def check_health(self):
		return True

	def create_message(self, raw_content):
		message = Protocol_Msg()
		message.performative = 'broadcast'
		message.sender = str(self.ID)
		message.rank = 10
		message.receiver = 'all'
		message.language = 'shqip'
		message.ontology = 'shenanigans'
		message.urgency = 'INFO'
		message.content = self.create_msg_content(raw_content)
		message.timestamp = time.strftime('%X', time.gmtime())
		#print message
		return message

	def create_msg_content(self, raw_content):
		content = ''
		for x in raw_content:
			content = content + str(x[0]) + '|' 
		return content
