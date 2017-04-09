#!/usr/bin/env python
# Parent class of agent, implementing the core parts of the theoretical concept
# Framework v1.0
import sys
import time
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

roslib.load_manifest('gitagent')
import rospy
import actionlib
import action_server_git
import Queue


class Agent0:
    def __init__(self, ID, conf, services, willingness, simulation, popSize, provaNr, depend_nr, battery, sensors,
                 actuators, motors, static):

        # logging class
        self.log = mylogging.Logging(popSize, provaNr, ID, willingness[1], depend_nr)
        self.begin = 0
        self.end = 0

        self.static = static

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

        # Enumerated lists for each #########
        self.services = services
        self.languages = conf['languages']
        self.protocols = conf['protocols']
        self.abilities = conf['abilities']
        self.resources = conf['resources']
        ####################################

        # Variables manipulated by multiple threads ###
        self.adaptive_state = []
        ##############################################

        ## Contains info specific to the internal state of the agent such as: state, health attributes etc.
        self.mycore = core_aboutme.Core(willingness, ID, conf['battery'], sensors, actuators, motors)
        self.mycore.LOW = willingness[1]

        self.log.write_log_file(self.log.stdout_log, 'init gitagent ' + str(self.mycore.sensmot) + '\n')
        ## Contains mixed info ############################################################################
        self.myknowledge = knowledge.Knowledge0()
        # use simulation functions
        self.simulation = simulation
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

        rospy.loginfo('Agent with id: %d, delta: %f, theta: %f, thetaLOW: %f', ID, willingness[1], willingness[0], self.mycore.LOW)

        self.reason = 'Deafult: None'

        self.start = time.time()

        time.sleep(10)

    ##############################################################################################
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
            if (time.time() - self.start) > 1800:
                #pdb.set_trace()
                msg = '[fsm %d] Simulation finished. Number of generated tasks: %d\n' % (
                self.simulation.fsm, sum(self.simulation.no_self_tasks_attempted))
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)
                # Send kill signal to msgPUnit
                self.publish_bcast[0].publish(self.mycore.create_message('DIE', 'DIE'))
                self.reason = 'Simulation end'
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

            ##MOVE ###############################################################################
            self.myknowledge.position2D = self.simulation.move(self.myknowledge.position2D)
            msg = '[fsm ' + str(self.simulation.fsm) + '] self.myknowledge.position2D: ' + str(
                self.myknowledge.position2D) + '\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            self.publish_bcast[1].publish(self.mycore.create_message(self.myknowledge.position2D, 'position'))
            ######################################################################################

            self.fsm_step()

        msg = '[fsm %d] Rospy shutdown. Number of generated tasks: %d\n' % (
        self.simulation.fsm, sum(self.simulation.no_self_tasks_attempted))
        # self.log.write_log_file(self.log.stdout_log, msg)
        rospy.loginfo(msg)
        # Send kill signal to msgPUnit
        self.publish_bcast[0].publish(self.mycore.create_message('DIE', 'DIE'))
        self.reason = 'Rospy shutdown'
        rospy.on_shutdown(self.my_hook)
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
        # print 'I am in blocking action server'
        # rospy.loginfo('Asking agent with id: %d, for help', agent_id)
        msg = '[fsm ' + str(self.simulation.fsm) + '- blocking call - BEGIN]  ' + str(
            rospy.get_name()) + ' -> I am requesting a favor\n'
        # self.log.write_log_file(self.log.stdout_log, msg)
        rospy.loginfo(msg)
        self.begin += 1
        try:
            client = actionlib.SimpleActionClient(agent_id, doMeFavorAction)
            if not client.wait_for_server(timeout=rospy.Duration(60)):
                msg = '[fsm ' + str(self.simulation.fsm) + '- blocking call - BEGIN]  ' + str(
                    rospy.get_name()) + ' -> Couldn\'t connect to server \n'
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)
                return -1

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

            msg = '[fsm ' + str(self.simulation.fsm) + '- blocking_call] Goal sent. Goal state %s\n' % client.get_state()
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            if client.wait_for_result(timeout=rospy.Duration(15)):
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
                        rospy.loginfo('t %d\n'% t)
                        task_idx = self.myknowledge.known_people[agent_idx][2].index(t)
                        rospy.loginfo('tx %d\n'% task_idx)
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

            self.myknowledge.known_people[agent_idx][1] = self.myknowledge.helping_interactions[agent_idx]\
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

            msg = '[fsm ' + str(self.simulation.fsm) + '- blocking_call - END] perceived helpfulness %f\n' % \
                                                       self.myknowledge.known_people[agent_idx][1]
            msg += '[fsm ' + str(self.simulation.fsm) + '- blocking_call] capability expertise %f\n' % \
                                                        self.myknowledge.known_people[agent_idx][3][task_idx]
            msg += '[fsm ' + str(self.simulation.fsm) + '- blocking_call] Result ' + str(result) + '\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            self.simulation.requests[self.myknowledge.difficulty] = self.simulation.requests[self.myknowledge.difficulty] + 1
            self.end += 1
            return result

        except:
            rospy.loginfo("Unexpected error: end]" + str(sys.exc_info()[0]))
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
            goal = self.mycore.string2goalPlan(goalh.content, self.log)

            self.simulation.requests_received[len(goal[0]['abilities']) - 1] += 1

            msg = '[execute_git %d] Goal: %s\n' % (int(goal[0]['senderID']), str(goal))
            self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            # Check if I have already gotten smth from this sender, in that case it's already in the queue, just change task_status to 0
            try:
                # self.log.write_log_file(self.log.stdout_log, '[execute_git] check if guy is in list\n')
                index = next(
                    index for (index, d) in enumerate(self.keep_track_threads) if d['senderId'] == int(goal[0]['senderID']))
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

            timeout = time.time() + 10  # set timeout to be 10 seconds
            # self.log.write_log_file(self.log.stdout_log, '[execute_git %d] timeout: %s\n' % (int(goal[0]['senderID']), str(timeout)))

            msg = '[execute_git %d] Current goal status: %s\n' % (int(goal[0]['senderID']), goalhandle.get_goal_status())
            self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            while self.keep_track_threads[index]['task_status'] == 0:
                # self.log.write_log_file(self.log.stdout_log, '[execute_git] Current goal status: %s\n' % goalhandle.get_goal_status())
                # Let the thread wait for 10 sec, if nothing then return with -1 ~ FAIL
                if time.time() > timeout:
                    self.keep_track_threads[index]['task_status'] = 12
                    msg = '[execute_git %d] request dropped. Threads %s\n' % (
                    int(goal[0]['senderID']), str(self.keep_track_threads))
                    self.log.write_log_file(self.log.stdout_log, msg)
                    rospy.loginfo(msg)
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


        except:
            rospy.loginfo("Unexpected error: " + str(sys.exc_info()[0]))
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
        if not self.myknowledge.plan_pending_eval.empty():
            msg = '[fsm ' + str(self.simulation.fsm) + '] adaptive state: True\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            self.myknowledge.lock.acquire()
            self.myknowledge.old_state = self.mycore.state
            self.mycore.state = 1
            msg = '[fsm ' + str(self.simulation.fsm) + '] Old state, and current state:' + str(
                self.myknowledge.old_state) + str(self.mycore.state) + '\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)
            self.myknowledge.lock.release()
        else:
            msg = '[fsm ' + str(self.simulation.fsm) + '] adaptive state: False\n'
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

    def eval_temp_2(self):

        self.begin += 1
        msg = '[adapt ' + str(self.simulation.interact) + ' BEGIN]\n'
        # self.log.write_log_file(self.log.stdout_log, msg)
        rospy.loginfo(msg)
        try:
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
            # Find the index of this agent in known_people or add it if it is not there
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
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)
            else:
                success = -1.0
                msg = '[adapt %d] Not in known people, success = %f\n' % (self.simulation.interact, success)
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)

            ## Here put the new fuzzy evaluation function
            # accept = True
            #pdb.set_trace()
            abil, equip, knowled, tools, env_risk, diff_task_tradeoff = self.simulation.simulate_give_params()
            energy_diff = self.mycore.battery - float(plan[0]['energy'])
            ag_risk = 1.0 - success

            msg = '[adapt %d] energy diff = %f\n' % (self.simulation.interact, energy_diff)
            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            if not sum(self.simulation.no_self_tasks_attempted) == 0:
                performance = sum(self.simulation.no_self_tasks_completed) / float(sum(self.simulation.no_self_tasks_attempted))
            else:
                performance = 1.0

            if self.static[1] == 0:
                accept, delta = self.mycore.b_delta(energy_diff, abil, equip, knowled, tools, env_risk, ag_risk, performance, diff_task_tradeoff)
            else:
                delta = self.mycore.delta
                if not abil or not equip or not knowled or not tools:
                    self.simulation.finish = 0.0
                else:
                    self.simulation.finish = 1.0
                if random.random() < delta:
                    accept = True
                else:
                    accept = False

            # print accept
            msg = '[adapt %d] abil = %f, equip = %f, knowled = %f, tools = %f, env_risk = %f, task-trade = %f, delta = %f\n' % (self.simulation.interact, abil, equip, knowled, tools, env_risk, diff_task_tradeoff, delta)

            msg += '[adapt %d] Accept = %f, simulation-finish = %f\n' % (self.simulation.interact, accept, self.simulation.finish)
            msg += '[adapt %d] Plan ' + str(plan) + '\n'

            # self.log.write_log_file(self.log.stdout_log, msg)
            rospy.loginfo(msg)

            self.myknowledge.lock.acquire()
            self.simulation.delta_theta.append([0, delta, accept, performance])
            self.myknowledge.lock.release()

            if accept:
                self.myknowledge.attempted_jobs += 1

                self.simulation.requests_rec_accept[len(plan[0]['abilities']) - 1] += 1

                msg = '[adapt ' + str(self.simulation.interact) + '] Adopted plan: ' + str(plan) + '\n'
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)

                for x in plan:
                    msg = '[adapt ' + str(self.simulation.interact) + '] Task in plan: ' + str(x) + '\n'
                    # self.log.write_log_file(self.log.stdout_log, msg)
                    rospy.loginfo(msg)
                    self.myknowledge.task_queue.put(x)

                msg = '[adapt %d] Tasks put in queue\n' % self.simulation.interact
                # self.log.write_log_file(self.log.stdout_log, msg)
                rospy.loginfo(msg)

                self.myknowledge.lock.acquire()
                self.mycore.state = 2
                self.myknowledge.lock.release()

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

        except:
            rospy.loginfo("Unexpected error: " + str(sys.exc_info()[0]))
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

    def idle(self):
        # print 'im in idle'
        self.simulation.idle = self.simulation.inc_iterationstamps(self.simulation.idle)
        msg = '[idle ' + str(self.simulation.idle) + '] idle\n'
        # self.log.write_log_file(self.log.stdout_log, msg)
        rospy.loginfo(msg)
        self.generate_goal_v2()
        self.commit2goal()

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
                    rospy.loginfo('thread active %d\n'% int(x['senderId']))
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
                    msg = '[execute ' + str(self.simulation.execute) + ']' + str(
                        self.myknowledge.service) + '\n'
                    # self.log.write_log_file(self.log.stdout_log, msg)

                    self.myknowledge.service_id = int(self.myknowledge.service['id'])

                    msg += '[execute ' + str(self.simulation.execute) + ']' + str(self.myknowledge.service_id) + '\n'

                    self.myknowledge.iteration = 1

                    msg += '[execute ' + str(self.simulation.execute) + ']' + str(self.myknowledge.iteration) + '\n'

                    # Detect task difficulty - from nr of required services
                    self.myknowledge.difficulty = self.simulation.detect_difficulty(self.myknowledge.service)
                    self.simulation.no_tasks_attempted[self.myknowledge.difficulty] += 1

                    msg += '[execute ' + str(self.simulation.execute) + '] Difficulty: ' + str(
                        self.myknowledge.difficulty) + '\n'
                    rospy.loginfo(msg)

                    if not int(self.myknowledge.service['senderID'] == self.mycore.ID):
                        if self.is_thread_active(int(self.myknowledge.service['senderID'])):
                            msg = '[execute ' + str(
                                self.simulation.execute) + ']I am helping someone and their thread is still active\n'
                            rospy.loginfo(msg)

                            self.execute_step_v4()
                        else:
                            msg = '[execute ' + str(self.simulation.execute) + ']Thread not active anymore\n'
                            rospy.loginfo(msg)
                    else:
                        msg = '[execute ' + str(self.simulation.execute) + '] Working for myself\n'
                        self.simulation.no_self_tasks_attempted[self.myknowledge.difficulty] += 1
                        rospy.loginfo(msg)
                        self.execute_step_v4()
                else:
                    self.myknowledge.lock.acquire()
                    self.mycore.state = 0
                    self.myknowledge.lock.release()
                    msg = '[execute ' + str(self.simulation.execute) + '] My state: ' + str(self.mycore.state) + '\n'
                    rospy.loginfo(msg)
            else:
                msg = '[execute ' + str(self.simulation.execute) + '] continue working\n'
                rospy.loginfo(msg)
                self.execute_step_v4()

            msg = '[execute ' + str(self.simulation.execute) + 'END]\n'
            rospy.loginfo(msg)
            self.end += 1

        except:
            rospy.loginfo("Unexpected error: " + str(sys.exc_info()[0]))
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
            self.begin += 1
            msg = '[run_step ' + str(self.simulation.execute) + ' BEGIN] in execute_step\n'
            rospy.loginfo(msg)
            # print 'in execute_step'
            #pdb.set_trace()
            # This returns the best candidate id, and success measure
            success_chance, candidate_id, candidate_idx = self.mycore.best_candidate(self.myknowledge.known_people,
                                                                                     self.myknowledge.service, self.log)
            msg = '[run_step ' + str(
                self.simulation.execute) + ' BEGIN] success %f, id %d, idx %d\n' % (
                success_chance, candidate_id, candidate_idx
            )
            rospy.loginfo(msg)

            if candidate_id == self.myknowledge.service['senderID'] and not self.mycore.ID == self.myknowledge.service[
                'senderID']:
                msg = '[run_step ' + str(self.simulation.execute) + '] do not ask the same agent that asked you for help'
                rospy.loginfo(msg)
                success_chance = -1.0

            abil, equip, knowled, tools, env_risk, diff_task_progress = self.simulation.simulate_ask_params()
            energy_diff = self.mycore.battery - float(self.myknowledge.service['energy'])
            ag_risk = 1.0 - success_chance

            if not sum(self.simulation.no_self_tasks_attempted) == 0:
                performance = sum(self.simulation.no_self_tasks_completed) / float(sum(self.simulation.no_self_tasks_attempted))
            else:
                performance = 1.0

            if self.static[0] == 0:
                depend, gamma = self.mycore.b_gamma(energy_diff, abil, equip, knowled, tools, env_risk, ag_risk, performance, diff_task_progress)
            else:
                gamma = self.mycore.gamma
                if self.simulation.finish == -1.0:
                    if not abil or not equip or not knowled or not tools:
                        self.simulation.finish = 0.0
                    else:
                        self.simulation.finish = 1.0
                if random.random() < gamma:
                    depend = True
                else:
                    depend = False

            msg = '[run_step ' + str(self.simulation.execute) + '] ask for help: ' + str(depend) + '\n'
            msg += '[execute %d] abil = %f, equip = %f, knowled = %f, tools = %f, env_risk = %f, task-trade = %f, gamma = %f\n' % (self.simulation.execute, abil, equip, knowled, tools, env_risk, diff_task_progress, gamma) + '\n'

            rospy.loginfo(msg)

            self.myknowledge.lock.acquire()
            self.simulation.delta_theta.append([1, gamma, depend, performance])
            self.myknowledge.lock.release()

            result = 0

            if depend:
                self.simulation.no_tasks_depend_attempted[self.myknowledge.difficulty] += 1
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

            else:
                exec_time = self.simulation.delay[self.myknowledge.difficulty]
                msg = '[run_step ' + str(self.simulation.execute) + '] Do it yourself\n ...Wait for %f\n' % exec_time
                rospy.loginfo(msg)

                self.simulation.exec_times[self.myknowledge.difficulty] = self.simulation.exec_times[
                                                                              self.myknowledge.difficulty] + exec_time
                msg = '[run_step ' + str(
                    self.simulation.execute) + '] difficulty: %f, delay: %f, addi: %f\n' % (
                    self.myknowledge.difficulty, self.simulation.delay[self.myknowledge.difficulty],
                    self.simulation.additional_delay[self.myknowledge.difficulty])
                rospy.loginfo(msg)
                #pdb.set_trace()
                time.sleep(exec_time)
                self.myknowledge.service_id = -1
                self.myknowledge.iteration = -1

                if random.random() < self.simulation.finish:
                    result = 1
                    self.myknowledge.completed_jobs += 1
                    self.simulation.no_tasks_completed[self.myknowledge.difficulty] += 1
                else:
                    result = 2

                # diminish by the energy required by the task
                self.mycore.battery_change(int(self.myknowledge.service['energy']))

            # In case I am helping some other agent, trigger response here
            msg = '[run_step ' + str(self.simulation.execute) + '] sender: %d, result: %d\n' % (int(self.myknowledge.service['senderID']), result)
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

                    msg = '[run_step ' + str(self.simulation.execute) + '] Threads %s\n' % str(self.keep_track_threads)
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
            self.simulation.finish = -1.0
            self.end += 1

        except:
            rospy.loginfo("Unexpected error: " + str(sys.exc_info()[0]))
            pass

    def regenerate(self):
        # print 'im in regenerate'
        self.simulation.regenerate = self.simulation.inc_iterationstamps(self.simulation.regenerate)
        self.myknowledge.lock.acquire()
        self.mycore.state = 0
        self.myknowledge.lock.release()
        self.mycore.battery += 4400 - self.mycore.battery
        msg = '[fsm_INFO] I am in regenrate, switch to idle, state changed to %d, energy acquired %d' % (self.mycore.state, self.mycore.battery)
        rospy.loginfo(msg)

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

    # MUST be overriden in the child class, depending on the different types of inputs!
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
                      'equipment': equipment, 'startLoc': startLoc, 'reward': reward, 'resources': res,
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
            if random.random() < 0.6:
                it = [100, 400, 700]
                en = [1, 10, 30]
                re = [50, 150, 350]
                ab = [['walk'], ['walk', 'talk'], ['walk', 'talk', 'smoke']]
                risurs = [['pringles'], ['pringles', 'brie'], ['pringles', 'brie', 'beer']]
                etime = [130, 1300, 2300]

                difficulty = random.randint(0,2)

                msg = '[generate goal ' + str(self.simulation.idle) + ' BEGIN] ' + str(
                    self.simulation.no_self_tasks_attempted) + ' difficulty: ' + str(difficulty) + '\n'
                rospy.loginfo(msg)

                senderId = self.mycore.ID
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

                tasks = [{'abilities': abilities, 'estim_time': estim_time, 'senderID': senderId, 'energy': energy,
                          'iterations': iterations, 'id': tID, 'name': tName, 'endLoc': endLoc, 'planID': planId,
                          'equipment': equipment, 'startLoc': startLoc, 'reward': reward, 'resources': res,
                          'reward': reward, 'noAgents': noAgents}]

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
                #msg = '[generate goal ' + str(self.simulation.idle) + '] do nothing - zot jepi atij qe rri kot :DD\n'
                #rospy.loginfo(msg)
                pass

            msg = '[generate goal ' + str(self.simulation.idle) + ' END]\n'
            rospy.loginfo(msg)
            self.end += 1

        except:
            rospy.loginfo("Unexpected error: " + str(sys.exc_info()[0]))
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
