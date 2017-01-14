#!/usr/bin/env python
import sys
from gitagent.msg import *
from threading import Lock
import random
import roslib
roslib.load_manifest('gitagent')
import rospy
import actionlib
import time
import traceback
import threading

class Client:
    def __init__(self):
        rospy.init_node('client2', anonymous=True)
        self.client = actionlib.SimpleActionClient('server', doMeFavorAction)

    def done(self, state, result):
        print 'stuff'
        #print result.act_outcome

    def active(self):
        print 'Goal just sent!\n'

    def feedback(self, feedback):
        print 'Feedback: %f\n' % feedback.time2finish

    def call_action_server(self, goal):
        print 'I am here'
        self.client.wait_for_server()
        print 'I am requesting a favor'

        formatted_goal = doMeFavorGoal(performative='plead4goal', sender='2', rank=10, receiver='2', language='shqip', ontology='laraska', urgency='none', content=goal, timestamp=time.strftime('%X', time.gmtime()))

        print str(formatted_goal)

        self.client.send_goal(formatted_goal, self.done, self.active, self.feedback)

if __name__ == '__main__':

    try:
        client = Client()
        print 'Client up and running'
        #client.call_action_server('stuff')
        client.call_action_server('crap')
        rospy.spin()
    except rospy.ROSInterruptException:
        traceback.print_exc()
        raise
    except (AttributeError, TypeError, ValueError, NameError):
        traceback.print_exc()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc()
        raise
