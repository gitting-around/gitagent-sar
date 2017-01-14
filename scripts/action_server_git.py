#!/usr/bin/env python
import sys
from gitagent.msg import *
from threading import Lock
import random
import roslib
roslib.load_manifest('gitagent')
import rospy
from actionlib import ActionServer
from actionlib.server_goal_handle import ServerGoalHandle
import Queue
import traceback
import time
import threading

class GitActionServer:

    def __init__(self, name, ActionSpec, execute_cb=None, auto_start=True):

        self.execute_callback = execute_cb
        self.goal_callback = None
        self.preempt_callback = None

        # since the internal_goal/preempt_callbacks are invoked from the
        # ActionServer while holding the self.action_server.lock
        # self.lock must always be locked after the action server lock
        # to avoid an inconsistent lock acquisition order
        #self.lock = threading.RLock()

        #self.execute_condition = threading.Condition(self.lock)

        self.current_goal = ServerGoalHandle()
        self.next_goal = ServerGoalHandle()

        #create the action server
        self.action_server = ActionServer(name, ActionSpec, self.get_next_gh, self.internal_preempt_callback, auto_start)

        ## @brief Explicitly start the action server, used it auto_start is set to false
    def start(self):
        self.action_server.start()

    ## @brief Sets the status of the active goal to succeeded
    ## @param  result An optional result to send back to any clients of the goal
    def set_succeeded(self, gh, result=None, text=""):
        if not result:
            result = self.get_default_result()
        gh.set_succeeded(result, text)

    def get_default_result(self):
        return self.action_server.ActionResultType()

    def git_accept_new_goal(self, goal):
        rospy.loginfo("A new goal %s  has been accepted", str(goal.get_goal()))
        goal.set_accepted("This goal has been accepted by the simple action server -- wait for response")

    def set_preempted(self, goal, result=None, text=""):
        if not result:
            result=self.get_default_result();
        rospy.logdebug("Setting the current goal as canceled");
        goal.set_canceled(result, text);

    #If a new goal is received, put the goalhandle in queue
    def get_next_gh(self, goal):
        #self.execute_condition.acquire()

        try:
            rospy.logdebug("A new goal %shas been recieved by the single goal action server", goal.get_goal_id().id)

            rospy.loginfo("A new goal %shas been recieved by the single goal action server", goal.get_goal_id().id)

            if self.execute_callback:
                #Start new thread on execute()
                rospy.loginfo("New thread about to be launched on execute")
                try:
                    t = threading.Thread(target=self.execute_callback, args=(goal,))
                    t.start()
                except:
                    rospy.logerr("Error: unable to start thread")
            else:
                rospy.logerr("DEFINE an execute callback moron")
            #self.execute_condition.release()

        except Exception as e:
            rospy.logerr("SimpleActionServer.internal_goal_callback - exception %s", str(e))
            #self.execute_condition.release()

    def internal_preempt_callback(self):
        pass
