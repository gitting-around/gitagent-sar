#!/usr/bin/env python
#no license, for the love of god
import sys
import rospy
import time
from gitagent.msg import *

class PUnit:
	me = -1
	known_people = []
	protMsg = Protocol_Msg()

	def __init__(self):

		rospy.init_node('msg_punit', anonymous=True)
		agent_id = rospy.get_param('msg_punit/myID')
		print agent_id
		self.me = agent_id
		print self.me

		self.filters = []

		self.publish_brain = rospy.Publisher('bcasts_brain', Protocol_Msg, queue_size=200)
		self.publish_env_msg = rospy.Publisher('/environment/msg_topic', Protocol_Msg, queue_size=200)
		rospy.Subscriber('bcasts', Protocol_Msg, self.callback_brain)
		rospy.Subscriber('/environment/msg_topic', Protocol_Msg, self.callback_env_msg)

	def callback_brain(self, data):
		rospy.loginfo(rospy.get_caller_id() + " Callback-from-brain %s, %s", data.sender, data.content)
		print data.content+'__'+str(self.me)

		if not rospy.is_shutdown():
			self.publish_env_msg.publish(data)
			print 'published to environment'
		else:
			print 'rospy is shutdown'

	def callback_env_msg(self, data):
		rospy.loginfo(rospy.get_caller_id() + " Callback-from-env_msg %s, %s", data.sender, data.content)
		if not int(data.sender) == self.me:
			new = self.new_people(int(data.sender), data.content)
			if not rospy.is_shutdown() and new:
				self.publish_brain.publish(data)
				print 'PUBLISHED new individual'

		else:
			print 'Ignore messages send by self'

	def new_people(self, idi, content):
		guy_id_srv = [idi]
		guy_id_srv.append([int(x) for x in filter(None, content.split('|'))])
		new = True
		for x in self.known_people:
			if x[0] == idi:
				new = False
		if new:
			self.known_people.append(guy_id_srv)
		print 'KNOWN guys: ', self.known_people
		return new

if __name__ == '__main__':

	stderr_file = '/home/mfi01/.ros/RESULT/error_msg_punit'
	f = open(stderr_file, 'w+')
	orig_stderr = sys.stderr
	sys.stderr = f

	stdout_file = '/home/mfi01/.ros/RESULT/stdout_msg_unit'
	s = open(stdout_file, 'w+')
	orig_stdout = sys.stdout
	#sys.stdout = s

	try:
		punit = PUnit()
		rospy.spin()
	finally:
		sys.stderr = orig_stderr
		f.close()
		sys.stdout = orig_stdout
		s.close()
