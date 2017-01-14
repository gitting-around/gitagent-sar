#!/usr/bin/env python
import sys
from gitagent.msg import *
import roslib
roslib.load_manifest('gitagent')
import rospy
import actionlib
import traceback
import time
import threading

class Client:
    def __init__(self):
        rospy.init_node('client', anonymous=True)
        self.client = actionlib.SimpleActionClient('server', doMeFavorAction)

    def done(self, state, result):
        print 'This is the outcome: ' + str(result.act_outcome)
        #print result.act_outcome

    def active(self):
        print 'Goal just sent!\n'

    def feedback(self, feedback):
        print 'Feedback: %f\n' % feedback.time2finish

    def call_action_server(self, goal):
        print 'I am here'
        self.client.wait_for_server()
        print 'I am requesting a favor'

        formatted_goal = doMeFavorGoal(performative='plead4goal', sender='1', rank=10, receiver='2', language='shqip', ontology='laraska', urgency='none', content=goal, timestamp=time.strftime('%X', time.gmtime()))

        print str(formatted_goal)

        #self.client.send_goal(formatted_goal, self.done, self.active, self.feedback)
        self.client.send_goal(formatted_goal)
        print 'goal state %s\n' % self.client.get_state()
        self.client.wait_for_result()
        print 'goal state %s\n' % self.client.get_state()
        print 'Result: ' + str(self.client.get_result())


if __name__ == '__main__':

    try:
        client = Client()
        print 'Client up and running'
        client.call_action_server('stuff')
        #client.call_action_server('crap')
        while True:
            print 'hello'
            time.sleep(2)
    except rospy.ROSInterruptException:
        traceback.print_exc()
        raise
    except (AttributeError, TypeError, ValueError, NameError):
        traceback.print_exc()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc()
        raise
