#!/usr/bin/env python
import sys
from gitagent.msg import *
from threading import Lock
import random
import roslib
roslib.load_manifest('gitagent')
import rospy
import actionlib
import Queue
import queue_action_server
import action_server_git
import traceback
import time
import threading

class Server:
    def __init__(self):
        rospy.init_node('server', anonymous=True)
        self.queueGoalHandles = Queue.Queue()
        #self.server = queue_action_server.SimpleActionServer('server', doMeFavorAction, self.queueGoalHandles, self.execute, False)
        #self.server = actionlib.SimpleActionServer('server', doMeFavorAction, self.execute2, False)
        self.server = action_server_git.GitActionServer('server', doMeFavorAction, self.execute, False)
        self.server.start()
        self.keep_track_threads = []
        self.lock = Lock()

    #Needs to be used similarly as handle_serve, in order to block threads respectively.
    def execute(self, goalhandle):
        print 'I got a request'

        # Add tag to identify current thread
        # Task status: -1 ~ FAIL, 0 ~ PENDING, 1 ~ SUCCESS, 10 ~ no thread active
        index = -1

        feedback = doMeFavorFeedback()
        result = doMeFavorResult()

        self.lock.acquire()
        goal = goalhandle.get_goal()
        print 'extracted goal content: ' + str(goal.sender)

        #Check if I have already gotten smth from this sender, in that case it's already in the queue, just change task_status to 0
        try:
            index = next(index for (index, d) in enumerate(self.keep_track_threads) if d['senderId'] == int(goal.sender))
            self.keep_track_threads[index]['task_status'] = 0
            print 'Guy currently in list: %d' % index
        except StopIteration:
            print 'A new guy in here'
            self.keep_track_threads.append({'senderId':int(goal.sender), 'task_status':0})
            # It is assumed that the senderId is unique, that is the server cannot get 2 a second task from an agent, without returning with the first.
            # {senderID:task_status}
            #self.keep_track_threads.append({data.sender:0})
            index = len(self.keep_track_threads) - 1
        print self.keep_track_threads
        # Put task in a queue, make thread wait until task status is set to success/fail -- might be possible to add a timeout for that
        self.queueGoalHandles.put(goalhandle)
        self.lock.release()
        print 'Current goal status: %s\n' % goalhandle.get_goal_status()
        while self.keep_track_threads[index]['task_status'] == 0:
            print 'Current goal status: %s\n' % goalhandle.get_goal_status()
            rospy.sleep(1)
            # During execution some feedback might be available
        #self.server.publish_result(0,49)
        print 'Thread: ' + str(self.keep_track_threads[index]['task_status']) + ' has returned'
        result.act_outcome = self.keep_track_threads[index]['task_status']
        self.server.set_succeeded(goalhandle, result)
        print 'Current goal status: %s\n' % goalhandle.get_goal_status()
        self.lock.acquire()
        self.keep_track_threads[index]['task_status'] = 10
        self.lock.release()
        print self.keep_track_threads
        print result

    def execute2(self, data):
        self.queueGoals.put(data.content)
        print 'Execute ' + str(data.content)
        # Do lots of awesome groundbreaking robot stuff here

        feedback = doMeFavorFeedback()
        result = doMeFavorResult()

        percent = 0
        while percent < 100.0:
            print 'percent ' + str(percent)
            percent = percent + 10.0
            feedback.time2finish = percent
            self.server.publish_feedback(feedback)

        result.act_outcome = 1
        print '[action] ' + str(result)
        self.server.set_succeeded(result)

    def theLoop(self):
        print 'Sever started'
        while not rospy.is_shutdown():
            #print 'Waiting for goal...'
            #Non-blocking
            try:
                item = self.queueGoalHandles.get(False)
                print item

                #Assuming we always accept the goal - set this goal as the current goal
                print 'Current goal status: %s\n' % item.get_goal_status()
                self.server.git_accept_new_goal(item)
                print 'Current goal status: %s\n' % item.get_goal_status()

                i = 0
                while i <= 10:
                    print i
                    i = i + 1
                    time.sleep(1)
                index = next(index for (index, d) in enumerate(self.keep_track_threads) if d['senderId'] == int(item.get_goal().sender))
                self.keep_track_threads[index]['task_status'] = 1
                #self.keep_track_threads[0]['task_status'] = 1
                print self.keep_track_threads

            except Queue.Empty:
                #print 'empty queue'
                pass

if __name__ == '__main__':

    try:
        serve = Server()
        serve.theLoop()
    except rospy.ROSInterruptException:
        traceback.print_exc()
    except (AttributeError, TypeError, ValueError, NameError):
        traceback.print_exc()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc()
