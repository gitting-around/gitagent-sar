#!/usr/bin/env python
# Parent class of agent, implementing the core parts of the theoretical concept
# Framework v1.0
import sys
import time
import math
import mylogging
import core_aboutme
import knowledge
import simulation
from gitagent.msg import *
from gitagent.srv import *
from threading import Lock
import random
import timeit
import roslib
import pdb
import numpy as np
import matplotlib.pyplot as plt

roslib.load_manifest('gitagent')
import rospy
import actionlib
import action_server_git
import Queue


class Agent0:
    def __init__(self, ID, conf, services, willingness, simulation, popSize, provaNr, depend_nr, battery, sensors,
                 actuators, motors, static, memory):
        # print conf
        rospy.loginfo('Agent conf: %s\n', str(conf))

        # use simulation functions
        self.simulation = simulation
        # logging class
        self.log = mylogging.Logging(popSize, provaNr, ID, willingness[1], depend_nr)
        self.begin = 0
        self.end = 0

        self.static = static

        # Enumerated lists for each #########
        self.languages = conf['languages']
        self.protocols = conf['protocols']
        self.abilities = conf['abilities']
        self.resources = conf['resources']
        # self.services = services
        self.services = []
        for x in self.abilities:
            self.services.append(x)
        rospy.loginfo('Agent services: %s', self.services)
        rospy.loginfo('Agent resources: %s', self.resources)
        ####################################

        # Variables manipulated by multiple threads ###
        self.adaptive_state = []
        ##############################################

        ## Contains info specific to the internal state of the agent such as: state, health attributes etc.
        self.mycore = core_aboutme.Core(willingness, ID, conf['battery'], sensors, actuators, motors, memory)

        self.log.write_log_file(self.log.stdout_log, 'init gitagent ' + str(self.mycore.sensmot) + '\n')
        ## Contains mixed info ############################################################################
        self.myknowledge = knowledge.Knowledge0()

        ##Wait until gotten initial position from the environment node
        self.init_sub = rospy.Subscriber('/environment/init_locs', Init_Loc, self.callback_init_loc_msg)
        self.fires_sub = rospy.Subscriber('/environment/fires', Fires_Info, self.callback_fires_env)
        rospy.Subscriber('/environment/fires_pb', Fires_Info, self.callback_fires_msg)
        self.publish_loc = rospy.Publisher('/environment/track_locs', Track_Loc, queue_size=200)
        self.publish_fires = rospy.Publisher('/environment/fires_pb', Fires_Info, queue_size=200)

        rospy.Subscriber('/environment/fbase', Fire_Base, self.callback_fb_msg)
        rospy.Subscriber('/environment/abase', Ambulance_Base, self.callback_ab_msg)

        while True:
            if not self.myknowledge.position2D == [-1, -1] and self.simulation.fires.size:
                # Wait until I get initial position
                break

        # They will contain arrays of topic's names ###
        self.inputs = conf['sensors']
        # print self.inputs
        self.publish_bcast = []
        self.outputs = conf['actuators']
        self.motors = conf['motors']
        # print self.outputs
        self.init_inputs(self.inputs)
        self.init_outputs(self.outputs)
        self.init_serve(ID)
        ##############################################
        # print self.inputs, self.outputs, self.motors, self.languages, self.protocols, conf['battery']
        ############ ACTION SERVER ###################################################################
        self.log.write_log_file(self.log.stdout_log, 'rospy name ' + str(rospy.get_name()) + '\n')
        self.server = action_server_git.GitActionServer(rospy.get_name(), doMeFavorAction, self.execute_git, False)
        self.server.start()
        self.keep_track_threads = []
        self.queueGoalHandles = Queue.Queue()
        ##############################
        for x in range(1, 10):
            self.publish2sensormotor(self.services)

        rospy.loginfo('Agent with id: %d, delta: %f, theta: %f, thetaLOW: %f', ID, willingness[1], willingness[0],
                      self.mycore.LOW)

        self.reason = 'Default: None'
        time.sleep(10)
        self.simulation_end = 0.0
        self.start = time.time()

    ##############################################################################################
    def callback_fb_msg(self, data):
        self.simulation.fbase = [data.id, data.xpos, data.ypos]
        print self.simulation.fbase

    def callback_ab_msg(self, data):
        self.simulation.abase = [data.id, data.xpos, data.ypos]
        print self.simulation.abase

    def callback_fires_env(self, data):
        try:
            self.myknowledge.lock_cb.acquire()
            self.simulation.callback_env += 1
            # if ((data.xpos - self.myknowledge.position2D[0]) ** 2 + (data.ypos - self.myknowledge.position2D[1]) ** 2) < self.simulation.visible_distance**2:
            if self.simulation.fires.size:
                self.simulation.fires[0] = data.id
                self.simulation.fires[1] = data.xpos
                self.simulation.fires[2] = data.ypos
                self.simulation.fires[3] = data.intensity
                self.simulation.fires[4] = data.victims
                self.simulation.fires[5] = data.status
                if np.sum(self.simulation.fires[3]) == -1000 * 40 and np.sum(self.simulation.fires[4]) == -1000 * 40:
                    if not self.simulation.all_out:
                        self.simulation.all_out = True
            else:
                self.simulation.fires = np.zeros((7, 40))
                self.simulation.fires[0] = data.id
                self.simulation.fires[1] = data.xpos
                self.simulation.fires[2] = data.ypos
                self.simulation.fires[3] = data.intensity
                self.simulation.fires[4] = data.victims
                self.simulation.fires[5] = data.status
                self.simulation.fires[6] = [0 for x in range(0, len(data.id))]
            msg = '[env ' + str(self.simulation.callback_env) + ']  callback_fires_env: \n' + str(
                np.array(self.simulation.fires))
            # msg = '[fsm ' + str(self.simulation.fsm) + ']  callback_fires_env: \n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            # rospy.loginfo(msg)
            # rospy.loginfo(msg)
            self.myknowledge.lock_cb.release()
        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))
            pass

    def callback_fires_msg(self, data):
        try:
            self.myknowledge.lock_cb.acquire()
            self.simulation.callback_msg += 1
            # check if I already know about this
            # Doesn't handle new fires, it just makes visible those which are too far away
            # msg = '[fsm ' + str(self.simulation.fsm) + ']  callback_fires_msg: \n' + str(np.array(self.simulation.fires)) + ' tip: ' + str(type(self.simulation.fires[0]))
            # self.log.write_log_file(self.log.stdout_log, msg)
            # rospy.loginfo(msg)
            # msg = '\n[#msg ' + str(self.simulation.callback_msg) + ']  callback_fires_msg: \n' + str(np.array(self.simulation.fires))
            msg = '\n[#msg ' + str(self.simulation.callback_msg) + '] callback_fires_msg, data: ' + str(np.array(data))
            # rospy.loginfo(msg)
            for i, x in enumerate(data.id):
                # msg = '[fsm ' + str(self.simulation.fsm) + '] callback_fires_msg: \n' + ' tip: ' + str(type(self.simulation.fires[3])) + ', ' + str(type(data.intensity[i])) + ', ' + str(self.simulation.fires[3])
                # self.log.write_log_file(self.log.stdout_log, msg)
                # rospy.loginfo(msg)
                # msg = '[msg ' + str(self.simulation.callback_msg) + ']  data id: %f, %f \n' % (i, x)
                # self.log.write_log_file(self.log.stdout_log, msg)
                # rospy.loginfo(msg)
                for j, a in enumerate(self.simulation.fires[0]):
                    # msg = '[msg ' + str(self.simulation.callback_msg) + ']  sim fires: %f, %s \n' % (j, str(a))
                    # self.log.write_log_file(self.log.stdout_log, msg)
                    # rospy.loginfo(msg)
                    if a == x:
                        # msg += '[msg ' + str(self.simulation.callback_msg) + ']  a[0]: %f, x: %f \n' % (a,x)
                        # self.log.write_log_file(self.log.stdout_log, msg)
                        # rospy.loginfo(msg)
                        if self.simulation.fires[3][j] > data.intensity[i]:
                            self.simulation.fires[3][j] = data.intensity[i]
                            self.simulation.fires[5][j] = data.status[i]

                        if self.simulation.fires[4][j] > data.victims[i]:
                            self.simulation.fires[4][j] = data.victims[i]

                        self.simulation.fires[6][j] = 1
                        msg += '\n Relevant update'
                        # msg = '[msg ' + str(self.simulation.callback_msg) + '] self.simulation.fires[6]: \n' + str(self.simulation.fires[6][j])
                        # rospy.loginfo(msg)
                        break
                        # self.simulation.fires[3][i] = data.intensity[i]
                        # self.simulation.fires[4][i] = data.victims[i]
                        # self.simulation.fires[5][i] = data.status[i]
                        # self.simulation.fires[6][i] = 1
            msg += '\n[&msg ' + str(self.simulation.callback_msg) + ']  callback_fires_msg: \n' + str(
                np.array(self.simulation.fires[6]))
            # self.log.write_log_file(self.log.stdout_log, msg)
            # rospy.loginfo(msg)
            # rospy.loginfo(msg)
            self.myknowledge.lock_cb.release()
        except:
            rospy.loginfo(msg)
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))

    def callback_init_loc_msg(self, data):
        if self.myknowledge.position2D == [-1, -1]:
            msg = '[fsm ' + str(self.simulation.fsm) + ']  callback_init_loc_msg: \n' + str(np.array(data))
            # self.log.write_log_file(self.log.stdout_log, msg)
            for i, x in enumerate(data.ids):
                if x == self.mycore.ID:
                    self.myknowledge.position2D = [data.xpos[i], data.ypos[i]]
                    print x
            msg += '[fsm ' + str(self.simulation.fsm) + ']  callback_init_loc_msg: \n' + str(
                self.myknowledge.position2D)
            rospy.loginfo(msg)
            self.init_sub.unregister()

    def my_hook(self):
        print self.reason
        msg = '[fsm ' + str(self.simulation.fsm) + '] ' + self.reason + '\n'
        msg += '[fsm ' + str(self.simulation.fsm) + '] ' + str(self.begin) + ' ' + str(self.end) + '\n'

        # self.log.write_log_file(self.log.stdout_log, msg)
        rospy.loginfo(msg)

    def fsm(self):
        while not rospy.is_shutdown():
            # Simulation stopping criterion
            # if sum(self.simulation.generated_tasks) + 1 > self.simulation.STOP:

            # Stop the simulation when all fires and victims are rescued
            if self.simulation.all_out or (time.time() - self.start) > 600:
                # if (time.time() - self.start) > 120:
                # pdb.set_trace()
                msg = '[fsm %d] Simulation finished. Number of self generated tasks: %d\n' % (
                    self.simulation.fsm, sum(self.simulation.no_self_tasks_attempted))
                # self.log.write_log_file(self.log.stdout_log, msg)

                # this is to check why nB and task attempted is a different number

                if self.mycore.state == 2 and not self.myknowledge.service_id == -1 and not self.myknowledge.iteration == -1:
                    self.simulation.no_tasks_attempted[0] -= 1
                    if int(self.myknowledge.service['senderID'] == self.mycore.ID):
                        self.simulation.no_self_tasks_attempted[0] -= 1

                msg += "\nsimulation has reached END, all fires out, all victims saved."
                rospy.loginfo(msg)
                # Send kill signal to msgPUnit
                self.publish_bcast[0].publish(self.mycore.create_message('DIE', 'DIE'))
                self.reason = 'Normal simulation end'
                self.simulation.time_running = time.time() - self.simulation.time_started
                rospy.signal_shutdown(self.reason)
                rospy.on_shutdown(self.my_hook)
                break

            self.change_selfstate_v2()
            # normally you might want to estimate a value that corresponds to the cost of each cycle
            # self.mycore.battery_change(-1)
            self.mycore.sensory_motor_state_mockup()
            self.mycore.check_health()
            # funksioni meposhte mund te ekzekutohet ne paralel --> per tu zhvilluar me tej ne nje moment te dyte
            self.publish2sensormotor(self.services)
            msg = '[fsm ' + str(self.simulation.fsm) + '] current state: ' + str(self.mycore.state) + '\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            ## MOVE ###############################################################################
            '''
            self.myknowledge.position2D = self.simulation.move(self.myknowledge.position2D)
            msg = '[fsm ' + str(self.simulation.fsm) + '] self.myknowledge.position2D: ' + str(
                self.myknowledge.position2D) + '\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            self.publish_bcast[1].publish(self.mycore.create_message(self.myknowledge.position2D, 'position'))
            '''
            ######################################################################################
            # Calculate time of fms_step
            start = time.time()
            self.fsm_step()
            elapsed = time.time() - start
            msg = '[fsm ' + str(self.simulation.fsm) + '] fsm_step exec time: ' + str(
                elapsed) + '\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)
        '''
        temp = np.array(self.simulation.levywalk)
        plt.figure()
        plt.plot(temp[:, [0]], temp[:, [1]])
        plt.savefig('/home/mfi01/catkin_ws/levy_walk_' + str(self.mycore.ID) + '.jpeg')
        if self.simulation.walk:
            temp = np.array(self.simulation.walk)
            plt.figure()
            plt.plot(temp[:, [0]], temp[:, [1]])
            plt.savefig('/home/mfi01/catkin_ws/walk_' + str(self.mycore.ID) + '.jpeg')
        '''

        self.simulation_end = time.time() - self.start
        msg = '[fsm %d] Rospy shutdown. Number of generated tasks: %d\n' % (
            self.simulation.fsm, sum(self.simulation.no_self_tasks_attempted))
        # self.log.write_log_file(self.log.stdout_log, msg)
        rospy.loginfo(msg)
        # Send kill signal to msgPUnit
        self.publish_bcast[0].publish(self.mycore.create_message('DIE', 'DIE'))
        #self.reason = 'Rospy shutdown'
        #rospy.on_shutdown(self.my_hook)
        return

    def fsm_step(self):
        self.simulation.fsm = self.simulation.inc_iterationstamps(self.simulation.fsm)

        msg = '[fsm_INFO] begin: %d, end: %d\n' % (self.begin, self.end)
        rospy.loginfo(msg)

        if self.mycore.state == 0:
            self.idle()
        elif self.mycore.state == 1:
            self.interact()
        elif self.mycore.state == 2:
            self.execute_v2()
        elif self.mycore.state == 3:
            self.regenerate()
        elif self.mycore.state == 4:
            self.dead()

            ### TESTING ACTION SERVER ########################################################################
            ##################################################################################################

    def done(self, state, result):
        self.log.write_log_file(self.log.stdout_log,
                                '[fsm ' + str(self.simulation.fsm) + ']  state ' + str(state) + '\n')
        self.log.write_log_file(self.log.stdout_log,
                                '[fsm ' + str(self.simulation.fsm) + ']  result ' + str(result.act_outcome) + '\n')

    def active(self):
        msg = '[fsm ' + str(self.simulation.fsm) + ']  Goal just sent!\n'
        # self.log.write_log_file(self.log.stdout_log, msg)
        rospy.loginfo(msg)

    def feedback(self, feedback):
        self.log.write_log_file(self.log.stdout_log,
                                '[fsm ' + str(self.simulation.fsm) + ']  Feedback: %f\n' % feedback.time2finish)

    # Non-blocking call to a server -- not now
    def call_action_server(self, goal, agent_id):
        client = actionlib.SimpleActionClient(agent_id, doMeFavorAction)
        client.wait_for_server()
        self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + ']  ' + str(
            rospy.get_name()) + '\nI am requesting a favor\n')
        print rospy.get_name()
        print 'I am requesting a favor'

        goal2str = self.mycore.goal2string(goal)
        self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + ']  ' + goal2str + '\n')

        formatted_goal = doMeFavorGoal(performative='plead4goal', sender=str(self.mycore.ID), rank=10,
                                       receiver=agent_id, language='shqip', ontology='laraska', urgency='none',
                                       content=goal2str, timestamp=time.strftime('%X', time.gmtime()))

        print str(formatted_goal)
        self.log.write_log_file(self.log.stdout_log,
                                '[fsm ' + str(self.simulation.fsm) + ']  ' + str(formatted_goal) + '\n')

        client.send_goal(formatted_goal, self.done, self.active, self.feedback)

        self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + ']  after sending goal\n')

    # Blocking call to a server -- IN USE NOW
    def call_blocking_action_server(self, goal, agent_id, agent_idx):
        self.mycore.amIblocking = True
        # print 'I am in blocking action server'
        # rospy.loginfo('Asking agent with id: %d, for help', agent_id)
        msg = '[fsm ' + str(self.simulation.fsm) + '- blocking call - BEGIN]  ' + str(
            rospy.get_name()) + ' -> I am requesting a favor\n'
        # self.log.write_log_file(self.log.stdout_log, msg)
        rospy.loginfo(msg)
        self.begin += 1
        try:
            client = actionlib.SimpleActionClient(agent_id, doMeFavorAction)
            if not client.wait_for_server(timeout=rospy.Duration(20)):
                msg = '[fsm ' + str(self.simulation.fsm) + '- blocking call - BEGIN]  ' + str(
                    rospy.get_name()) + ' -> Couldn\'t connect to server \n'
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)
                return -1

            # Add sender - in case there is a chain of them
            msg = '[fsm ' + str(self.simulation.fsm) + '- blocking_call]  ' + str(goal) + '\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)
            goal2str = self.mycore.goal2string(goal)
            # self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + ']  ' + goal2str + '\n')

            formatted_goal = doMeFavorGoal(performative='plead4goal', sender=str(self.mycore.ID), rank=10,
                                           receiver=agent_id, language='shqip', ontology='laraska', urgency='none',
                                           content=goal2str, timestamp=time.strftime('%X', time.gmtime()))

            msg = '[fsm ' + str(self.simulation.fsm) + '- blocking_call]  ' + str(formatted_goal) + '\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            # client.send_goal(formatted_goal, self.done, self.active, self.feedback)
            client.send_goal(formatted_goal)

            msg = '[fsm ' + str(
                self.simulation.fsm) + '- blocking_call] Goal sent. Goal state %s\n' % client.get_state()
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            if client.wait_for_result(timeout=rospy.Duration(1)):
                msg = '[fsm ' + str(self.simulation.fsm) + '- blocking_call] server returned\n'
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)
                res = client.get_result()
                result = res.act_outcome
            else:
                msg = '[fsm ' + str(self.simulation.fsm) + '- blocking_call] server did not return\n'
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)
                result = 12

            # Update profile of the agent asked for help
            task_id = goal['id']

            task_idx = -1
            for t in self.myknowledge.known_people[agent_idx][2]:
                if t == task_id:
                    rospy.loginfo('t %d\n' % t)
                    task_idx = self.myknowledge.known_people[agent_idx][2].index(t)
                    rospy.loginfo('tx %d\n' % task_idx)
                    break

            msg = '[fsm ' + str(self.simulation.fsm) + '- blocking_call] task_id %d, task_idx %d, agent_tasks %s\n' % (
                task_id, task_idx, self.myknowledge.known_people[agent_idx][2])
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            self.myknowledge.lock.acquire()

            self.myknowledge.capability_expertise[agent_idx][task_idx][1] += 1
            self.myknowledge.total_interactions[agent_idx] += 1

            msg += '[fsm ' + str(self.simulation.fsm) + '- blocking_call] cap expertise %s\n' % str(
                self.myknowledge.capability_expertise)

            if not result == 12:
                self.myknowledge.helping_interactions[agent_idx] += 1
                if result == 1:
                    self.myknowledge.capability_expertise[agent_idx][task_idx][0] += 1

            msg = '[fsm ' + str(self.simulation.fsm) + '- blocking_call] tot interactions %s\n' % str(
                self.myknowledge.total_interactions)
            msg += '[fsm ' + str(self.simulation.fsm) + '- blocking_call] helping inter %s\n' % str(
                self.myknowledge.helping_interactions)
            msg += '[fsm ' + str(self.simulation.fsm) + '- blocking_call] cap expertise %s\n' % str(
                self.myknowledge.capability_expertise)
            # self.log.write_log_file(self.log.stdout_log, msg)

            self.myknowledge.known_people[agent_idx][1] = self.myknowledge.helping_interactions[agent_idx] \
                                                          / float(self.myknowledge.total_interactions[agent_idx])

            msg += '[fsm ' + str(self.simulation.fsm) + '- blocking_call] perceived help %f\n' % \
                                                        self.myknowledge.known_people[agent_idx][1]

            self.myknowledge.known_people[agent_idx][3][task_idx] = \
                self.myknowledge.capability_expertise[agent_idx][task_idx][0] \
                / float(
                    self.myknowledge.capability_expertise[agent_idx][task_idx][1])
            msg += '[fsm ' + str(self.simulation.fsm) + '- blocking_call] cap expertise %s\n' % str(
                self.myknowledge.known_people)

            self.myknowledge.lock.release()

            rospy.loginfo(msg)
            self.simulation.requests[self.myknowledge.difficulty] = self.simulation.requests[
                                                                        self.myknowledge.difficulty] + 1
            msg = '[fsm ' + str(self.simulation.fsm) + '- blocking_call - END] perceived helpfulness %f\n' % \
                                                       self.myknowledge.known_people[agent_idx][1]
            msg += '[fsm ' + str(self.simulation.fsm) + '- blocking_call] capability expertise %f\n' % \
                                                        self.myknowledge.known_people[agent_idx][3][task_idx]
            msg += '[fsm ' + str(self.simulation.fsm) + '- blocking_call] Result ' + str(result) + '\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            msg += '[fsm ' + str(self.simulation.fsm) + '- blocking_call] Requests ' + str(
                sum(self.simulation.requests)) + '\n'
            rospy.loginfo(msg)

            self.end += 1
            self.mycore.amIblocking = False
            msg += '[fsm ' + str(self.simulation.fsm) + '- blocking_call] blocking ' + str(self.mycore.amIblocking) + '\n'
            rospy.loginfo(msg)

            return result
        except rospy.ROSInternalException:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))
            pass
        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()[0]) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))
            pass

    def execute_git(self, goalhandle):
        # print 'I got a request'
        # Add tag to identify current thread
        # Task status: 12 ~ REJECT, 0 ~ PENDING, 1 ~ SUCCESS, 2 ~ FAIL 10 ~ no thread active
        # index = -1
        msg = '[execute_git - BEGIN]\n'
        rospy.loginfo(msg)
        self.begin += 1
        try:
            feedback = doMeFavorFeedback()
            result = doMeFavorResult()

            self.myknowledge.lock.acquire()
            goalh = goalhandle.get_goal()
            # self.log.write_log_file(self.log.stdout_log, '[execute_git] getting goal: %s\n' % goal)
            msg = '[execute_git] Goal: %s\n' % (str(goalh.content))

            rospy.loginfo(msg)

            goal = self.mycore.string2goalPlan(goalh.content, self.log)

            self.simulation.requests_received[len(goal[0]['abilities']) - 1] += 1

            # Read all the senders for a task #

            msg = '[execute_git %d] Goal: %s\n' % (int(goal[0]['senderID']), str(goal))
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            # Check if I have already gotten smth from this sender, in that case it's already in the queue, just change task_status to 0
            try:
                # self.log.write_log_file(self.log.stdout_log, '[execute_git] check if guy is in list\n')
                index = next(
                    index for (index, d) in enumerate(self.keep_track_threads) if
                    d['senderId'] == int(goal[0]['senderID']))
                self.keep_track_threads[index]['task_status'] = 0
                # print 'Guy currently in list: %d' % index
                msg = '[execute_git %d] Guy currently in list: %d\n' % (int(goal[0]['senderID']), index)
                self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)

            except StopIteration:
                # we can check first element in potential array goal, because the sender for each task is the same
                self.keep_track_threads.append({'senderId': int(goal[0]['senderID']), 'task_status': 0})
                index = len(self.keep_track_threads) - 1
                msg = '[execute_git %d] New guy: %d\n' % (int(goal[0]['senderID']), index)
                self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)
                # It is assumed that the senderId is unique, that is the server cannot get 2 a second task from an agent, without returning with the first.
                # {senderID:task_status}
                # self.keep_track_threads.append({data.sender:0})

            msg = '[execute_git %d] Threads: %s\n' % (int(goal[0]['senderID']), str(self.keep_track_threads))
            self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            # it seems that I have mixed up the queues. goalhandles I need only manipulate in execute_git. the goal themselves and the keep_track_threads are manipulated by the main thread!
            # self.queueGoalHandles.put(goalhandle)

            self.myknowledge.plan_pending_eval.put(goal)
            # self.log.write_log_file(self.log.stdout_log, '[execute_git %d] %s\n' % (int(goal[0]['senderID']), str(self.myknowledge.plan_pending_eval)))
            self.myknowledge.lock.release()

            timeout = time.time() + 20  # set timeout to be 10 seconds
            # self.log.write_log_file(self.log.stdout_log, '[execute_git %d] timeout: %s\n' % (int(goal[0]['senderID']), str(timeout)))

            msg = '[execute_git %d] Current goal status: %s\n' % (
                int(goal[0]['senderID']), goalhandle.get_goal_status())
            self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            while self.keep_track_threads[index]['task_status'] == 0:
                # self.log.write_log_file(self.log.stdout_log, '[execute_git] Current goal status: %s\n' % goalhandle.get_goal_status())
                # Let the thread wait for 10 sec, if nothing then return with -1 ~ FAIL
                #if time.time() > timeout:
                if self.mycore.amIblocking or time.time() > timeout:
                    self.simulation.rejection_blocking += 1
                    # if self.mycore.amIblocking:
                    self.keep_track_threads[index]['task_status'] = 12
                    msg = '[execute_git %d] request dropped, because I am waiting on another agent. Threads %s\n' % (
                        int(goal[0]['senderID']), str(self.keep_track_threads))
                    self.log.write_log_file(self.log.stdout_log, msg)
                    rospy.loginfo(msg)
                    self.myknowledge.timeouts += 1
                    break

            self.server.git_accept_new_goal(goalhandle)

            msg = '[execute_git %d] Current goal status: %s. Threads %s\n' % (
                int(goal[0]['senderID']), goalhandle.get_goal_status(), str(self.keep_track_threads))
            self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            result.act_outcome = self.keep_track_threads[index]['task_status']

            self.server.set_succeeded(goalhandle, result)
            msg = '[execute_git %d] Current goal status: %s. Threads %s\n' % (
                int(goal[0]['senderID']), goalhandle.get_goal_status(), str(self.keep_track_threads))
            self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            # self.server.set_succeeded(goalhandle)
            self.myknowledge.lock.acquire()
            self.keep_track_threads[index]['task_status'] = 10
            self.myknowledge.lock.release()

            msg = '[execute_git %d - END] Threads: %s\nResult %s\n' % (
                int(goal[0]['senderID']), str(self.keep_track_threads), str(result))
            self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)
        except rospy.ROSInternalException:
            rospy.loginfo(
                "Unexpected internal error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))
            pass
        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))
            pass
        msg = '[execute_git %d - END]\n' % int(goal[0]['senderID'])
        rospy.loginfo(msg)
        self.end += 1

    def execute(self, data):
        # Do lots of awesome groundbreaking robot stuff here

        ###Extract content
        self.log.write_log_file(self.log.stdout_log, '[action] ' + str(data.content) + '\n')
        goal = self.mycore.string2goal(data.content)

        self.log.write_log_file(self.log.stdout_log, '[action] ' + str(goal) + '\n')
        feedback = doMeFavorFeedback()
        result = doMeFavorResult()
        self.log.write_log_file(self.log.stdout_log, '[action] ' + str(feedback) + '\n')
        percent = 0
        while percent < 100.0:
            percent = percent + 10.0
            feedback.time2finish = percent
            self.log.write_log_file(self.log.stdout_log, '[action] ' + str(feedback) + '\n')
            self.server.publish_feedback(feedback)
        result.act_outcome = 1
        self.log.write_log_file(self.log.stdout_log, '[action] ' + str(result) + '\n')
        self.server.set_succeeded(result)

    def check_agent_exist(self, agent_id):
        found = False
        for x in self.myknowledge.known_people:
            if agent_id == x[0]:
                found = True
                break
        if not found:
            self.myknowledge.people.append(agent_id)

    ##################################################################################################
    ##################################################################################################

    def change_selfstate_v2(self):
        if not self.mycore.state == 3:
            if not self.myknowledge.plan_pending_eval.empty():
                msg = '[fsm ' + str(self.simulation.fsm) + '] adaptive state: True\n'
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)

                self.myknowledge.lock.acquire()
                self.myknowledge.old_state = self.mycore.state
                self.mycore.state = 1
                msg = '[fsm ' + str(self.simulation.fsm) + '] Old state, and current state:' + str(
                    self.myknowledge.old_state) + ', ' + str(self.mycore.state) + '\n'
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)
                self.myknowledge.lock.release()
            else:
                msg = '[fsm ' + str(self.simulation.fsm) + '] adaptive state: False\n'
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)

    def eval_temp_2(self):
        try:
            self.begin += 1
            msg = '[adapt ' + str(self.simulation.interact) + ' BEGIN]\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)
            msg = '[adapt ' + str(self.simulation.interact) + ' BEGIN]\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)
            ## Take plan-request out of queue, and put the tasks into the queue for tasks the agent has committed to
            # careful with the queues below, there is no handling if it is empty!!
            # pdb.set_trace()
            plan = self.myknowledge.plan_pending_eval.get()
            msg = '[adapt' + str(self.simulation.interact) + '] plan gotten from queue \n' + str(plan)
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)
            # print 'This is the newly gotten plan ' + str(plan)
            aID = int(plan[0]['senderID'])
            aIDx = -1
            # print self.myknowledge.known_people
            # Find the index of this agent in known_people. TODO add it if not there
            for x in self.myknowledge.known_people:
                if x[0] == aID:
                    aIDx = self.myknowledge.known_people.index(x)
                    msg = '[adapt %d] aIDX = %d\n' % (self.simulation.interact, aIDx)
                    # self.log.write_log_file(self.log.stdout_log, msg)
                    rospy.loginfo(msg)
                    break
            if not aIDx == -1:
                # It is not success but PERCEIVED WILLINGNESS
                success = self.myknowledge.known_people[aIDx][1]
                msg = '[adapt %d] In known people, success = %f\n' % (self.simulation.interact, success)
                msg += '[adapt %d] In known people, %s\n' % (
                    self.simulation.interact, str(self.myknowledge.known_people))
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)
            else:
                success = -1.0
                msg = '[adapt %d] Not in known people, success = %f\n' % (self.simulation.interact, success)
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)

            # pdb.set_trace()
            # abil, equip, knowled, tools, env_risk, diff_task_tradeoff = self.simulation.simulate_give_params()
            abil = 1
            msg = '[adapt %d] task abilities: %s\n own abilities: %s\n' % (
                self.simulation.interact, plan[0]['abilities'], self.abilities)
            # self.log.write_log_file(self.log.stdout_log, msg)
            for x in plan[0]['abilities']:
                if not x in self.abilities:
                    abil = 0
                    if x == 'transport_victim' and 'proxy' in self.abilities:
                        abil = 1
                    break
            equip = 1
            knowled = 1
            tools = 1

            msg += '[adapt %d] task resources: %s\n own resources: %s\n' % (
                self.simulation.interact, plan[0]['resources'], self.resources)
            # pdb.set_trace()
            for x in plan[0]['resources']:
                if not x in self.resources:
                    tools = 0
                    msg += '\nthe resource is not there at all'
                    break
                elif not plan[0]['resources'][x] <= 0:
                    if self.resources[x] / float(plan[0]['resources'][x]) == 0 or self.resources[x] <= 0:
                        tools = 0  # in this case tools not enough!! -> in the context of the current iteration
                        break
                    break

            msg += '[adapt %d] task resources: %s\n own resources: %s\n' % (
                self.simulation.interact, plan[0]['resources'], self.resources)
            msg += '[adapt %d] abil: %d\n tools: %d\n' % (self.simulation.interact, abil, tools)
            rospy.loginfo(msg)

            env_risk = 0
            if self.myknowledge.old_state == 2 and self.myknowledge.service:
                diff_task_tradeoff = (plan[0]['reward'] - self.myknowledge.service['reward']) / float(
                    self.myknowledge.service['reward'])
                msg = '[adapt %d] new rew %f, old reward %f, trade-off %f:' % (
                    self.simulation.interact, plan[0]['reward'], self.myknowledge.service['reward'], diff_task_tradeoff)
                old_reward = self.myknowledge.service['reward']
            else:
                diff_task_tradeoff = 1
                old_reward = 1
                msg = '[adapt %d] trade-off %f:' % (self.simulation.interact, diff_task_tradeoff)

            # energy_diff = self.mycore.battery - float(plan[0]['energy'])  # HOW 2 DEAL with this
            energy_diff = - float(plan[0]['energy']) + (self.mycore.battery - self.mycore.battery_min)

            # ag_risk = 1.0 - success

            if success == -1.0:
                ag_risk = 0.0
            else:
                ag_risk = 1.0 - success

            msg += '[adapt %d] energy diff = %f\n' % (self.simulation.interact, energy_diff)
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            # if not sum(self.simulation.no_self_tasks_attempted) == 0:
            if not sum(self.simulation.no_tasks_attempted) == 0:
                # performance = sum(self.simulation.no_self_tasks_completed) / float(sum(self.simulation.no_self_tasks_attempted))
                performance = sum(self.simulation.no_tasks_completed) / float(sum(self.simulation.no_tasks_attempted))
            else:
                performance = 1.0

            culture = self.calc_culture(self.myknowledge.known_people)
            self.simulation.culture.append(culture)
            msg = '[adapt %d] performance = %f\n' % (self.simulation.interact, performance)
            msg += '[adapt %d] ag_risk = %f, culture = %f\n' % (self.simulation.interact, ag_risk, culture)
            rospy.loginfo(msg)
            # pdb.set_trace()
            if self.static[1] == 0:
                self.myknowledge.lock.acquire()
                # accept, delta = self.mycore.b_delta(energy_diff, abil, equip, knowled, tools, env_risk, [ag_risk, 0], performance, diff_task_tradeoff, culture, aID)
                # accept, delta = self.mycore.deltaD_no_chain(energy_diff, abil, equip, knowled, tools, env_risk, [ag_risk, 0], performance, diff_task_tradeoff, old_reward, culture, aID)
                # accept, delta = self.mycore.deltaD(energy_diff, abil, equip, knowled, tools, env_risk, [ag_risk, 0], performance, diff_task_tradeoff, old_reward, culture, aID)
                accept, delta = self.mycore.delta5(energy_diff, abil, equip, knowled, tools, env_risk, [ag_risk, 0],
                                                   performance, diff_task_tradeoff, culture, aID)
                self.myknowledge.lock.release()

                if not abil or not equip or not knowled or not tools:
                    # For now a plan has only one task but TODO change simulation finish for all the tasks in a plan
                    plan[0]['simulation_finish'] = 0.0
                else:
                    plan[0]['simulation_finish'] = 1.0
            else:
                delta = self.mycore.delta
                if not abil or not equip or not knowled or not tools:
                    # For now a plan has only one task but TODO change simulation finish for all the tasks in a plan
                    plan[0]['simulation_finish'] = 0.0
                else:
                    plan[0]['simulation_finish'] = 1.0
                if random.random() < delta:
                    accept = True
                else:
                    accept = False

            # print accept
            msg = '[adapt %d] abil = %f, equip = %f, knowled = %f, tools = %f, env_risk = %f, task-trade = %f, delta = %f\n' % (
                self.simulation.interact, abil, equip, knowled, tools, env_risk, diff_task_tradeoff, delta)

            msg += '[adapt %d] Accept = %f, delta = %f, simulation-finish = %f\n' % (
                self.simulation.interact, accept, delta, plan[0]['simulation_finish'])
            msg += 'Plan ' + str(plan) + '\n'

            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            self.myknowledge.lock.acquire()
            # CAREFUL - appended performance with respect to dependent jobs
            if not sum(self.simulation.no_tasks_depend_attempted) == 0:
                depend_performance = sum(self.simulation.no_tasks_depend_completed) / float(
                    sum(self.simulation.no_tasks_depend_attempted))
            else:
                depend_performance = 1.0

            if not sum(self.simulation.no_self_tasks_attempted) == 0:
                own_performance = sum(self.simulation.no_self_tasks_completed) / float(
                    sum(self.simulation.no_self_tasks_attempted))
            else:
                own_performance = 1.0
            self.simulation.delta_theta.append(
                [0, delta, accept, performance, depend_performance, own_performance, self.mycore.gamma])
            self.myknowledge.lock.release()

            if accept:
                # self.myknowledge.attempted_jobs += 1
                if self.is_thread_active(int(plan[0]['senderID'])):
                    self.simulation.requests_rec_accept[len(plan[0]['abilities']) - 1] += 1

                    msg = '[adapt ' + str(self.simulation.interact) + '] Adopted plan: ' + str(plan) + '\n'
                    # self.log.write_log_file(self.log.stdout_log, msg)
                    rospy.loginfo(msg)

                    for x in plan:
                        msg = '[adapt ' + str(self.simulation.interact) + '] Task in plan: ' + str(x) + '\n'
                        # self.log.write_log_file(self.log.stdout_log, msg)
                        x['ac_senders'].append(self.mycore.ID)
                        msg += '[adapt ' + str(self.simulation.interact) + '] senders: ' + str(x['ac_senders']) + '\n'
                        rospy.loginfo(msg)
                        self.myknowledge.task_queue.put(x)

                    # put the service that I am doing back in the queue back in the queue, updating the iterations left ##
                    if self.myknowledge.old_state == 2 and not self.myknowledge.service_id == -1 and not self.myknowledge.iteration == -1:
                        self.myknowledge.service['iterations'] = self.myknowledge.service[
                                                                     'iterations'] - self.myknowledge.iteration + 1
                        # self.myknowledge.service['iterations'] = self.myknowledge.service['iterations'] - self.myknowledge.iteration
                        msg = '[adapt %d] exchange tasks, new iterations %d, already done %d\n' % (
                            self.simulation.interact, self.myknowledge.service['iterations'],
                            self.myknowledge.iteration - 1)
                        self.myknowledge.task_queue.put(self.myknowledge.service)
                        self.myknowledge.service_id = -1
                        self.myknowledge.iteration = -1
                        self.simulation.current_fire = -1
                        self.simulation.current_victim = -1
                        # the task I reput in the queue will be counted again when it's taken from the queue.
                        self.simulation.no_tasks_attempted[0] -= 1
                        if int(self.myknowledge.service['senderID'] == self.mycore.ID):
                            self.simulation.no_self_tasks_attempted[0] -= 1
                    ########

                    msg += '[adapt %d] Tasks put in queue\n' % self.simulation.interact
                    # self.log.write_log_file(self.log.stdout_log, msg)
                    rospy.loginfo(msg)

                    self.myknowledge.lock.acquire()
                    self.mycore.state = 2
                    self.myknowledge.lock.release()
                else:
                    msg = "\n Thread not active anymore"
                    self.myknowledge.lock.acquire()
                    self.mycore.state = 0
                    self.myknowledge.lock.release()
                    rospy.loginfo(msg)
            else:
                # print 'keep at what you\'re doing'
                msg = '[adapt %d] Do not adapt\n' % self.simulation.interact
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)

                index = next(index for (index, d) in enumerate(self.keep_track_threads) if d['senderId'] == aID)

                if self.is_thread_active(aID):
                    self.keep_track_threads[index]['task_status'] = 12
                    msg = '[adapt' + str(self.simulation.interact) + '] Threads %s\n' % str(self.keep_track_threads)
                    # self.log.write_log_file(self.log.stdout_log, msg)
                    rospy.loginfo(msg)
                else:
                    self.keep_track_threads[index]['task_status'] = 10
                    msg = '[adapt' + str(
                        self.simulation.interact) + '] Not adapted, but thread not active anymore. Threads %s\n' % str(
                        self.keep_track_threads)
                    # self.log.write_log_file(self.log.stdout_log, msg)
                    rospy.loginfo(msg)

                self.myknowledge.lock.acquire()
                self.mycore.state = self.myknowledge.old_state
                self.myknowledge.lock.release()

            # Record
            self.simulation.delta_esteem.append(performance)
            self.simulation.delta.append(delta)
            self.simulation.delta_bool.append(accept)
        except rospy.ROSInternalException:
            rospy.loginfo(
                "Unexpected internal error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))
            pass
        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))
            pass

        msg = '[adapt' + str(self.simulation.interact) + ' END] \n'
        # self.log.write_log_file(self.log.stdout_log, msg)
        rospy.loginfo(msg)
        self.end += 1

    def amIHelping(self, sender):
        if not sender == self.mycore.ID:
            return True
        else:
            return False

    def get_visible_fires(self):
        try:
            # visible_fires = [x for x in np.transpose(np.array(self.simulation.fires)) if(((x[1] - self.myknowledge.position2D[0]) ** 2 + (x[2] - self.myknowledge.position2D[1]) ** 2) < self.simulation.visible_distance ** 2 or x[6] == 1) and not x[3] == -1000]
            visible_fires = [x for x in np.transpose(np.array(self.simulation.fires)) if (
            ((x[1] - self.myknowledge.position2D[0]) ** 2 + (x[2] - self.myknowledge.position2D[1]) ** 2)
            < self.simulation.visible_distance ** 2 or x[6] == 1) and not x[3] <= 0]

            '''
            msg = str(np.transpose(np.array(self.simulation.fires))) + '\n'
            for x in np.transpose(np.array(self.simulation.fires)):
                msg += 'my pos: %f, %f\n' % (self.myknowledge.position2D[0], self.myknowledge.position2D[1])
                msg += 'fire: %f, %f, and told: %f\n' % (x[1], x[2], x[6])
                msg += 'dist: %f, %f\n' % ((x[1] - self.myknowledge.position2D[0]) ** 2 + (
                    x[2] - self.myknowledge.position2D[1]) ** 2, self.simulation.visible_distance**2)
            '''

            # pdb.set_trace()
            '''
            if len(self.simulation.fires.shape) > 1:
                msg = 'all fires visible now: %d, %d' % (len(visible_fires), self.simulation.fires.shape[1])
                rospy.loginfo(msg)
                if len(visible_fires) == self.simulation.fires.shape[1]:
                    self.simulation.time_all_visible = time.time()
                    msg = 'all fires visible now: %d, %d' % (len(visible_fires), self.simulation.fires.shape[1])
                    rospy.loginfo(msg)
            '''
            msg = '[get_visible_fires] all: %s\n' % str(np.transpose(np.array(self.simulation.fires)))
            msg += '[get_visible_fires] visible: %s\n' % str(np.array(visible_fires))
            # self.log.write_log_file(self.log.stdout_log, msg)

            rospy.loginfo(msg)
            return np.transpose(np.array(visible_fires))
        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))

    def get_visible_victims(self):
        try:
            visible_fires = [x for x in np.transpose(np.array(self.simulation.fires)) if
                             ((((x[1] - self.myknowledge.position2D[0]) ** 2 + (
                                 x[2] - self.myknowledge.position2D[1]) ** 2) < self.simulation.visible_distance ** 2 or
                               x[6] == 1) and x[5] == 0) and x[4] > 0]
            msg = '[get_visible_victims] all victims: %s \n' % str(np.transpose(np.array(self.simulation.fires)))
            msg += '[get_visible_victims] visible victims: %s\n' % str(np.array(visible_fires))
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)
            return np.transpose(np.array(visible_fires))
        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))

    def idle(self):
        try:
            # print 'im in idle'
            self.simulation.idle = self.simulation.inc_iterationstamps(self.simulation.idle)
            msg = '[idle ' + str(self.simulation.idle) + '] idle\n'
            # self.log.write_log_file(self.log.stdout_log, msg)

            start = time.time()
            # self.generate_goal_v2()
            # self.random_walk()

            if 'proxy' in self.abilities:
                self.levy_walk_step(1)
                fire = Fires_Info()
                # time.sleep(5)
                visible_fires = np.transpose(self.get_visible_fires())
                if visible_fires.size:
                    fire.id = [x[0] for x in visible_fires]
                    fire.xpos = [x[1] for x in visible_fires]
                    fire.ypos = [x[2] for x in visible_fires]
                    fire.intensity = [x[3] for x in visible_fires]
                    fire.victims = [x[4] for x in visible_fires]
                    fire.status = [x[5] for x in visible_fires]

                    self.publish_fires.publish(fire)
            else:
                self.levy_walk_step(0)
                self.generate_goal_v3()

            elapsed = time.time() - start
            msg += '[fsm ' + str(self.simulation.fsm) + '] generate_goal exec time: ' + str(elapsed) + '\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)
            self.commit2goal()
        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))

    def interact(self):
        # print 'im in interact'
        self.simulation.interact = self.simulation.inc_iterationstamps(self.simulation.interact)

        self.eval_temp_2()

        self.evaluate_my_state()
        self.evaluate_agent()
        self.evaluate_request()
        self.commit2agent()

    def is_thread_active(self, senderID):
        for x in self.keep_track_threads:
            if int(x['senderId']) == senderID:
                if int(x['task_status']) == 0:
                    rospy.loginfo('thread active %d\n' % int(x['senderId']))
                    return True
        return False

    def execute_v2(self):
        try:
            self.begin += 1
            self.simulation.execute = self.simulation.inc_iterationstamps(self.simulation.execute)

            msg = '[execute ' + str(self.simulation.execute) + ' BEGIN] Current service ' + str(
                self.myknowledge.service) + '\n'
            msg += '[execute ' + str(self.simulation.execute) + '] id ' + str(self.myknowledge.service_id) + '\n'
            msg += '[execute ' + str(self.simulation.execute) + '] nr of iterations ' + str(
                self.myknowledge.iteration) + '\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            if self.myknowledge.service_id == -1 and self.myknowledge.iteration == -1:
                if not self.myknowledge.task_queue.empty():
                    self.myknowledge.service = self.myknowledge.task_queue.get()
                    active_senders = [self.mycore.ID]
                    msg = '[execute ' + str(self.simulation.execute) + ']' + str(
                        self.myknowledge.service) + '\n'
                    # self.log.write_log_file(self.log.stdout_log, msg)
                    self.simulation.counted_d = 0
                    self.simulation.current_fire = -1
                    self.simulation.current_victim = -1

                    if "fire_extinguishing" in self.abilities:
                        msg += '[execute ' + str(self.simulation.execute) + '] water:' + str(
                            self.resources['water']) + '\n'
                        if self.resources['water'] <= 0:
                            # self.goto_base(1)
                            pass
                        # self.resources['water'] = 25
                        msg += '[execute ' + str(self.simulation.execute) + '] water:' + str(
                            self.resources['water']) + '\n'
                    elif "transport_victim" or "proxy" in self.abilities:
                        msg += '[execute ' + str(self.simulation.execute) + '] spots:' + str(
                            self.resources['spotxPerson']) + '\n'
                        if self.resources['spotxPerson'] <= 0:
                            # self.goto_base(2)
                            pass
                        # self.resources['spotxPerson'] = 5
                        msg += '[execute ' + str(self.simulation.execute) + '] spots:' + str(
                            self.resources['spotxPerson']) + '\n'

                    self.myknowledge.service_id = int(self.myknowledge.service['id'])

                    msg += '[execute ' + str(self.simulation.execute) + ']' + str(self.myknowledge.service_id) + '\n'

                    self.myknowledge.iteration = 1

                    msg += '[execute ' + str(self.simulation.execute) + ']' + str(self.myknowledge.iteration) + '\n'

                    # Detect task difficulty - from nr of required services
                    self.myknowledge.difficulty = self.simulation.detect_difficulty(self.myknowledge.service)
                    msg += '[execute ' + str(self.simulation.execute) + ' BEGIN] Current service ' + str(
                        self.myknowledge.service) + '\n'
                    msg += '[execute ' + str(self.simulation.execute) + '] iterations' + str(
                        self.myknowledge.service['iterations']) + '\n'

                    rospy.loginfo(msg)

                    # self.simulation.time = self.simulation.delay[self.myknowledge.difficulty] / float(self.myknowledge.service['iterations'])

                    self.simulation.no_tasks_attempted[self.myknowledge.difficulty] += 1

                    msg = '[execute ' + str(self.simulation.execute) + '] Difficulty: ' + str(
                        self.myknowledge.difficulty) + '\n'
                    rospy.loginfo(msg)

                    if not int(self.myknowledge.service['senderID'] == self.mycore.ID):
                        if self.is_thread_active(int(self.myknowledge.service['senderID'])):
                            msg = '[execute ' + str(
                                self.simulation.execute) + ']I am helping someone and their thread is still active\n'
                            rospy.loginfo(msg)

                            self.execute_step_v6()
                        else:
                            msg = '[execute ' + str(self.simulation.execute) + ']Thread not active anymore\n'

                            self.myknowledge.service_id = -1
                            self.myknowledge.iteration = -1
                            self.simulation.no_tasks_attempted[self.myknowledge.difficulty] -= 1
                            rospy.loginfo(msg)
                    else:
                        msg = '[execute ' + str(self.simulation.execute) + '] Working for myself\n'
                        self.simulation.no_self_tasks_attempted[self.myknowledge.difficulty] += 1
                        rospy.loginfo(msg)
                        self.execute_step_v6()
                else:
                    self.myknowledge.lock.acquire()
                    self.mycore.state = 0
                    self.myknowledge.lock.release()
                    msg = '[execute ' + str(self.simulation.execute) + '] My state: ' + str(self.mycore.state) + '\n'
                    rospy.loginfo(msg)
            else:
                msg = '[execute ' + str(self.simulation.execute) + '] continue working\n'
                rospy.loginfo(msg)
                self.execute_step_v6()

            msg = '[execute ' + str(self.simulation.execute) + 'END]\n'
            rospy.loginfo(msg)
            self.end += 1

        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()[0]) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))
            pass

    def execute_step_v2(self):
        dependencies = self.simulation.sim_dependencies(self.myknowledge.service)

        self.log.write_log_file(self.log.stdout_log,
                                '[run_step ' + str(self.simulation.execute) + '] dependencies: %f \n' % dependencies)

        self.log.write_log_file(self.log.stdout_log,
                                '[run_step ' + str(self.simulation.execute) + '] fuzzy inputs: %f, health: %f\n' % int(
                                    dependencies, sum([self.mycore.sensmot, self.mycore.battery])))

        start_time = timeit.default_timer()
        depend_fuzzy = self.mycore.willing2ask(
            [sum([self.mycore.sensmot, self.mycore.battery]), 0.7, dependencies, 0.5])
        self.simulation.fuzzy_time.append(timeit.default_timer() - start_time)

        self.log.write_log_file(self.log.stdout_log,
                                '[run_step ' + str(self.simulation.execute) + '] depend_fuzzy: %f \n' % int(
                                    depend_fuzzy))

        if self.myknowledge.iteration < int(self.myknowledge.service['iterations']):
            self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(
                self.simulation.execute) + '] Running task: %d, iteration: %d\n' % (
                                        self.myknowledge.service_id, self.myknowledge.iteration))
            self.myknowledge.iteration = self.myknowledge.iteration + 1
        else:
            self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(
                self.simulation.execute) + '] Task: %d done\n' % self.myknowledge.service_id)
            self.myknowledge.service_id = -1
            self.myknowledge.iteration = -1

    ##Instead of iteration, pause for some prespecified time
    def execute_step_v3(self):
        dependencies, req_missing = self.simulation.sim_dependencies(self.myknowledge.service)

        self.log.write_log_file(self.log.stdout_log,
                                '[run_step ' + str(self.simulation.execute) + '] dependencies: %f \n' % dependencies)

        self.log.write_log_file(self.log.stdout_log,
                                '[run_step ' + str(self.simulation.execute) + '] fuzzy inputs: %f, health: %f\n' % (
                                    dependencies, sum([self.mycore.sensmot, self.mycore.battery])))

        start_time = timeit.default_timer()
        depend_fuzzy = self.mycore.willing2ask(
            [sum([self.mycore.sensmot, self.mycore.battery]), 0.7, dependencies, 0.5])
        self.simulation.fuzzy_time.append(timeit.default_timer() - start_time)

        self.log.write_log_file(self.log.stdout_log,
                                '[run_step ' + str(self.simulation.execute) + '] depend_fuzzy: ' + str(
                                    depend_fuzzy) + '\n')

        if req_missing and not depend_fuzzy:
            self.simulation.required_missing_noreq = self.simulation.required_missing_noreq + 1
            self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(
                self.simulation.execute) + '] There should have been a request: ' + str(
                self.simulation.required_missing_noreq / float(self.simulation.required_missing)) + '\n')

        if depend_fuzzy:
            self.simulation.requests[self.myknowledge.difficulty] = self.simulation.requests[
                                                                        self.myknowledge.difficulty] + 1
            exec_time = self.simulation.additional_delay[self.myknowledge.difficulty] + self.simulation.delay[
                self.myknowledge.difficulty]
            self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(
                self.simulation.execute) + '] difficulty: %f, delay: %f, addi: %f\n' % (
                                        self.myknowledge.difficulty, self.simulation.delay[self.myknowledge.difficulty],
                                        self.simulation.additional_delay[self.myknowledge.difficulty]))
            self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(
                self.simulation.execute) + '] Ask for help\n ...Wait for %f\n' % exec_time)
            self.simulation.exec_times[self.myknowledge.difficulty] = self.simulation.exec_times[
                                                                          self.myknowledge.difficulty] + exec_time
            time.sleep(exec_time)
        else:
            exec_time = self.simulation.delay[self.myknowledge.difficulty]
            self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(
                self.simulation.execute) + '] Do it yourself\n ...Wait for %f\n' % exec_time)
            self.simulation.exec_times[self.myknowledge.difficulty] = self.simulation.exec_times[
                                                                          self.myknowledge.difficulty] + exec_time

            self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(
                self.simulation.execute) + '] difficulty: %f, delay: %f, addi: %f\n' % (
                                        self.myknowledge.difficulty, self.simulation.delay[self.myknowledge.difficulty],
                                        self.simulation.additional_delay[self.myknowledge.difficulty]))
            time.sleep(exec_time)
            self.myknowledge.service_id = -1
            self.myknowledge.iteration = -1

    ##Make requests to action server
    def execute_step_v4(self):
        try:
            if self.myknowledge.iteration == 1:
                self.begin += 1
                msg = '[run_step ' + str(self.simulation.execute) + ' BEGIN] in execute_step\n'
                rospy.loginfo(msg)
                # print 'in execute_step'
                # pdb.set_trace()
                # This returns the best candidate id, and success measure
                success_chance, candidate_id, candidate_idx = self.mycore.best_candidate(self.myknowledge.known_people,
                                                                                         self.myknowledge.service,
                                                                                         self.log, int(
                        self.myknowledge.service['senderID']))
                msg = '[run_step ' + str(
                    self.simulation.execute) + ' BEGIN] success %f, id %d, idx %d\n' % (
                    success_chance, candidate_id, candidate_idx
                )
                rospy.loginfo(msg)

                if candidate_id == int(self.myknowledge.service['senderID']) and not self.mycore.ID == \
                        self.myknowledge.service['senderID']:
                    msg = '[run_step ' + str(
                        self.simulation.execute) + '] do not ask the same agent that asked you for help'
                    rospy.loginfo(msg)
                    success_chance = -1.0

                abil, equip, knowled, tools, env_risk, diff_task_progress = self.simulation.simulate_ask_params()

                if self.myknowledge.service['simulation_finish'] == 0.0:
                    abil = 0.0

                energy_diff = self.mycore.battery - float(self.myknowledge.service['energy'])
                ag_risk = 1.0 - success_chance

                # if not sum(self.simulation.no_self_tasks_attempted) == 0:
                if not sum(self.simulation.no_tasks_attempted) == 0:
                    # performance = sum(self.simulation.no_self_tasks_completed) / float(sum(self.simulation.no_self_tasks_attempted))
                    performance = sum(self.simulation.no_tasks_completed) / float(
                        sum(self.simulation.no_tasks_attempted))
                else:
                    performance = 1.0

                if self.static[0] == 0:
                    self.myknowledge.lock.acquire()
                    depend, gamma = self.mycore.b_gamma(energy_diff, abil, equip, knowled, tools, env_risk, ag_risk,
                                                        performance, diff_task_progress)
                    self.myknowledge.lock.release()
                    self.myknowledge.service['simulation_finish'] = 1.0
                else:
                    gamma = self.mycore.gamma
                    if random.random() < gamma:
                        depend = True
                    else:
                        depend = False
                        if self.myknowledge.service['simulation_finish'] == -1.0:
                            if not abil or not equip or not knowled or not tools:
                                self.myknowledge.service['simulation_finish'] = 0.0
                                self.simulation.no_tasks_depend_attempted[self.myknowledge.difficulty] += 1
                            else:
                                self.myknowledge.service['simulation_finish'] = 1.0

                msg = '[run_step ' + str(self.simulation.execute) + '] ask for help: ' + str(depend) + '\n'
                msg += '[execute %d] abil = %f, equip = %f, knowled = %f, tools = %f, env_risk = %f, task-trade = %f, gamma = %f\n' % (
                    self.simulation.execute, abil, equip, knowled, tools, env_risk, diff_task_progress, gamma) + '\n'

                rospy.loginfo(msg)

                self.myknowledge.lock.acquire()
                # CAREFUL - appended performance with respect to dependent jobs
                if not sum(self.simulation.no_tasks_depend_attempted) == 0:
                    depend_performance = sum(self.simulation.no_tasks_depend_completed) / float(
                        sum(self.simulation.no_tasks_depend_attempted))
                else:
                    depend_performance = 1.0

                if not sum(self.simulation.no_self_tasks_attempted) == 0:
                    own_performance = sum(self.simulation.no_self_tasks_completed) / float(
                        sum(self.simulation.no_self_tasks_attempted))
                else:
                    own_performance = 1.0
                self.simulation.delta_theta.append(
                    [1, gamma, depend, performance, depend_performance, own_performance, self.mycore.delta])
                self.myknowledge.lock.release()

                result = 0
            else:
                self.begin += 1
                msg = '[run_step ' + str(self.simulation.execute) + ' BEGIN] in execute_step\n'
                rospy.loginfo(msg)
                # print 'in execute_step'
                # pdb.set_trace()
                # This returns the best candidate id, and success measure
                success_chance, candidate_id, candidate_idx = self.mycore.best_candidate(self.myknowledge.known_people,
                                                                                         self.myknowledge.service,
                                                                                         self.log, int(
                        self.myknowledge.service['senderID']))
                msg = '[run_step ' + str(
                    self.simulation.execute) + ' BEGIN] success %f, id %d, idx %d\n' % (
                    success_chance, candidate_id, candidate_idx
                )
                rospy.loginfo(msg)

                if candidate_id == int(self.myknowledge.service['senderID']) and not self.mycore.ID == \
                        self.myknowledge.service['senderID']:
                    msg = '[run_step ' + str(
                        self.simulation.execute) + '] do not ask the same agent that asked you for help'
                    rospy.loginfo(msg)
                    success_chance = -1.0

                abil, equip, knowled, tools, env_risk, diff_task_progress = self.simulation.simulate_ask_params()
                energy_diff = self.mycore.battery - float(self.myknowledge.service['energy'])
                ag_risk = 1.0 - success_chance

                # if not sum(self.simulation.no_self_tasks_attempted) == 0:
                if not sum(self.simulation.no_tasks_attempted) == 0:
                    # performance = sum(self.simulation.no_self_tasks_completed) / float(sum(self.simulation.no_self_tasks_attempted))
                    performance = sum(self.simulation.no_tasks_completed) / float(
                        sum(self.simulation.no_tasks_attempted))
                else:
                    performance = 1.0

                if self.static[0] == 0:
                    self.myknowledge.lock.acquire()
                    depend, gamma = self.mycore.b_gamma(energy_diff, 1, equip, knowled, tools, env_risk, ag_risk,
                                                        performance, diff_task_progress)
                    self.myknowledge.lock.release()
                    self.myknowledge.service['simulation_finish'] = 1.0
                else:
                    gamma = self.mycore.gamma
                    if random.random() < gamma:
                        depend = True
                    else:
                        depend = False
                        if self.myknowledge.service['simulation_finish'] == -1.0:
                            if not abil or not equip or not knowled or not tools:
                                self.myknowledge.service['simulation_finish'] = 0.0
                                if self.myknowledge.iteration == 1:
                                    self.simulation.no_tasks_depend_attempted[self.myknowledge.difficulty] += 1
                            else:
                                self.myknowledge.service['simulation_finish'] = 1.0

                msg = '[run_step ' + str(self.simulation.execute) + '] ask for help: ' + str(depend) + '\n'
                msg += '[execute %d] abil = %f, equip = %f, knowled = %f, tools = %f, env_risk = %f, task-trade = %f, gamma = %f\n' % (
                    self.simulation.execute, abil, equip, knowled, tools, env_risk, diff_task_progress, gamma) + '\n'

                rospy.loginfo(msg)

                self.myknowledge.lock.acquire()
                # CAREFUL - appended performance with respect to dependent jobs
                if not sum(self.simulation.no_tasks_depend_attempted) == 0:
                    depend_performance = sum(self.simulation.no_tasks_depend_completed) / float(
                        sum(self.simulation.no_tasks_depend_attempted))
                else:
                    depend_performance = 1.0

                if not sum(self.simulation.no_self_tasks_attempted) == 0:
                    own_performance = sum(self.simulation.no_self_tasks_completed) / float(
                        sum(self.simulation.no_self_tasks_attempted))
                else:
                    own_performance = 1.0
                self.simulation.delta_theta.append(
                    [1, gamma, depend, performance, depend_performance, own_performance, self.mycore.delta])
                self.myknowledge.lock.release()

                result = 0
                pass
            #################################
            #################################
            #################################
            if depend:
                self.simulation.no_tasks_depend_attempted[self.myknowledge.difficulty] += 1
                msg = '[run_step ' + str(self.simulation.execute) + 'tasks depend: ' + str(
                    sum(self.simulation.no_tasks_depend_attempted)) + '\n'
                rospy.loginfo(msg)

                if self.mycore.ID == self.myknowledge.service['senderID']:
                    self.simulation.no_tasks_depend_own_attempted[self.myknowledge.difficulty] += 1
                if not candidate_id == -1:

                    msg = '[run_step ' + str(
                        self.simulation.execute) + '] Ask for help. Difficulty: %f, delay: %f, addi: %f\n' % (
                        self.myknowledge.difficulty,
                        self.simulation.delay[self.myknowledge.difficulty],
                        self.simulation.additional_delay[self.myknowledge.difficulty])
                    rospy.loginfo(msg)
                    # pdb.set_trace()
                    agent2ask = '/robot' + str(candidate_id) + '/brain_node'
                    msg = '[run_step ' + str(
                        self.simulation.execute) + '] agent2ask is: ' + str(agent2ask) + '\n'
                    rospy.loginfo(msg)
                    ######### Make request to action_server
                    # self.call_action_server(self.myknowledge.service, agent2ask)
                    # print 'before blocking call'
                    self.myknowledge.service['iterations'] = self.myknowledge.service[
                                                                 'iterations'] - self.myknowledge.iteration + 1
                    start = time.time()

                    result = self.call_blocking_action_server(self.myknowledge.service, agent2ask, candidate_idx)

                    # TIME THE SERVER'S RESPONSE!!
                    exec_time = time.time() - start

                    msg = '[run_step ' + str(self.simulation.execute) + '] exec_time: ' + str(exec_time) + '\n'
                    rospy.loginfo(msg)
                    self.myknowledge.service_id = -1
                    self.myknowledge.iteration = -1

                    # Assume that less energy is consumed when asking for help -- someone else is doing the deed
                    self.mycore.battery_change(0.2 * int(self.myknowledge.service['energy']))

                    if result == 1:
                        msg = '[run_step ' + str(self.simulation.execute) + '] depend SUCCESS\n'
                        self.simulation.requests_success[self.myknowledge.difficulty] += 1

                        rospy.loginfo(msg)
                        self.simulation.exec_times[self.myknowledge.difficulty] = self.simulation.exec_times[
                                                                                      self.myknowledge.difficulty] + exec_time
                        self.simulation.exec_times_depend.append(exec_time)
                        self.simulation.no_tasks_depend_completed[self.myknowledge.difficulty] += 1
                        self.simulation.no_tasks_completed[self.myknowledge.difficulty] += 1
                        if self.mycore.ID == self.myknowledge.service['senderID']:
                            self.simulation.no_tasks_depend_own_completed[self.myknowledge.difficulty] += 1

                    self.mycore.battery_change(0.2 * int(self.myknowledge.service['energy']))

                else:
                    # Count noones serves to identify those case in which the agent does not know anyone that could be of help
                    self.myknowledge.COUNT_noones[self.myknowledge.difficulty] += 1
                    self.myknowledge.service_id = -1
                    self.myknowledge.iteration = -1

                    # Assume that less energy is consumed when asking for help -- someone else is doing the deed
                    self.mycore.battery_change(0.002 * int(self.myknowledge.service['energy']))

                    msg = '[run_step ' + str(self.simulation.execute) + '] No one to ask. Known people ' + str(
                        self.myknowledge.known_people) + '\n'
                    rospy.loginfo(msg)

                # In case I am helping some other agent, trigger response here
                msg = '[run_step ' + str(self.simulation.execute) + '] sender: %d, result: %d\n' % (
                    int(self.myknowledge.service['senderID']), result)
                rospy.loginfo(msg)

                # pdb.set_trace()
                if self.amIHelping(int(self.myknowledge.service['senderID'])):
                    if result == 1:
                        self.simulation.requests_rec_success[self.myknowledge.difficulty] += 1
                    # You need to count loops
                    msg = '[run_step ' + str(self.simulation.execute) + '] service %s, threads: %s\n' % (
                        self.myknowledge.service, str(self.keep_track_threads))
                    rospy.loginfo(msg)

                    index = next(index for (index, d) in enumerate(self.keep_track_threads) if
                                 d['senderId'] == int(self.myknowledge.service['senderID']))

                    if self.is_thread_active(int(self.myknowledge.service['senderID'])):
                        if result == 1:
                            self.keep_track_threads[index]['task_status'] = 1
                        else:
                            self.keep_track_threads[index]['task_status'] = 2

                        msg = '[run_step ' + str(self.simulation.execute) + '] Threads %s\n' % str(
                            self.keep_track_threads)
                        rospy.loginfo(msg)
                    else:
                        self.keep_track_threads[index]['task_status'] = 10
                        msg = '[run_step ' + str(
                            self.simulation.execute) + '] End of task, but thread not active anymore. Threads %s\n' % str(
                            self.keep_track_threads)
                        rospy.loginfo(msg)
                else:
                    if result == 1:
                        self.simulation.no_self_tasks_completed[self.myknowledge.difficulty] += 1

                # Record
                self.simulation.theta_esteem.append(performance)
                self.simulation.theta_candidate.append(success_chance)
                self.simulation.theta.append(gamma)
                self.simulation.theta_bool.append(depend)
                # Inc to reach stop of simulation

                msg = '[run_step ' + str(self.simulation.execute) + ' END] \n'
                rospy.loginfo(msg)
                self.end += 1

            else:
                if self.myknowledge.iteration < int(self.myknowledge.service['iterations']):
                    msg = '[run_step ' + str(self.simulation.execute) + '] Running task: %d, iteration: %d\n' % (
                        self.myknowledge.service_id, self.myknowledge.iteration)
                    rospy.loginfo(msg)
                    self.myknowledge.iteration = self.myknowledge.iteration + 1
                    # Pause system for each iteration for some time - in order to have less iterations.
                    self.mycore.battery_change(
                        int(self.myknowledge.service['iterations']) / float(self.myknowledge.service['energy']))
                    # time.sleep(self.simulation.time)
                else:
                    msg = '[run_step ' + str(
                        self.simulation.execute) + '] Task: %d done\n' % self.myknowledge.service_id
                    rospy.loginfo(msg)
                    self.myknowledge.service_id = -1
                    self.myknowledge.iteration = -1
                    if random.random() <= self.myknowledge.service['simulation_finish']:
                        result = 1
                        self.myknowledge.completed_jobs += 1
                        self.simulation.no_tasks_completed[self.myknowledge.difficulty] += 1
                    else:
                        result = 2

                    # diminish by the energy required by the task
                    self.mycore.battery_change(
                        int(self.myknowledge.service['iterations']) / float(self.myknowledge.service['energy']))

                    # In case I am helping some other agent, trigger response here
                    msg = '[run_step ' + str(self.simulation.execute) + '] sender: %d, result: %d\n' % (
                        int(self.myknowledge.service['senderID']), result)
                    rospy.loginfo(msg)

                    # pdb.set_trace()
                    if self.amIHelping(int(self.myknowledge.service['senderID'])):
                        if result == 1:
                            self.simulation.requests_rec_success[self.myknowledge.difficulty] += 1
                        # You need to count loops
                        msg = '[run_step ' + str(self.simulation.execute) + '] service %s, threads: %s\n' % (
                            self.myknowledge.service, str(self.keep_track_threads))
                        rospy.loginfo(msg)

                        index = next(index for (index, d) in enumerate(self.keep_track_threads) if
                                     d['senderId'] == int(self.myknowledge.service['senderID']))

                        if self.is_thread_active(int(self.myknowledge.service['senderID'])):
                            if result == 1:
                                self.keep_track_threads[index]['task_status'] = 1
                            else:
                                self.keep_track_threads[index]['task_status'] = 2

                            msg = '[run_step ' + str(self.simulation.execute) + '] Threads %s\n' % str(
                                self.keep_track_threads)
                            rospy.loginfo(msg)
                        else:
                            self.keep_track_threads[index]['task_status'] = 10
                            msg = '[run_step ' + str(
                                self.simulation.execute) + '] End of task, but thread not active anymore. Threads %s\n' % str(
                                self.keep_track_threads)
                            rospy.loginfo(msg)
                    else:
                        if result == 1:
                            self.simulation.no_self_tasks_completed[self.myknowledge.difficulty] += 1

                    # Record
                    self.simulation.theta_esteem.append(performance)
                    self.simulation.theta_candidate.append(success_chance)
                    self.simulation.theta.append(gamma)
                    self.simulation.theta_bool.append(depend)
                    # Inc to reach stop of simulation

                    msg = '[run_step ' + str(self.simulation.execute) + ' END] \n'
                    rospy.loginfo(msg)
                    self.end += 1

        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()[0]) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))
            pass

    def execute_step_v5(self):
        try:
            self.begin += 1
            msg = '[run_step ' + str(self.simulation.execute) + ' BEGIN] in execute_step\n'
            rospy.loginfo(msg)
            # print 'in execute_step'
            # pdb.set_trace()

            # This returns the best candidate id, and success measure
            success_chance, candidate_id, candidate_idx = self.mycore.best_candidate(self.myknowledge.known_people,
                                                                                     self.myknowledge.service, self.log,
                                                                                     int(self.myknowledge.service[
                                                                                             'senderID']))
            msg = '[run_step ' + str(
                self.simulation.execute) + ' BEGIN] success %f, id %d, idx %d\n' % (
                success_chance, candidate_id, candidate_idx)
            rospy.loginfo(msg)

            # abil, equip, knowled, tools, env_risk, diff_task_progress = self.simulation.simulate_ask_params()

            msg = '[run_step %d] task abilities: %s, own abilities: %s\n' % (
                self.simulation.execute, self.myknowledge.service['abilities'], self.abilities)
            abil = 1

            for x in self.myknowledge.service['abilities']:
                if not x in self.abilities:
                    abil = 0
                    if x == 'transport_victim' and 'proxy' in self.abilities:
                        abil = 1
                    break
            equip = 1
            knowled = 1
            tools = 1
            msg += '[run_step %d] (consider on iteration) task resources: %s, own resources: %s\n' % (
                self.simulation.execute, self.myknowledge.service['resources'], self.resources)
            for x in self.myknowledge.service['resources']:
                if not x in self.resources:
                    tools = 0
                    break
                # elif self.myknowledge.service['resources'][x] > self.resources[x]:
                elif not self.myknowledge.service['resources'][x] <= 0:
                    if self.resources[x] / float(self.myknowledge.service['resources'][x]) == 0 or self.resources[
                        x] <= 0:
                        tools = 0  # in this case tools not enough!! -> in the context of the current iteration
                        break

            msg += '[run_step %d] abil: %d, tools: %d, no_att_tasks: %d\n' % (
                self.simulation.execute, abil, tools, sum(self.simulation.no_tasks_attempted))
            rospy.loginfo(msg)

            env_risk = 0

            if not self.myknowledge.service['iterations'] == 0:
                diff_task_progress = self.myknowledge.iteration / float(self.myknowledge.service['iterations'])
            else:
                diff_task_progress = 1

            # energy_diff = self.mycore.battery - float(self.myknowledge.service['energy'])
            # energy_diff = float(self.myknowledge.service['energy']-self.simulation.energy_iteration*self.myknowledge.iteration) - (self.mycore.battery - self.mycore.battery_min)
            energy_diff = self.simulation.energy_iteration - (self.mycore.battery - self.mycore.battery_min)

            if success_chance == -1.0:
                ag_risk = 0.0
            else:
                ag_risk = 1.0 - success_chance

            if success_chance == -1:
                success_chance = 0

            # if not sum(self.simulation.no_self_tasks_attempted) == 0:
            if not sum(self.simulation.no_tasks_attempted) == 0:
                # performance = sum(self.simulation.no_self_tasks_completed) / float(sum(self.simulation.no_self_tasks_attempted))
                performance = sum(self.simulation.no_tasks_completed) / float(
                    sum(self.simulation.no_tasks_attempted))
            else:
                performance = 1.0

            ###################################
            # pdb.set_trace()
            if self.static[0] == 0:
                self.myknowledge.lock.acquire()
                # depend, gamma = self.mycore.b_gamma(energy_diff, abil, equip, knowled, tools, env_risk, ag_risk,performance, diff_task_progress)
                # depend, gamma = self.mycore.gammaG(energy_diff, abil, equip, knowled, tools, env_risk, ag_risk,performance, diff_task_progress,self.myknowledge.service['iterations'], 0, candidate_id)
                depend, gamma = self.mycore.gamma3(energy_diff, abil, equip, knowled, tools, env_risk, ag_risk,
                                                   performance, diff_task_progress, 0, candidate_id)
                self.myknowledge.lock.release()
                self.myknowledge.service['simulation_finish'] = 1.0
            else:
                gamma = self.mycore.gamma
                if random.random() < gamma:
                    depend = True
                else:
                    depend = False
                    # if self.myknowledge.service['simulation_finish'] == -1.0:
                    if not abil or not equip or not knowled or not tools:
                        self.myknowledge.service['simulation_finish'] = 0.0
                        if not self.simulation.counted_d:
                            self.simulation.no_tasks_depend_attempted[self.myknowledge.difficulty] += 1
                            self.simulation.counted_d += 1
                    else:
                        self.myknowledge.service['simulation_finish'] = 1.0
            msg = '[run_step ' + str(self.simulation.execute) + '] ask for help: ' + str(depend) + '\n'
            msg += '[execute %d] abil = %f, equip = %f, knowled = %f, tools = %f, env_risk = %f, task-progress = %f, gamma = %f, sim-finish: %f, static: %f\n' % (
                self.simulation.execute, abil, equip, knowled, tools, env_risk, diff_task_progress, gamma,
                self.myknowledge.service['simulation_finish'], self.static[0]) + '\n'

            rospy.loginfo(msg)

            self.myknowledge.lock.acquire()
            # CAREFUL - appended performance with respect to dependent jobs
            if not sum(self.simulation.no_tasks_depend_attempted) == 0:
                depend_performance = sum(self.simulation.no_tasks_depend_completed) / float(
                    sum(self.simulation.no_tasks_depend_attempted))
            else:
                depend_performance = 1.0

            if not sum(self.simulation.no_self_tasks_attempted) == 0:
                own_performance = sum(self.simulation.no_self_tasks_completed) / float(
                    sum(self.simulation.no_self_tasks_attempted))
            else:
                own_performance = 1.0
            self.simulation.delta_theta.append(
                [1, gamma, depend, performance, depend_performance, own_performance, self.mycore.delta])
            self.myknowledge.lock.release()

            result = 0

            #################################
            #################################
            #################################
            if depend:
                self.simulation.no_tasks_depend_attempted[self.myknowledge.difficulty] += 1
                msg = '[run_step ' + str(self.simulation.execute) + 'tasks depend: ' + str(
                    sum(self.simulation.no_tasks_depend_attempted)) + '\n'
                rospy.loginfo(msg)

                if self.mycore.ID == self.myknowledge.service['senderID']:
                    self.simulation.no_tasks_depend_own_attempted[self.myknowledge.difficulty] += 1
                if not candidate_id == -1:

                    msg = '[run_step ' + str(
                        self.simulation.execute) + '] Ask for help. Difficulty: %f, delay: %f, addi: %f\n' % (
                        self.myknowledge.difficulty,
                        self.simulation.delay[self.myknowledge.difficulty],
                        self.simulation.additional_delay[self.myknowledge.difficulty])
                    rospy.loginfo(msg)
                    # pdb.set_trace()
                    agent2ask = '/robot' + str(candidate_id) + '/brain_node'
                    msg = '[run_step ' + str(
                        self.simulation.execute) + '] agent2ask is: ' + str(agent2ask) + '\n'
                    rospy.loginfo(msg)
                    ######### Make request to action_server
                    # self.call_action_server(self.myknowledge.service, agent2ask)
                    # print 'before blocking call'
                    self.myknowledge.service['iterations'] = self.myknowledge.service[
                                                                 'iterations'] - self.myknowledge.iteration + 1

                    self.simulation.neto_tasks_completed += (self.myknowledge.iteration - 1) / float(
                        self.myknowledge.service['noAgents'])
                    start = time.time()

                    result = self.call_blocking_action_server(self.myknowledge.service, agent2ask, candidate_idx)

                    # TIME THE SERVER'S RESPONSE!!
                    exec_time = time.time() - start

                    msg = '[run_step ' + str(self.simulation.execute) + '] exec_time: ' + str(exec_time) + '\n'
                    rospy.loginfo(msg)
                    self.myknowledge.service_id = -1
                    self.myknowledge.iteration = -1

                    # Assume that less energy is consumed when asking for help -- someone else is doing the deed
                    # self.mycore.battery_change(0.2 * int(self.myknowledge.service['energy']))

                    if result == 1:
                        msg = '[run_step ' + str(self.simulation.execute) + '] depend SUCCESS\n'
                        self.simulation.requests_success[self.myknowledge.difficulty] += 1

                        rospy.loginfo(msg)
                        self.simulation.exec_times[self.myknowledge.difficulty] = self.simulation.exec_times[
                                                                                      self.myknowledge.difficulty] + exec_time
                        self.simulation.exec_times_depend.append(exec_time)
                        self.simulation.no_tasks_depend_completed[self.myknowledge.difficulty] += 1
                        self.simulation.no_tasks_completed[self.myknowledge.difficulty] += 1
                        if self.mycore.ID == self.myknowledge.service['senderID']:
                            self.simulation.no_tasks_depend_own_completed[self.myknowledge.difficulty] += 1

                            # self.mycore.battery_change(0.2 * int(self.myknowledge.service['energy']))

                else:
                    # Count noones serves to identify those case in which the agent does not know anyone that could be of help
                    self.myknowledge.COUNT_noones[self.myknowledge.difficulty] += 1
                    self.myknowledge.service_id = -1
                    self.myknowledge.iteration = -1

                    # Assume that less energy is consumed when asking for help -- someone else is doing the deed
                    # self.mycore.battery_change(0.002 * int(self.myknowledge.service['energy']))

                    msg = '[run_step ' + str(self.simulation.execute) + '] No one to ask. Known people ' + str(
                        self.myknowledge.known_people) + '\n'
                    rospy.loginfo(msg)

                # In case I am helping some other agent, trigger response here
                msg = '[run_step ' + str(self.simulation.execute) + '] sender: %d, result: %d\n' % (
                    int(self.myknowledge.service['senderID']), result)
                rospy.loginfo(msg)

                # pdb.set_trace()
                if self.amIHelping(int(self.myknowledge.service['senderID'])):
                    if result == 1:
                        self.simulation.requests_rec_success[self.myknowledge.difficulty] += 1
                    # You need to count loops
                    msg = '[run_step ' + str(self.simulation.execute) + '] service %s, threads: %s\n' % (
                        self.myknowledge.service, str(self.keep_track_threads))
                    rospy.loginfo(msg)

                    index = next(index for (index, d) in enumerate(self.keep_track_threads) if
                                 d['senderId'] == int(self.myknowledge.service['senderID']))

                    if self.is_thread_active(int(self.myknowledge.service['senderID'])):
                        if result == 1:
                            self.keep_track_threads[index]['task_status'] = 1
                        else:
                            self.keep_track_threads[index]['task_status'] = 2

                        msg = '[run_step ' + str(self.simulation.execute) + '] Threads %s\n' % str(
                            self.keep_track_threads)
                        rospy.loginfo(msg)
                    else:
                        self.keep_track_threads[index]['task_status'] = 10
                        msg = '[run_step ' + str(
                            self.simulation.execute) + '] End of task, but thread not active anymore. Threads %s\n' % str(
                            self.keep_track_threads)
                        rospy.loginfo(msg)
                else:
                    if result == 1:
                        self.simulation.no_self_tasks_completed[self.myknowledge.difficulty] += 1

                # Record
                self.simulation.theta_esteem.append(performance)
                self.simulation.theta_candidate.append(success_chance)
                self.simulation.theta.append(gamma)
                self.simulation.theta_bool.append(depend)
                # Inc to reach stop of simulation

                msg = '[run_step ' + str(self.simulation.execute) + ' END] \n'
                rospy.loginfo(msg)
                self.end += 1

            else:
                if (self.myknowledge.iteration <= int(self.myknowledge.service['iterations'])) and ((
                                                                                                            'fire_extinguishing' in
                                                                                                            self.myknowledge.service[
                                                                                                                'abilities'] and not self.simulation.current_fire == -1000) \
                                                                                                            or (
                            'transport_victim' in self.myknowledge.service[
                            'abilities'] and not self.simulation.current_victim == -1000)):
                    # it is possible to check current known value for intensity
                    msg = '[run_step ' + str(self.simulation.execute) + '] Running task: %d, iteration: %d\n' % (
                        self.myknowledge.service_id, self.myknowledge.iteration)
                    rospy.loginfo(msg)

                    if self.myknowledge.iteration == 1:
                        self.walk(self.myknowledge.service['endLoc'][0], self.myknowledge.service['endLoc'][1])

                    self.myknowledge.iteration = self.myknowledge.iteration + 1
                    # Pause system for each iteration for some time - in order to have less iterations.
                    self.mycore.battery_change(self.simulation.energy_iteration)
                    # time.sleep(self.simulation.time)
                    # Put out a random fire
                    if 'fire_extinguishing' in self.myknowledge.service['abilities']:
                        if self.myknowledge.service['simulation_finish'] > 0:
                            rospy.wait_for_service('/environment/put_out')
                            try:
                                pof = rospy.ServiceProxy('/environment/put_out', Put_Out_Fire)
                                id = self.myknowledge.service['id']

                                msg = '[run_step ' + str(self.simulation.execute) + '] ' + str(
                                    self.simulation.fires) + ', simulation-finish: ' + str(
                                    self.myknowledge.service['simulation_finish']) + '\n'
                                rospy.loginfo(msg)

                                resp1 = pof(id, 1)
                                # msg = ''

                                for x in self.simulation.fires[0]:
                                    # msg += '\n' + str(type(x[0])) + ', ' + str(x[0]) + ', ' + str(int(self.myknowledge.service['id'])) + '\n'
                                    if x == int(self.myknowledge.service['id']):
                                        msg = '\n...' + str(x) + ', ' + str(int(self.myknowledge.service['id'])) + '\n'
                                        self.resources['water'] -= 1
                                        self.myknowledge.lock_cb.acquire()
                                        # pdb.set_trace()
                                        self.simulation.fires[3][x - 1] = resp1.current_intensity
                                        self.simulation.last_updated = time.time()
                                        self.myknowledge.lock_cb.release()
                                        self.simulation.current_fire = resp1.current_intensity
                                        self.myknowledge.service['resources'][
                                            'water'] -= 1  # this FLIES only when there's one ability involved
                                        break
                                msg += '[run_step ' + str(self.simulation.execute) + '] after putting out: ' + str(
                                    id) + ': ' + str(resp1.current_intensity) + '\n'
                                msg += '\n' + str(self.myknowledge.service) + '\n'
                                rospy.loginfo(msg)
                            except rospy.ServiceException, e:
                                msg = '[run_step ' + str(self.simulation.execute) + '] unexpected: %s\n' % e
                                rospy.loginfo(msg)
                    else:
                        if self.myknowledge.service['simulation_finish'] > 0:
                            rospy.wait_for_service('/environment/put_out')
                            try:
                                sv = rospy.ServiceProxy('/environment/save_victim', Save_Victim)
                                id = self.myknowledge.service['id']
                                msg = '[run_step ' + str(
                                    self.simulation.execute) + '] before calling carrying victims service: ' + str(
                                    self.simulation.fires) + '\n'
                                rospy.loginfo(msg)
                                resp1 = sv(id, 1)
                                for x in self.simulation.fires[0]:
                                    msg = '\n...' + str(x) + ', ' + str(
                                        int(self.myknowledge.service['id'])) + ' :' + str(
                                        x) + '\n'
                                    rospy.loginfo(msg)
                                    if x == int(self.myknowledge.service['id']):
                                        msg += '\n...>' + str(x) + ', ' + str(
                                            int(self.myknowledge.service['id'])) + '\n'
                                        self.myknowledge.lock_cb.acquire()
                                        self.simulation.fires[4][x - 1] = resp1.current_victims
                                        self.simulation.last_updated = time.time()
                                        self.resources['spotxPerson'] -= 1
                                        msg = '[run_step ' + str(self.simulation.execute) + '] : ' + str(
                                            self.simulation.fires) + ' :' + str(x) + '\n'
                                        rospy.loginfo(msg)
                                        self.myknowledge.lock_cb.release()
                                        self.simulation.current_victim = resp1.current_victims
                                        self.myknowledge.service['resources'][
                                            'spotxPerson'] -= 1  # this FLIES only when there's one ability involved
                                        break
                                msg = '[run_step ' + str(self.simulation.execute) + '] after carrying out: ' + str(
                                    id) + ': ' + str(resp1.current_victims) + '\n'
                                msg += '\n' + str(self.myknowledge.service) + '\n'
                                rospy.loginfo(msg)
                            except rospy.ServiceException, e:
                                msg = '[run_step ' + str(self.simulation.execute) + '] unexpected: %s\n' % e
                                rospy.loginfo(msg)

                else:
                    msg = '[run_step ' + str(
                        self.simulation.execute) + '] Task: %d done, other finish: %f, %f\n' % (
                        self.myknowledge.service_id, self.simulation.current_fire, self.simulation.current_victim)
                    rospy.loginfo(msg)

                    if random.random() < self.myknowledge.service['simulation_finish']:
                        result = 1
                        self.myknowledge.completed_jobs += 1
                        self.simulation.no_tasks_completed[self.myknowledge.difficulty] += 1
                        self.simulation.neto_tasks_completed += (self.myknowledge.iteration - 1) / float(
                            self.myknowledge.service['noAgents'])
                    else:
                        result = 2

                    self.myknowledge.service_id = -1
                    self.myknowledge.iteration = -1
                    # diminish by the energy required by the task
                    # self.mycore.battery_change(int(self.myknowledge.service['iterations']) / float(self.myknowledge.service['energy']))

                    # In case I am helping some other agent, trigger response here
                    msg = '[run_step ' + str(self.simulation.execute) + '] sender: %d, result: %d\n' % (
                        int(self.myknowledge.service['senderID']), result)
                    rospy.loginfo(msg)

                    # pdb.set_trace()
                    if self.amIHelping(int(self.myknowledge.service['senderID'])):
                        if result == 1:
                            # self.simulation.requests_rec_success[self.myknowledge.difficulty] += 1
                            pass
                        # You need to count loops
                        msg = '[run_step ' + str(self.simulation.execute) + '] service %s, threads: %s\n' % (
                            self.myknowledge.service, str(self.keep_track_threads))
                        rospy.loginfo(msg)

                        index = next(index for (index, d) in enumerate(self.keep_track_threads) if
                                     d['senderId'] == int(self.myknowledge.service['senderID']))

                        if self.is_thread_active(int(self.myknowledge.service['senderID'])):
                            if result == 1:
                                self.simulation.requests_rec_success[self.myknowledge.difficulty] += 1
                                self.keep_track_threads[index]['task_status'] = 1
                            else:
                                self.keep_track_threads[index]['task_status'] = 2

                            msg = '[run_step ' + str(self.simulation.execute) + '] Threads %s\n' % str(
                                self.keep_track_threads)
                            rospy.loginfo(msg)
                        else:
                            self.keep_track_threads[index]['task_status'] = 10
                            msg = '[run_step ' + str(
                                self.simulation.execute) + '] End of task, but thread not active anymore. Threads %s\n' % str(
                                self.keep_track_threads)
                            rospy.loginfo(msg)
                    else:
                        if result == 1:
                            self.simulation.no_self_tasks_completed[self.myknowledge.difficulty] += 1

                    # Record
                    self.simulation.theta_esteem.append(performance)
                    self.simulation.theta_candidate.append(success_chance)
                    self.simulation.theta.append(gamma)
                    self.simulation.theta_bool.append(depend)
                    # Inc to reach stop of simulation

                    msg = '[run_step ' + str(self.simulation.execute) + ' END] \n'
                    rospy.loginfo(msg)
                    self.end += 1

            if self.myknowledge.service_id == -1 and self.myknowledge.iteration == -1:
                if "fire_extinguishing" in self.abilities:
                    msg += '[run_step ' + str(self.simulation.execute) + '] water:' + str(
                        self.resources['water']) + '\n'
                    self.goto_base(1)
                    # self.resources['water'] = 25
                elif "transport_victim" or "proxy" in self.abilities:
                    msg += '[run_step ' + str(self.simulation.execute) + '] spots:' + str(
                        self.resources['spotxPerson']) + '\n'
                    self.goto_base(2)
                    # self.resources['spotxPerson'] = 5

        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()[0]) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))
            pass

    def execute_step_v6(self):
        try:
            self.begin += 1
            msg = '[run_step ' + str(self.simulation.execute) + ' BEGIN] in execute_step\n'
            rospy.loginfo(msg)
            success_chance = -1
            # print 'in execute_step'
            # pdb.set_trace()

            # This returns the best candidate id, and success measure
            agents2ask = self.mycore.best_candidate_list(self.myknowledge.known_people, self.myknowledge.service,
                                                         self.log, int(self.myknowledge.service['senderID']))
            msg = '[run_step ' + str(
                self.simulation.execute) + ' BEGIN] agents2ask %s\n' % (str(agents2ask))
            rospy.loginfo(msg)

            # abil, equip, knowled, tools, env_risk, diff_task_progress = self.simulation.simulate_ask_params()

            msg = '[run_step %d] task abilities: %s, own abilities: %s\n' % (
                self.simulation.execute, self.myknowledge.service['abilities'], self.abilities)
            abil = 1

            for x in self.myknowledge.service['abilities']:
                if not x in self.abilities:
                    abil = 0
                    if x == 'transport_victim' and 'proxy' in self.abilities:
                        abil = 1
                    break
            equip = 1
            knowled = 1
            tools = 1
            msg += '[run_step %d] (consider on iteration) task resources: %s, own resources: %s\n' % (
                self.simulation.execute, self.myknowledge.service['resources'], self.resources)
            for x in self.myknowledge.service['resources']:
                if not x in self.resources:
                    tools = 0
                    break
                # elif self.myknowledge.service['resources'][x] > self.resources[x]:
                elif not self.myknowledge.service['resources'][x] <= 0:
                    if self.resources[x] / float(self.myknowledge.service['resources'][x]) == 0 or self.resources[x] <= 0:
                        tools = 0  # in this case tools not enough!! -> in the context of the current iteration
                        break

            msg += '[run_step %d] abil: %d, tools: %d, no_att_tasks: %d\n' % (
                self.simulation.execute, abil, tools, sum(self.simulation.no_tasks_attempted))
            rospy.loginfo(msg)

            env_risk = 0

            if not self.myknowledge.service['iterations'] == 0:
                diff_task_progress = self.myknowledge.iteration / float(self.myknowledge.service['iterations'])
            else:
                diff_task_progress = 1

            # energy_diff = self.mycore.battery - float(self.myknowledge.service['energy'])
            # energy_diff = float(self.myknowledge.service['energy']-self.simulation.energy_iteration*self.myknowledge.iteration) - (self.mycore.battery - self.mycore.battery_min)
            energy_diff = self.simulation.energy_iteration - (self.mycore.battery - self.mycore.battery_min)

            if agents2ask[0][1] == -1.0:
                ag_risk = 0.0
            else:
                ag_risk = 1.0 - agents2ask[0][1]

            # if not sum(self.simulation.no_self_tasks_attempted) == 0:
            if not sum(self.simulation.no_tasks_attempted) == 0:
                # performance = sum(self.simulation.no_self_tasks_completed) / float(sum(self.simulation.no_self_tasks_attempted))
                performance = sum(self.simulation.no_tasks_completed) / float(
                    sum(self.simulation.no_tasks_attempted))
            else:
                performance = 1.0

            ###################################
            # pdb.set_trace()
            if self.static[0] == 0:
                self.myknowledge.lock.acquire()
                # depend, gamma = self.mycore.b_gamma(energy_diff, abil, equip, knowled, tools, env_risk, ag_risk,performance, diff_task_progress)
                # depend, gamma = self.mycore.gammaG(energy_diff, abil, equip, knowled, tools, env_risk, ag_risk,performance, diff_task_progress,self.myknowledge.service['iterations'], 0, candidate_id)
                depend, gamma = self.mycore.gamma3(energy_diff, abil, equip, knowled, tools, env_risk, ag_risk,
                                                   performance, diff_task_progress, 0, agents2ask[0][0])
                self.myknowledge.lock.release()
                self.myknowledge.service['simulation_finish'] = 1.0
            else:
                gamma = self.mycore.gamma
                if random.random() < gamma:
                    depend = True
                else:
                    depend = False
                    # if self.myknowledge.service['simulation_finish'] == -1.0:
                    if not abil or not equip or not knowled or not tools:
                        self.myknowledge.service['simulation_finish'] = 0.0
                        if not self.simulation.counted_d:
                            self.simulation.no_tasks_depend_attempted[self.myknowledge.difficulty] += 1
                            self.simulation.counted_d += 1
                    else:
                        self.myknowledge.service['simulation_finish'] = 1.0
            msg = '[run_step ' + str(self.simulation.execute) + '] ask for help: ' + str(depend) + '\n'
            msg += '[execute %d] abil = %f, equip = %f, knowled = %f, tools = %f, env_risk = %f, task-progress = %f, gamma = %f, sim-finish: %f, static: %f\n' % (
                self.simulation.execute, abil, equip, knowled, tools, env_risk, diff_task_progress, gamma,
                self.myknowledge.service['simulation_finish'], self.static[0]) + '\n'

            rospy.loginfo(msg)

            self.myknowledge.lock.acquire()
            # CAREFUL - appended performance with respect to dependent jobs
            if not sum(self.simulation.no_tasks_depend_attempted) == 0:
                depend_performance = sum(self.simulation.no_tasks_depend_completed) / float(
                    sum(self.simulation.no_tasks_depend_attempted))
            else:
                depend_performance = 1.0

            if not sum(self.simulation.no_self_tasks_attempted) == 0:
                own_performance = sum(self.simulation.no_self_tasks_completed) / float(
                    sum(self.simulation.no_self_tasks_attempted))
            else:
                own_performance = 1.0
            self.simulation.delta_theta.append(
                [1, gamma, depend, performance, depend_performance, own_performance, self.mycore.delta])
            self.myknowledge.lock.release()

            result = 0

            #################################
            #################################
            #################################
            if depend:
                self.simulation.no_tasks_depend_attempted[self.myknowledge.difficulty] += 1
                msg = '[run_step ' + str(self.simulation.execute) + 'tasks depend: ' + str(
                    sum(self.simulation.no_tasks_depend_attempted)) + '\n'
                rospy.loginfo(msg)

                if self.mycore.ID == self.myknowledge.service['senderID']:
                    self.simulation.no_tasks_depend_own_attempted[self.myknowledge.difficulty] += 1
                if agents2ask:
                    msg = '[run_step ' + str(
                        self.simulation.execute) + '] Ask for help. Difficulty: %f, delay: %f, addi: %f\n' % (
                        self.myknowledge.difficulty,
                        self.simulation.delay[self.myknowledge.difficulty],
                        self.simulation.additional_delay[self.myknowledge.difficulty])
                    rospy.loginfo(msg)
                    # pdb.set_trace()

                    for x in agents2ask:
                        msg = '[run_step ' + str(
                            self.simulation.execute) + '] agent2ask is: ' + str(x) + '\n'
                        rospy.loginfo(msg)
                        agent2ask = '/robot' + str(x[0]) + '/brain_node'
                        msg = '[run_step ' + str(
                            self.simulation.execute) + '] agent2ask is: ' + str(agent2ask) + '\n'
                        rospy.loginfo(msg)
                        ######### Make request to action_server
                        # self.call_action_server(self.myknowledge.service, agent2ask)
                        # print 'before blocking call'
                        self.myknowledge.service['iterations'] = self.myknowledge.service[
                                                                     'iterations'] - self.myknowledge.iteration + 1

                        start = time.time()

                        result = self.call_blocking_action_server(self.myknowledge.service, agent2ask, x[4])

                        # TIME THE SERVER'S RESPONSE!!
                        exec_time = time.time() - start

                        if result == 1:
                            success_chance = x[1]
                            self.simulation.neto_tasks_completed += (self.myknowledge.iteration - 1) / float(
                                self.myknowledge.service['noAgents'])
                            break

                        msg = '[run_step ' + str(self.simulation.execute) + '] exec_time: ' + str(exec_time) + '\n'
                        rospy.loginfo(msg)

                    self.myknowledge.service_id = -1
                    self.myknowledge.iteration = -1

                    # Assume that less energy is consumed when asking for help -- someone else is doing the deed
                    # self.mycore.battery_change(0.2 * int(self.myknowledge.service['energy']))

                    if result == 1:
                        msg = '[run_step ' + str(self.simulation.execute) + '] depend SUCCESS\n'
                        self.simulation.requests_success[self.myknowledge.difficulty] += 1

                        rospy.loginfo(msg)
                        self.simulation.exec_times[self.myknowledge.difficulty] = self.simulation.exec_times[
                                                                                      self.myknowledge.difficulty] + exec_time
                        self.simulation.exec_times_depend.append(exec_time)
                        self.simulation.no_tasks_depend_completed[self.myknowledge.difficulty] += 1
                        self.simulation.no_tasks_completed[self.myknowledge.difficulty] += 1
                        if self.mycore.ID == self.myknowledge.service['senderID']:
                            self.simulation.no_tasks_depend_own_completed[self.myknowledge.difficulty] += 1

                            # self.mycore.battery_change(0.2 * int(self.myknowledge.service['energy']))

                else:
                    # Count noones serves to identify those case in which the agent does not know anyone that could be of help
                    self.myknowledge.COUNT_noones[self.myknowledge.difficulty] += 1
                    self.myknowledge.service_id = -1
                    self.myknowledge.iteration = -1

                    # Assume that less energy is consumed when asking for help -- someone else is doing the deed
                    # self.mycore.battery_change(0.002 * int(self.myknowledge.service['energy']))

                    msg = '[run_step ' + str(self.simulation.execute) + '] No one to ask. Known people ' + str(
                        self.myknowledge.known_people) + '\n'
                    rospy.loginfo(msg)

                # In case I am helping some other agent, trigger response here
                msg = '[run_step ' + str(self.simulation.execute) + '] sender: %d, result: %d\n' % (
                    int(self.myknowledge.service['senderID']), result)
                rospy.loginfo(msg)

                # pdb.set_trace()
                if self.amIHelping(int(self.myknowledge.service['senderID'])):
                    if result == 1:
                        self.simulation.requests_rec_success[self.myknowledge.difficulty] += 1
                    # You need to count loops
                    msg = '[run_step ' + str(self.simulation.execute) + '] service %s, threads: %s\n' % (
                        self.myknowledge.service, str(self.keep_track_threads))
                    rospy.loginfo(msg)

                    index = next(index for (index, d) in enumerate(self.keep_track_threads) if
                                 d['senderId'] == int(self.myknowledge.service['senderID']))

                    if self.is_thread_active(int(self.myknowledge.service['senderID'])):
                        if result == 1:
                            self.keep_track_threads[index]['task_status'] = 1
                        else:
                            self.keep_track_threads[index]['task_status'] = 2

                        msg = '[run_step ' + str(self.simulation.execute) + '] Threads %s\n' % str(
                            self.keep_track_threads)
                        rospy.loginfo(msg)
                    else:
                        self.keep_track_threads[index]['task_status'] = 10
                        msg = '[run_step ' + str(
                            self.simulation.execute) + '] End of task, but thread not active anymore. Threads %s\n' % str(
                            self.keep_track_threads)
                        rospy.loginfo(msg)
                else:
                    if result == 1:
                        self.simulation.no_self_tasks_completed[self.myknowledge.difficulty] += 1

                # Record
                self.simulation.theta_esteem.append(performance)
                self.simulation.theta_candidate.append(success_chance)
                self.simulation.theta.append(gamma)
                self.simulation.theta_bool.append(depend)
                # Inc to reach stop of simulation

                msg = '[run_step ' + str(self.simulation.execute) + ' END] \n'
                rospy.loginfo(msg)
                self.end += 1

            else:
                if (self.myknowledge.iteration <= int(self.myknowledge.service['iterations'])) and (
                    ('fire_extinguishing' in self.myknowledge.service[
                        'abilities'] and not self.simulation.current_fire == -1000) or (
                                'transport_victim' in self.myknowledge.service[
                                'abilities'] and not self.simulation.current_victim == -1000)):
                    # it is possible to check current known value for intensity
                    msg = '[run_step ' + str(self.simulation.execute) + '] Running task: %d, iteration: %d\n' % (
                        self.myknowledge.service_id, self.myknowledge.iteration)
                    rospy.loginfo(msg)

                    if self.myknowledge.iteration == 1:
                        self.walk(self.myknowledge.service['endLoc'][0], self.myknowledge.service['endLoc'][1])

                    self.myknowledge.iteration = self.myknowledge.iteration + 1
                    # Pause system for each iteration for some time - in order to have less iterations.
                    self.mycore.battery_change(self.simulation.energy_iteration)
                    # time.sleep(self.simulation.time)
                    # Put out a random fire
                    if 'fire_extinguishing' in self.myknowledge.service['abilities']:
                        if self.myknowledge.service['simulation_finish'] > 0:
                            rospy.wait_for_service('/environment/put_out')
                            try:
                                pof = rospy.ServiceProxy('/environment/put_out', Put_Out_Fire)
                                id = self.myknowledge.service['id']

                                msg = '[run_step ' + str(self.simulation.execute) + '] ' + str(
                                    self.simulation.fires) + ', simulation-finish: ' + str(
                                    self.myknowledge.service['simulation_finish']) + '\n'
                                rospy.loginfo(msg)

                                resp1 = pof(id, 1)
                                # msg = ''

                                for x in self.simulation.fires[0]:
                                    # msg += '\n' + str(type(x[0])) + ', ' + str(x[0]) + ', ' + str(int(self.myknowledge.service['id'])) + '\n'
                                    if x == int(self.myknowledge.service['id']):
                                        msg = '\n...' + str(x) + ', ' + str(int(self.myknowledge.service['id'])) + '\n'
                                        self.resources['water'] -= 1
                                        self.myknowledge.lock_cb.acquire()
                                        # pdb.set_trace()
                                        self.simulation.fires[3][x - 1] = resp1.current_intensity
                                        self.simulation.last_updated = time.time()
                                        self.myknowledge.lock_cb.release()
                                        self.simulation.current_fire = resp1.current_intensity
                                        self.myknowledge.service['resources'][
                                            'water'] -= 1  # this FLIES only when there's one ability involved
                                        break
                                msg += '[run_step ' + str(self.simulation.execute) + '] after putting out: ' + str(
                                    id) + ': ' + str(resp1.current_intensity) + '\n'
                                msg += '\n' + str(self.myknowledge.service) + '\n'
                                rospy.loginfo(msg)
                            except rospy.ServiceException, e:
                                msg = '[run_step ' + str(self.simulation.execute) + '] unexpected: %s\n' % e
                                rospy.loginfo(msg)
                    else:
                        if self.myknowledge.service['simulation_finish'] > 0:
                            rospy.wait_for_service('/environment/put_out')
                            try:
                                sv = rospy.ServiceProxy('/environment/save_victim', Save_Victim)
                                id = self.myknowledge.service['id']
                                msg = '[run_step ' + str(
                                    self.simulation.execute) + '] before calling carrying victims service: ' + str(
                                    self.simulation.fires) + '\n'
                                rospy.loginfo(msg)
                                resp1 = sv(id, 1)
                                for x in self.simulation.fires[0]:
                                    msg = '\n...' + str(x) + ', ' + str(
                                        int(self.myknowledge.service['id'])) + ' :' + str(
                                        x) + '\n'
                                    rospy.loginfo(msg)
                                    if x == int(self.myknowledge.service['id']):
                                        msg += '\n...>' + str(x) + ', ' + str(
                                            int(self.myknowledge.service['id'])) + '\n'
                                        self.myknowledge.lock_cb.acquire()
                                        self.simulation.fires[4][x - 1] = resp1.current_victims
                                        self.simulation.last_updated = time.time()
                                        self.resources['spotxPerson'] -= 1
                                        msg = '[run_step ' + str(self.simulation.execute) + '] : ' + str(
                                            self.simulation.fires) + ' :' + str(x) + '\n'
                                        rospy.loginfo(msg)
                                        self.myknowledge.lock_cb.release()
                                        self.simulation.current_victim = resp1.current_victims
                                        self.myknowledge.service['resources'][
                                            'spotxPerson'] -= 1  # this FLIES only when there's one ability involved
                                        break
                                msg = '[run_step ' + str(self.simulation.execute) + '] after carrying out: ' + str(
                                    id) + ': ' + str(resp1.current_victims) + '\n'
                                msg += '\n' + str(self.myknowledge.service) + '\n'
                                rospy.loginfo(msg)
                            except rospy.ServiceException, e:
                                msg = '[run_step ' + str(self.simulation.execute) + '] unexpected: %s\n' % e
                                rospy.loginfo(msg)

                else:
                    msg = '[run_step ' + str(
                        self.simulation.execute) + '] Task: %d done, other finish: %f, %f\n' % (
                        self.myknowledge.service_id, self.simulation.current_fire, self.simulation.current_victim)
                    rospy.loginfo(msg)

                    if random.random() < self.myknowledge.service['simulation_finish']:
                        result = 1
                        self.myknowledge.completed_jobs += 1
                        self.simulation.no_tasks_completed[self.myknowledge.difficulty] += 1
                        self.simulation.neto_tasks_completed += (self.myknowledge.iteration - 1) / float(
                            self.myknowledge.service['noAgents'])
                    else:
                        result = 2

                    self.myknowledge.service_id = -1
                    self.myknowledge.iteration = -1
                    # diminish by the energy required by the task
                    # self.mycore.battery_change(int(self.myknowledge.service['iterations']) / float(self.myknowledge.service['energy']))

                    # In case I am helping some other agent, trigger response here
                    msg = '[run_step ' + str(self.simulation.execute) + '] sender: %d, result: %d\n' % (
                        int(self.myknowledge.service['senderID']), result)
                    rospy.loginfo(msg)

                    # pdb.set_trace()
                    if self.amIHelping(int(self.myknowledge.service['senderID'])):
                        if result == 1:
                            # self.simulation.requests_rec_success[self.myknowledge.difficulty] += 1
                            pass
                        # You need to count loops
                        msg = '[run_step ' + str(self.simulation.execute) + '] service %s, threads: %s\n' % (
                            self.myknowledge.service, str(self.keep_track_threads))
                        rospy.loginfo(msg)

                        index = next(index for (index, d) in enumerate(self.keep_track_threads) if
                                     d['senderId'] == int(self.myknowledge.service['senderID']))

                        if self.is_thread_active(int(self.myknowledge.service['senderID'])):
                            if result == 1:
                                self.simulation.requests_rec_success[self.myknowledge.difficulty] += 1
                                self.keep_track_threads[index]['task_status'] = 1
                            else:
                                self.keep_track_threads[index]['task_status'] = 2

                            msg = '[run_step ' + str(self.simulation.execute) + '] Threads %s\n' % str(
                                self.keep_track_threads)
                            rospy.loginfo(msg)
                        else:
                            self.keep_track_threads[index]['task_status'] = 10
                            msg = '[run_step ' + str(
                                self.simulation.execute) + '] End of task, but thread not active anymore. Threads %s\n' % str(
                                self.keep_track_threads)
                            rospy.loginfo(msg)
                    else:
                        if result == 1:
                            self.simulation.no_self_tasks_completed[self.myknowledge.difficulty] += 1

                    # Record
                    self.simulation.theta_esteem.append(performance)
                    self.simulation.theta_candidate.append(success_chance)
                    self.simulation.theta.append(gamma)
                    self.simulation.theta_bool.append(depend)
                    # Inc to reach stop of simulation

                    msg = '[run_step ' + str(self.simulation.execute) + ' END] \n'
                    rospy.loginfo(msg)
                    self.end += 1

            if self.myknowledge.service_id == -1 and self.myknowledge.iteration == -1:
                if "fire_extinguishing" in self.abilities:
                    msg += '[run_step ' + str(self.simulation.execute) + '] water:' + str(
                        self.resources['water']) + '\n'
                    self.goto_base(1)
                    # self.resources['water'] = 25
                elif "transport_victim" or "proxy" in self.abilities:
                    msg += '[run_step ' + str(self.simulation.execute) + '] spots:' + str(
                        self.resources['spotxPerson']) + '\n'
                    self.goto_base(2)
                    # self.resources['spotxPerson'] = 5

        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()[0]) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))
            pass

    def regenerate(self):
        # print 'im in regenerate'
        self.simulation.regenerate = self.simulation.inc_iterationstamps(self.simulation.regenerate)
        self.myknowledge.lock.acquire()
        self.mycore.state = 0
        self.myknowledge.lock.release()
        # self.mycore.battery += 400000 - self.mycore.battery
        self.mycore.battery = 1
        msg = '[fsm_INFO] I am in regenrate, switch to idle, state changed to %d, energy acquired %d' % (
            self.mycore.state, self.mycore.battery)
        rospy.loginfo(msg)
        self.simulation.count_recharge += 1
        self.debug_self()
        self.fix_bugs()

    def dead(self):
        # print 'im in dead'
        self.simulation.dead = self.simulation.inc_iterationstamps(self.simulation.dead)
        self.log.write_log_file(self.log.stdout_log, 'In dead - should return')

        self.evaluate_self()
        self.evaluate_environment()
        self.evaluate_selfmending()

        self.myknowledge.lock.acquire()
        self.mycore.state = 3
        self.myknowledge.lock.release()

        msg = '[fsm_INFO] I am in dead, switch to regenerate, state changed to %d' % self.mycore.state
        rospy.loginfo(msg)

        '''
        self.publish_bcast[0].publish(self.mycore.create_message('DIE', 'DIE'))
        self.reason = 'Simulation end - in the dead state'
        rospy.signal_shutdown(self.reason)
        rospy.on_shutdown(self.my_hook)
        '''

    # this implements a levy flight/walk - make this bounded!
    # Targeted at police officers
    def levy_walk_step(self, bounded):
        alpha = 1.5
        theta = random.random() * 2 * math.pi
        f = math.pow(random.random(), (-1 / alpha))
        oldX = self.myknowledge.position2D[0]
        oldY = self.myknowledge.position2D[1]

        if bounded:  # bounded within region
            # VERY BAD SOLUTION - fix it
            if self.mycore.ID == 17:
                d = [0, 0]
            elif self.mycore.ID == 18:
                d = [0, 1]
            elif self.mycore.ID == 19:
                d = [1, 1]
            elif self.mycore.ID == 20:
                d = [1, 0]

            if self.myknowledge.position2D[0] + f * math.cos(theta) < d[0] * 15:
                self.myknowledge.position2D[0] = d[0] * 15
            elif self.myknowledge.position2D[0] + f * math.cos(theta) > (d[0] + 1) * 15:
                self.myknowledge.position2D[0] = (d[0] + 1) * 15
            else:
                self.myknowledge.position2D[0] = self.myknowledge.position2D[0] + f * math.cos(theta)

            if self.myknowledge.position2D[1] + f * math.sin(theta) < d[1] * 15:
                self.myknowledge.position2D[1] = d[1] * 15
            elif self.myknowledge.position2D[1] + f * math.sin(theta) > (d[1] + 1) * 15:
                self.myknowledge.position2D[1] = (d[1] + 1) * 15
            else:
                self.myknowledge.position2D[1] = self.myknowledge.position2D[1] + f * math.sin(theta)
            msg = '[levy_walk] un-bounded: newX: %f, newY: %f, oldX: %f, oldY: %f, finalX: %f, finalY: %f\n' % (
                self.myknowledge.position2D[0] + f * math.cos(theta),
                self.myknowledge.position2D[1] + f * math.sin(theta), oldX, oldY, self.myknowledge.position2D[0],
                self.myknowledge.position2D[1])

            rospy.loginfo(msg)
            self.simulation.levywalk.append([self.myknowledge.position2D[0], self.myknowledge.position2D[1]])
        else:  # bounded within the whole grid
            # pdb.set_trace()
            if self.myknowledge.position2D[0] + f * math.cos(theta) < 0:
                self.myknowledge.position2D[0] = 0
            elif self.myknowledge.position2D[0] + f * math.cos(theta) > 30:
                self.myknowledge.position2D[0] = 30
            else:
                self.myknowledge.position2D[0] = self.myknowledge.position2D[0] + f * math.cos(theta)

            if self.myknowledge.position2D[1] + f * math.sin(theta) < 0:
                self.myknowledge.position2D[1] = 0
            elif self.myknowledge.position2D[1] + f * math.sin(theta) > 30:
                self.myknowledge.position2D[1] = 30
            else:
                self.myknowledge.position2D[1] = self.myknowledge.position2D[1] + f * math.sin(theta)
            msg = '[levy_walk] un-bounded: newX: %f, newY: %f, oldX: %f, oldY: %f, finalX: %f, finalY: %f\n' % (
                self.myknowledge.position2D[0] + f * math.cos(theta),
                self.myknowledge.position2D[1] + f * math.sin(theta), oldX, oldY, self.myknowledge.position2D[0],
                self.myknowledge.position2D[1])

            rospy.loginfo(msg)
            self.simulation.levywalk.append([self.myknowledge.position2D[0], self.myknowledge.position2D[1]])

        distance = math.sqrt(
            (self.myknowledge.position2D[0] - oldX) ** 2 + (self.myknowledge.position2D[1] - oldY) ** 2)
        time_for_walk = self.simulation.hR2sS * distance / float(self.myknowledge.speed[0])
        time.sleep(time_for_walk)

        # self.mycore.battery -= distance

        msg += '[levy_walk] d: %f, time: %f\n' % (distance, time_for_walk)
        rospy.loginfo(msg)

        location = Track_Loc()
        location.id = self.mycore.ID
        location.xpos = self.myknowledge.position2D[0]
        location.ypos = self.myknowledge.position2D[1]
        self.publish_loc.publish(location)

    # Targeted at police officers - OLD GRID_SIZE
    def random_walk_custom(self):

        if self.mycore.ID == 17:
            d = [0, 0]
        elif self.mycore.ID == 18:
            d = [0, 1]
        elif self.mycore.ID == 19:
            d = [1, 1]
        elif self.mycore.ID == 20:
            d = [1, 0]

        dx = random.randint(1, 10)
        dy = random.randint(1, 10)

        oldx = self.myknowledge.position2D[0]
        oldy = self.myknowledge.position2D[1]

        if self.myknowledge.position2D[0] + dx > d[0] * 50 and self.myknowledge.position2D[0] + dx < (
            d[0] + 1) * 50:  # 10 is the width of the space
            self.myknowledge.position2D[0] = self.myknowledge.position2D[0] + dx

        if self.myknowledge.position2D[1] + dy > d[1] * 50 and self.myknowledge.position2D[1] + dy < (
            d[0] + 1) * 50:  # 10 is the height of the space
            self.myknowledge.position2D[1] = self.myknowledge.position2D[1] + dy

        # self.mycore.battery -= math.sqrt((self.myknowledge.position2D[0] - oldx) ** 2 + (self.myknowledge.position2D[1] - oldy) ** 2)

        msg = '[random_walk] oldx: %f, oldy: %f, dx: %f, dy: %f, x: %f, y:%f\n' % (
            oldx, oldy, dx, dy, self.myknowledge.position2D[0], self.myknowledge.position2D[1])

        rospy.loginfo(msg)

        location = Track_Loc()
        location.id = self.mycore.ID
        location.xpos = self.myknowledge.position2D[0]
        location.ypos = self.myknowledge.position2D[1]
        self.publish_loc.publish(location)

    # OLD GRID_SIZE
    def random_walk(self):  # take energy unit for walking, 1 energy unit, 1 unit distance covered
        dx = random.randint(20, 50)
        dy = random.randint(20, 50)

        oldx = self.myknowledge.position2D[0]
        oldy = self.myknowledge.position2D[1]

        if self.myknowledge.position2D[0] + dx > 100:  # 10 is the width of the space
            self.myknowledge.position2D[0] = self.myknowledge.position2D[0] + dx - 100
        else:
            self.myknowledge.position2D[0] += dx

        if self.myknowledge.position2D[1] + dy > 100:  # 10 is the height of the space
            self.myknowledge.position2D[1] = self.myknowledge.position2D[1] + dy - 100
        else:
            self.myknowledge.position2D[1] += dy

        # self.mycore.battery -= math.sqrt((self.myknowledge.position2D[0] - oldx) ** 2 + (self.myknowledge.position2D[1] - oldy) ** 2)

        msg = '[random_walk] oldx: %f, oldy: %f, dx: %f, dy: %f, x: %f, y:%f\n' % (
            oldx, oldy, dx, dy, self.myknowledge.position2D[0], self.myknowledge.position2D[1])

        rospy.loginfo(msg)

        location = Track_Loc()
        location.id = self.mycore.ID
        location.xpos = self.myknowledge.position2D[0]
        location.ypos = self.myknowledge.position2D[1]
        self.publish_loc.publish(location)

    def walk(self, destx, desty):
        distance = math.sqrt(
            (self.myknowledge.position2D[0] - destx - 1) ** 2 + (self.myknowledge.position2D[1] - desty - 1) ** 2)
        # self.mycore.battery -= distance
        self.myknowledge.position2D[0] = destx - 1
        self.myknowledge.position2D[1] = desty - 1
        msg = '[walk] oldx: %f, oldy: %f, x: %f, y:%f\n' % (
            destx, desty, self.myknowledge.position2D[0], self.myknowledge.position2D[1])

        time_for_walk = self.simulation.hR2sS * distance / float(self.myknowledge.speed[1])
        time.sleep(time_for_walk)

        msg += '[walk] d: %f, time: %f\n' % (distance, time_for_walk)
        rospy.loginfo(msg)
        self.simulation.walk.append([self.myknowledge.position2D[0], self.myknowledge.position2D[1]])
        location = Track_Loc()
        location.id = self.mycore.ID
        location.xpos = self.myknowledge.position2D[0]
        location.ypos = self.myknowledge.position2D[1]
        self.publish_loc.publish(location)

    # type = 1 (fire base), type = 2 (ambulance base)
    # for now we have one of each
    def goto_base(self, type):
        # pdb.set_trace()
        msg = 'goto_base'
        self.simulation.count_gotobase += 1
        if type == 1:
            self.walk(self.simulation.fbase[1][0], self.simulation.fbase[2][0])
            self.resources['water'] = 25
            msg = '[goto_base ' + str(self.simulation.execute) + '] water:' + str(self.resources['water']) + '\n'
            time.sleep(self.simulation.water_refurnish_time)
        elif type == 2:
            self.walk(self.simulation.abase[1][0], self.simulation.fbase[2][0])
            self.resources['spotxPerson'] = 5
            msg = '[goto_base ' + str(self.simulation.execute) + '] spots:' + str(self.resources['spotxPerson']) + '\n'
            time.sleep(self.simulation.drop_victims_base)
        else:
            pass
        rospy.loginfo(msg)

    # MUST be overridden in the child class, depending on the different types of inputs!
    def init_inputs(self, inputs):
        pass

    def init_outputs(self, outputs):
        for x in outputs:
            self.publish_bcast.append(rospy.Publisher(x, Protocol_Msg, queue_size=200))
            # print self.publish_bcast

    def generate_goal(self):
        if random.random() > 0.8:
            senderId = self.mycore.ID
            planId = -random.randint(1, 100)
            tID = random.randint(1, 10)
            iterations = random.randint(1, 100)
            energy = random.randint(1, 100)
            reward = random.randint(1, 100)
            tName = 'randomCrap'
            startLoc = [2, 3]
            endLoc = [5, 6]
            noAgents = random.randint(1, 100)
            equipment = [['pip'], ['pop'], ['pup']]
            abilities = ['halloumi']
            res = ['mozarella']
            estim_time = random.random() * random.randint(1, 100)

            tasks = [{'abilities': abilities, 'estim_time': estim_time, 'senderID': senderId, 'energy': energy,
                      'iterations': iterations, 'id': tID, 'name': tName, 'endLoc': endLoc, 'planID': planId,
                      'equipment': equipment, 'startLoc': startLoc, 'resources': res,
                      'reward': reward, 'noAgents': noAgents}]

            self.log.write_log_file(self.log.stdout_log,
                                    '[generate goal ' + str(self.simulation.idle) + '] Chosen service: ' + str(
                                        tasks) + '\n')

            for x in tasks:
                self.log.write_log_file(self.log.stdout_log,
                                        '[generate goal ' + str(self.simulation.interact) + '] ' + str(x) + '\n')
                self.myknowledge.task_queue.put(x)

            self.myknowledge.lock.acquire()
            self.mycore.state = 2
            self.myknowledge.attempted_jobs += 1
            self.myknowledge.lock.release()
        else:
            self.log.write_log_file(self.log.stdout_log, '[generate goal ' + str(
                self.simulation.idle) + '] do nothing - zot jepi atij qe rri kot :DD\n')

    def generate_goal_v2(self):
        try:
            self.begin += 1
            if random.random() < 0.001:
                it = [10, 10, 10]
                en = [1, 10, 30]
                re = [50, 150, 350]
                ab = [['walk'], ['walk', 'talk'], ['walk', 'talk', 'smoke']]
                risurs = [['pringles'], ['pringles', 'brie'], ['pringles', 'brie', 'beer']]
                etime = [130, 1300, 2300]

                difficulty = random.randint(0, 2)

                msg = '[generate goal ' + str(self.simulation.idle) + ' BEGIN] ' + str(
                    self.simulation.no_self_tasks_attempted) + ' difficulty: ' + str(difficulty) + '\n'
                rospy.loginfo(msg)

                senderId = self.mycore.ID
                acSenderId = [self.mycore.ID]
                planId = -random.randint(1, 100)
                tID = random.randint(1, 9)
                iterations = it[difficulty]
                energy = en[difficulty]
                reward = re[difficulty]
                tName = 'randomCrap'
                startLoc = [2, 3]
                endLoc = [5, 6]
                noAgents = random.randint(1, 100)
                equipment = [['pip'], ['pop'], ['pup']]
                abilities = ab[difficulty]
                res = risurs[difficulty]
                estim_time = etime[difficulty]
                simulation_finish = -1.0

                tasks = [{'abilities': abilities, 'estim_time': estim_time, 'senderID': senderId, 'energy': energy,
                          'iterations': iterations, 'id': tID, 'name': tName, 'endLoc': endLoc, 'planID': planId,
                          'equipment': equipment, 'startLoc': startLoc, 'reward': reward, 'resources': res,
                          'simulation_finish': simulation_finish, 'noAgents': noAgents, 'ac_senders': acSenderId}]

                # msg = '[generate goal ' + str(self.simulation.idle) + '] Chosen service: ' + str(tasks) + '\n'
                # rospy.loginfo(msg)

                for x in tasks:
                    msg = '[generate goal ' + str(self.simulation.idle) + '] ' + str(x) + '\n'
                    rospy.loginfo(msg)
                    self.myknowledge.task_queue.put(x)

                self.myknowledge.lock.acquire()
                self.mycore.state = 2
                self.myknowledge.lock.release()
            else:
                # msg = '[generate goal ' + str(self.simulation.idle) + '] do nothing - zot jepi atij qe rri kot :DD\n'
                # rospy.loginfo(msg)
                pass

            msg = '[generate goal ' + str(self.simulation.idle) + ' END]\n'
            rospy.loginfo(msg)
            self.end += 1

        except:
            rospy.loginfo("Unexpected error: " + str(sys.exc_info()[0]))
            pass

    def pick_task(self, visible_tasks):
        try:
            pick = False
            while not pick:
                # data.id, data.xpos, data.ypos, data.intensity, data.victims, data.status
                idx = random.randint(0, visible_tasks.shape[0] - 1)
                # if ((visible_tasks[idx][1] - self.myknowledge.position2D[0]) ** 2 + (visible_tasks[idx][2] - self.myknowledge.position2D[1]) ** 2) < self.mycore.battery ** 2:
                if visible_tasks[idx][3] * self.simulation.energy_iteration < self.mycore.battery:
                    msg = '[generate tailored goal ' + str(
                        self.simulation.idle) + '] iterations: %f, energy x iteration: %f, total energy: %f, battery level: %f\n' % (
                        visible_tasks[idx][3], self.simulation.energy_iteration,
                        visible_tasks[idx][3] * self.simulation.energy_iteration, self.mycore.battery)
                    rospy.loginfo(msg)
                    pick = True
            return idx
        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))

    def generate_goal_v3(self):
        try:
            # Generate a task based on the fires and victims to be saved
            if "fire_extinguishing" in self.abilities:
                visible_fires = np.transpose(np.array(self.get_visible_fires()))

                if visible_fires.size:
                    if self.simulation.time_started == 0:
                        self.simulation.time_started = time.time()
                    # Pick a fire randomly
                    msg = '[generate goal ' + str(self.simulation.idle) + '] ' + str(visible_fires) + '\n'
                    rospy.loginfo(msg)
                    vf_id = self.pick_task(visible_fires)

                    senderId = self.mycore.ID
                    acSenderId = [self.mycore.ID]
                    planId = -random.randint(1, 100)
                    tID = visible_fires[vf_id][0]

                    # energy = math.sqrt((self.myknowledge.position2D[0] - visible_fires[vf_id][1]) ** 2 + (self.myknowledge.position2D[1] - visible_fires[vf_id][2]) ** 2)
                    endLoc = [visible_fires[vf_id][1], visible_fires[vf_id][2]]
                    startLoc = [self.myknowledge.position2D[0], self.myknowledge.position2D[1]]
                    reward = visible_fires[vf_id][3]
                    res = {'water': visible_fires[vf_id][3]}
                    iterations = math.ceil(visible_fires[vf_id][3] / float(self.simulation.extinguish_step))
                    energy = iterations * self.simulation.energy_iteration

                    tName = 'extinguish'
                    noAgents = random.randint(1, 100)
                    equipment = [['pip'], ['pop'], ['pup']]
                    abilities = {'fire_extinguishing': 1.0}
                    estim_time = 100  # jibberish value
                    simulation_finish = -1.0

                    # noagents serves for original nr of iterations
                    tasks = [{'abilities': abilities, 'estim_time': estim_time, 'senderID': senderId, 'energy': energy,
                              'iterations': iterations, 'id': tID, 'name': tName, 'endLoc': endLoc, 'planID': planId,
                              'equipment': equipment, 'startLoc': startLoc, 'reward': reward, 'resources': res,
                              'simulation_finish': simulation_finish, 'noAgents': int(iterations),
                              'ac_senders': acSenderId}]

                    msg = '[generate goal ' + str(self.simulation.idle) + '] Chosen service: ' + str(tasks) + '\n'
                    rospy.loginfo(msg)

                    for x in tasks:
                        msg = '[generate goal ' + str(self.simulation.idle) + '] ' + str(x) + '\n'
                        rospy.loginfo(msg)
                        self.myknowledge.task_queue.put(x)

                    now = time.time()
                    self.simulation.time_per_task.append(now - self.simulation.time_started)
                    self.simulation.time_started = now

                    self.myknowledge.lock.acquire()
                    self.mycore.state = 2
                    self.myknowledge.lock.release()
            elif "transport_victim" in self.abilities:
                visible_victims = np.transpose(np.array(self.get_visible_victims()))

                if visible_victims.size:
                    if self.simulation.time_started == 0:
                        self.simulation.time_started = time.time()
                    # Pick a victim location randomly
                    msg = '[generate goal ' + str(self.simulation.idle) + '] ' + str(visible_victims) + '\n'
                    rospy.loginfo(msg)
                    vf_id = self.pick_task(visible_victims)

                    senderId = self.mycore.ID
                    acSenderId = [self.mycore.ID]
                    planId = -random.randint(1, 100)
                    tID = visible_victims[vf_id][0]

                    # energy = math.sqrt((self.myknowledge.position2D[0] - visible_victims[vf_id][1]) ** 2 + (self.myknowledge.position2D[1] - visible_victims[vf_id][2]) ** 2)
                    endLoc = [visible_victims[vf_id][1], visible_victims[vf_id][2]]
                    startLoc = [self.myknowledge.position2D[0], self.myknowledge.position2D[1]]
                    reward = visible_victims[vf_id][4]
                    res = {'spotxPerson': visible_victims[vf_id][4]}
                    iterations = visible_victims[vf_id][4]
                    energy = iterations * self.simulation.energy_iteration

                    tName = 'extinguish'
                    noAgents = random.randint(1, 100)
                    equipment = [['pip'], ['pop'], ['pup']]
                    abilities = {'transport_victim': 1.0}
                    estim_time = 100  # jibberish value
                    simulation_finish = -1.0

                    # noagents serves for original nr of iterations
                    tasks = [{'abilities': abilities, 'estim_time': estim_time, 'senderID': senderId, 'energy': energy,
                              'iterations': iterations, 'id': tID, 'name': tName, 'endLoc': endLoc, 'planID': planId,
                              'equipment': equipment, 'startLoc': startLoc, 'reward': reward, 'resources': res,
                              'simulation_finish': simulation_finish, 'noAgents': int(iterations),
                              'ac_senders': acSenderId}]

                    msg = '[generate goal ' + str(self.simulation.idle) + '] Chosen service: ' + str(tasks) + '\n'
                    rospy.loginfo(msg)

                    for x in tasks:
                        msg = '[generate goal ' + str(self.simulation.idle) + '] ' + str(x) + '\n'
                        rospy.loginfo(msg)
                        self.myknowledge.task_queue.put(x)

                    now = time.time()
                    self.simulation.time_per_task.append(now - self.simulation.time_started)
                    self.simulation.time_started = now

                    self.myknowledge.lock.acquire()
                    self.mycore.state = 2
                    self.myknowledge.lock.release()
        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))
            pass

    def plan2goal(self):
        pass

    def commit2goal(self):
        pass

    def evaluate_my_state(self):
        pass

    def evaluate_agent(self):
        pass

    def evaluate_request(self):
        pass

    def commit2agent(self):
        pass

    def evaluate_self(self):
        pass

    def evaluate_environment(self):
        pass

    def evaluate_selfmending(self):
        pass

    # help, expertise, load)
    def eval_culture(self):
        help = 0.0
        no_people = 0.0
        rospy.loginfo('eval: ' + str(self.myknowledge.known_people) + '\n')
        for x in self.myknowledge.known_people:
            if x[1] < 0:
                help += 0
            else:
                help += x[1]
            no_people += 1

        if no_people == 0.0:
            return -1.0
        else:
            culture = help / float(no_people)
            return culture

    def debug_self(self):
        pass

    def fix_bugs(self):
        pass

    def make_request(self):
        pass

    def resolve_dependencies(self, service):
        if len(service) > 4:
            return True
        else:
            return False

    def eval_plan(self):
        pass

    def eval_temp(self):
        for x in self.services:
            if x[0] == self.myknowledge.service_req[self.myknowledge.client_index]:
                self.myknowledge.task_idx = self.services.index(x)

        # Decide if it is good to accept request

        self.log.write_log_file(self.log.stdout_log,
                                '[adapt ' + str(self.simulation.interact) + '] client: %d, service_resp: %s\n' % (
                                    self.myknowledge.current_client[self.myknowledge.client_index],
                                    str(self.myknowledge.service_resp[
                                            self.myknowledge.client_index])) + '[adapt ' + str(
                                    self.simulation.interact) + '] old serve: %s\n' % (str(self.myknowledge.service)))

        rate = -1000
        rate_depend = -1000

        if self.myknowledge.attempted_jobs == 0:
            rate = 0.0
        else:
            rate = 1.0 * self.myknowledge.completed_jobs / self.myknowledge.attempted_jobs

        if self.myknowledge.attempted_jobs_depend == 0:
            rate_depend = 0.0
        else:
            rate_depend = 1.0 * self.myknowledge.completed_jobs_depend / self.myknowledge.attempted_jobs_depend

        accept = self.keep_request(self.myknowledge.current_client[self.myknowledge.client_index],
                                   self.services[self.myknowledge.task_idx], self.myknowledge.old_state,
                                   self.myknowledge.service, rate, rate_depend)
        if self.simulation.handle > 0:
            self.log.write_log_file(self.log.stdout_log,
                                    '[adapt ' + str(self.simulation.interact) + '] handled = %d\n' % (
                                        self.simulation.handle))
            self.myknowledge.timeouts_xinteract.append(1.0 * self.myknowledge.timeouts / self.simulation.handle)
        else:
            self.log.write_log_file(self.log.stdout_log,
                                    '[adapt ' + str(self.simulation.interact) + '] nope, nope, nope\n')
            # print 'nope'

        self.log.write_log_file(self.log.stdout_log,
                                '[adapt ' + str(self.simulation.interact) + '] accept ' + str(accept) + '\n')

        if accept:
            ############################ playing with 'queues' - THIS PART IS NOT THREAD-SAFE, NOR FINAL, nor does it remove anything from the .._eval list ###########################
            self.myknowledge.task_queue = self.myknowledge.task_pending_eval
            self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(self.simulation.interact) + '] ' + str(
                self.myknowledge.task_queue) + '\n')
            ########################################################################################################################
            self.myknowledge.count_posReq = self.myknowledge.count_posReq + 1
            self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(self.simulation.interact) + '] adapted\n')

            self.myknowledge.attempted_jobs = self.myknowledge.attempted_jobs + 1

            self.myknowledge.iteration = 1
            self.mycore.state = 2
            self.myknowledge.service = self.services[self.myknowledge.task_idx]

            if len(self.myknowledge.service) > 4:
                self.myknowledge.attempted_jobs_depend = self.myknowledge.attempted_jobs_depend + 1

            self.myknowledge.helping = True
            self.log.write_log_file(self.log.stdout_log,
                                    '[adapt ' + str(self.simulation.interact) + '] service: ' + str(
                                        self.myknowledge.service) + '\n' + '[adapt ' + str(
                                        self.simulation.interact) + '] helping: ' + str(
                                        self.myknowledge.helping) + '\n')

        else:
            # print 'keep at what you\'re doing'
            # praktikisht e le pergjysem kerkesen
            self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(
                self.simulation.interact) + '] keep at what you\'re doing\n' + '[adapt ' + str(
                self.simulation.interact) + '] before if: current client_index: ' + str(
                self.myknowledge.client_index) + '\n')
            if not self.myknowledge.client_index == -1:
                self.myknowledge.lock.acquire()
                self.myknowledge.service_req[self.myknowledge.client_index] = -1
                self.myknowledge.service_resp_content[self.myknowledge.client_index] = -1
                self.myknowledge.service_resp[self.myknowledge.client_index] = True
                self.myknowledge.lock.release()

            self.myknowledge.client_index = self.myknowledge.old_client_index
            self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(
                self.simulation.interact) + '] after old state: current client_index: ' + str(
                self.myknowledge.client_index) + '\n')

            self.mycore.state = self.myknowledge.old_state

    def keep_request(self, client, new_service, state, old_service, jobs_dropped, depend_done):
        accept = False
        ## what you need to make only one agent dynamic ############################################################################################################
        if self.mycore.ID == 7:
            drop_rate = jobs_dropped - self.myknowledge.past_jobs_dropped
            self.log.write_log_file(self.log.stdout_log,
                                    '[dep_delta] dropped: %f, past_dropped: %f, past delta: %f\n' % (
                                        jobs_dropped, self.myknowledge.past_jobs_dropped, self.mycore.willingness[1]))

            # self.delta = self.delta - (jobs_dropped - self.past_jobs_dropped) * jobs_dropped
            if jobs_dropped > self.myknowledge.HIGH:
                self.mycore.willingness[1] = self.mycore.willingness[1] - self.myknowledge.step
                self.log.write_log_file(self.log.stdout_log, '[dep_delta] delta decreased %f by step %f\n' % (
                    self.mycore.willingness[1], self.myknowledge.step))
            elif jobs_dropped < self.myknowledge.LOW:
                self.mycore.willingness[1] = self.mycore.willingness[1] + self.myknowledge.step
                self.log.write_log_file(self.log.stdout_log, '[dep_delta] delta increased %f by step %f\n' % (
                    self.mycore.willingness[1], self.myknowledge.step))
            elif abs(drop_rate) >= 0.01:
                self.log.write_log_file(self.log.stdout_log, '[dep_delta] entered else, L < jb_d < H\n')
                inc_dec = 1 if drop_rate >= 0 else -1
                self.mycore.willingness[1] = self.mycore.willingness[1] - inc_dec * self.myknowledge.step
                self.log.write_log_file(self.log.stdout_log,
                                        '[dep_delta] delta change %f by step %f, inc_dec = %d\n' % (
                                            self.mycore.willingness[1], self.myknowledge.step, inc_dec))
            else:
                self.log.write_log_file(self.log.stdout_log,
                                        '[dep_delta] delta doesn\'t change, else condition, %f by step %f\n' % (
                                            self.mycore.willingness[1], self.myknowledge.step))
                # print 'no change'

            # fit to [0,1]
            if self.mycore.willingness[1] > 1.0:
                self.mycore.willingness[1] = 1.0
            elif self.mycore.willingness[1] < 0.0:
                self.mycore.willingness[1] = 0.0

            self.log.write_log_file(self.log.stdout_log, '[dep_delta] delta = %f\n' % self.mycore.willingness[1])
            self.myknowledge.past_jobs_dropped = jobs_dropped
        ###########################################################################################################################################################

        self.myknowledge.moving_delta_sorted.append(self.mycore.willingness[1])
        self.myknowledge.moving_drop_jobs.append(jobs_dropped)
        self.myknowledge.moving_depend_done.append(depend_done)

        self.log.write_log_file(self.log.stdout_log,
                                '[dep_delta] moving_delta_sorted = %s\n' % str(self.myknowledge.moving_delta_sorted))
        self.log.write_log_file(self.log.stdout_log,
                                '[dep_delta] moving_drop_jobs = %s\n' % str(self.myknowledge.moving_drop_jobs))

        match = False
        if self.myknowledge.moving_delta:
            for x in self.myknowledge.moving_delta:
                if client in x:
                    self.myknowledge.moving_delta[self.myknowledge.moving_delta.index(x)].append(
                        self.mycore.willingness[1])
                    match = True
                    break
            if not match:
                self.myknowledge.moving_delta.append([client, self.mycore.willingness[1]])
        else:
            self.myknowledge.moving_delta.append([client, self.mycore.willingness[1]])

        check_rand = random.random()

        if check_rand < self.mycore.willingness[1]:
            accept = True

        # print 'ACCEPT: ', accept

        return accept

    def publish2sensormotor(self, raw_content):
        if not rospy.is_shutdown():
            # print rospy.get_name()
            self.publish_bcast[0].publish(self.mycore.create_message(raw_content, ''))
        else:
            self.reason = 'Unknown reason - publish2sensormotor'
            rospy.on_shutdown(self.my_hook)

    def init_serve(self, agentid):
        myservice = '/robot' + str(agentid) + '/serve'
        # print 'DECLARING my service'
        srv = rospy.Service(myservice, Protocol_Srv, self.handle_serve)

    def handle_serve(self, request):
        pass

    def call_serve(self, server, myid, request, anyone_index):
        pass

    def calc_culture(self, known_people):
        pass
