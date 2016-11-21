#!/usr/bin/env python
import sys
import random
import mylogging
from gitagent.msg import *
import time

class Core:
	def __init__(self, willingness, ID, battery, sensors, actuators, motors):
		#willingness - [theta, delta]
		self.willingness = willingness

		#start always in idle
		self.state = 0

		#agent name (unique -- it has to uniquely point to some agent)
		self.ID = ID

		#Battery levels
		self.battery = battery

		#3 arrays which keep the states for sensors, actuators, motors
		self.sensors = sum(sensors)
		self.actuators = sum(actuators)
		self.motors = sum(motors)
		self.sensmot = sum([self.sensors, self.actuators, self.motors])

		#This is the minimum value for the battery levels in which it could be 
		#considered that the agent works properly
		self.battery_min = 300
		self.sensmot_min = 300

		#This could be an array, in which each element represents health over some dimension
		self.check_health()

		print self.willingness
		print self.state
		print self.battery

	#This function can perform some 'health' analysis on the state of different parts of the system.
	def check_health(self):
		if self.battery <= self.battery_min or self.sensmot <= self.sensmot_min:
			#Levels not acceptable ---> change state to dead
			self.state = 4

	def battery_change(self, change):
		self.battery = self.battery + change
	
	#It might be possible to introduce random issues here, i.e. aggravate the change of 'health'
	def sensory_motor_state_mockup(self):
		self.sensmot = sum([self.sensors, self.actuators, self.motors])

	def create_message(self, raw_content, tipmsg):
		message = Protocol_Msg()
		message.performative = 'broadcast'
		message.sender = str(self.ID)
		message.rank = 10
		message.receiver = 'all'
		message.language = 'shqip'
		message.ontology = 'shenanigans'
		message.urgency = 'INFO'
		message.content = self.create_msg_content(raw_content, tipmsg)
		message.timestamp = time.strftime('%X', time.gmtime())
		#print message
		return message

	def create_msg_content(self, raw_content, tipmsg):
		content = ''
		if tipmsg == 'position':
			for x in raw_content:
				content = content + str(x) + '|'
		else:
			for x in raw_content:
				content = content + str(x[0]) + '|'
		return content
