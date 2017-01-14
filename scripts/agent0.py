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
                 actuators, motors):

        # logging class
        self.log = mylogging.Logging(popSize, provaNr, ID, willingness[1], depend_nr)

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

        rospy.loginfo('Agent with id: %d, delta: %f, theta: %f', ID, willingness[1], willingness[0])

        self.reason = 'Deafult: None'

        time.sleep(10)

    ##############################################################################################
    def my_hook(self):
        print self.reason
        self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + '] ' + self.reason + '\n')

    def fsm(self):
        while not rospy.is_shutdown():
            # Simulation stopping criterion
            if (sum(self.simulation.generated_tasks) + 1) > self.simulation.STOP:
                self.log.write_log_file(self.log.stdout_log, '[fsm %d] Simulation finished. Number of tasks done: %d\n'
                                    % (self.simulation.fsm, self.simulation.stopINC))
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
            self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + '] current state: ' + str(
                self.mycore.state) + '\n')

            ##MOVE ###############################################################################
            self.myknowledge.position2D = self.simulation.move(self.myknowledge.position2D)
            self.log.write_log_file(self.log.stdout_log,
                                    '[fsm ' + str(self.simulation.fsm) + '] self.myknowledge.position2D: ' + str(
                                        self.myknowledge.position2D) + '\n')
            self.publish_bcast[1].publish(self.mycore.create_message(self.myknowledge.position2D, 'position'))
            ######################################################################################

            self.fsm_step()
        return

    def fsm_step(self):
        self.simulation.fsm = self.simulation.inc_iterationstamps(self.simulation.fsm)

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
        self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + ']  Goal just sent!\n')

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

        client = actionlib.SimpleActionClient(agent_id, doMeFavorAction)
        client.wait_for_server()
        self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + '-block]  ' + str(
            rospy.get_name()) + '\nI am requesting a favor\n')
        # print rospy.get_name()
        # print 'I am requesting a favor'

        goal2str = self.mycore.goal2string(goal)
        # self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + ']  ' + goal2str + '\n')

        formatted_goal = doMeFavorGoal(performative='plead4goal', sender=str(self.mycore.ID), rank=10,
                                       receiver=agent_id, language='shqip', ontology='laraska', urgency='none',
                                       content=goal2str, timestamp=time.strftime('%X', time.gmtime()))

        self.log.write_log_file(self.log.stdout_log,
                                '[fsm ' + str(self.simulation.fsm) + ']  ' + str(formatted_goal) + '\n')

        # client.send_goal(formatted_goal, self.done, self.active, self.feedback)
        self.myknowledge.total_interactions[agent_idx] += 1
        client.send_goal(formatted_goal)
        self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + '-block] Goal sent!!\n')

        self.log.write_log_file(self.log.stdout_log,
                                '[fsm ' + str(self.simulation.fsm) + '-block] goal state %s\n' % client.get_state())
        # client.wait_for_result() # Set timeout to 15 seconds

        if client.wait_for_result(timeout=rospy.Duration(15)):
            self.log.write_log_file(self.log.stdout_log,
                                    '[fsm ' + str(self.simulation.fsm) + '-block] server returned\n')
            result = client.get_result()
        else:
            self.log.write_log_file(self.log.stdout_log,
                                    '[fsm ' + str(self.simulation.fsm) + '-block] server did not return\n')
            result = 12

        # Update profile of the agent asked for help
        task_id = goal['id']

        task_idx = -1
        for x in self.myknowledge.known_people:
            if x[0] == agent_id:
                for t in x[2]:
                    if t == task_id:
                        task_idx = x[2].index(t)
                        break
                break
        self.log.write_log_file(self.log.stdout_log,
                                '[fsm ' + str(self.simulation.fsm) + '-block] task_id %d, task_idx %d, agent_tasks %s\n'
                                % (task_id, task_idx, self.myknowledge.known_people[agent_idx][2]))
        self.myknowledge.lock.acquire()
        # rospy.loginfo('Result from agent with id: %d, is: %d', agent_id, result)

        if not result == 12:
            self.myknowledge.helping_interactions[agent_idx] += 1
            if result == 1:
                self.myknowledge.completed_jobs += 1
                self.myknowledge.completed_jobs_depend += 1
                self.myknowledge.capability_expertise[agent_idx][task_idx][0] += 1

        # Update perceived helpfulness and expertise
        # print self.myknowledge.known_people[agent_idx][1]
        # print self.myknowledge.helping_interactions[agent_idx]
        # print self.myknowledge.total_interactions[agent_idx]
        self.myknowledge.known_people[agent_idx][1] = self.myknowledge.helping_interactions[agent_idx] \
                                                      / float(self.myknowledge.total_interactions[agent_idx])

        self.log.write_log_file(self.log.stdout_log,
                                '[fsm ' + str(self.simulation.fsm) + '-block] perceived helpfulness %f\n' %
                                self.myknowledge.known_people[agent_idx][1])

        self.myknowledge.known_people[agent_idx][3][task_idx] = \
        self.myknowledge.capability_expertise[agent_idx][task_idx][0] \
        / float(
            self.myknowledge.capability_expertise[agent_idx][task_idx][1])

        self.log.write_log_file(self.log.stdout_log,
                                '[fsm ' + str(self.simulation.fsm) + '-block] capability expertise %f\n'
                                % self.myknowledge.known_people[agent_idx][3][task_idx])

        self.myknowledge.lock.release()

        self.log.write_log_file(self.log.stdout_log,
                                '[fsm ' + str(self.simulation.fsm) + '-block] Result ' + str(result) + '\n')

        return result

    def execute_git(self, goalhandle):
        # print 'I got a request'
        # Add tag to identify current thread
        # Task status: 12 ~ REJECT, 0 ~ PENDING, 1 ~ SUCCESS, 2 ~ FAIL 10 ~ no thread active
        # index = -1

        feedback = doMeFavorFeedback()
        result = doMeFavorResult()

        self.myknowledge.lock.acquire()
        goalh = goalhandle.get_goal()
        # self.log.write_log_file(self.log.stdout_log, '[execute_git] getting goal: %s\n' % goal)
        goal = self.mycore.string2goalPlan(goalh.content, self.log)
        self.log.write_log_file(self.log.stdout_log,
                                '[execute_git %d] goal: %s\n' % (int(goal[0]['senderID']), str(goal)))
        rospy.loginfo('Agent with id: %d, requested assistance', int(goal[0]['senderID']))

        # Check if I have already gotten smth from this sender, in that case it's already in the queue, just change task_status to 0
        try:
            # self.log.write_log_file(self.log.stdout_log, '[execute_git] check if guy is in list\n')
            index = next(
                index for (index, d) in enumerate(self.keep_track_threads) if d['senderId'] == int(goal[0]['senderID']))
            self.keep_track_threads[index]['task_status'] = 0
            # print 'Guy currently in list: %d' % index
            self.log.write_log_file(self.log.stdout_log,
                                    '[execute_git %d] Guy currently in list: %d\n' % (int(goal[0]['senderID']), index))
        except StopIteration:
            # we can check first element in potential array goal, because the sender for each task is the same
            self.keep_track_threads.append({'senderId': int(goal[0]['senderID']), 'task_status': 0})
            index = len(self.keep_track_threads) - 1
            self.log.write_log_file(self.log.stdout_log,
                                    '[execute_git %d] New guy: %d\n' % (int(goal[0]['senderID']), index))
            # It is assumed that the senderId is unique, that is the server cannot get 2 a second task from an agent, without returning with the first.
            # {senderID:task_status}
            # self.keep_track_threads.append({data.sender:0})
        self.log.write_log_file(self.log.stdout_log, '[execute_git %d] Threads: %s\n' % (
        int(goal[0]['senderID']), str(self.keep_track_threads)))

        # Put task in a queue, make thread wait until task status is set to success/fail -- might be possible to add a timeout for that
        self.queueGoalHandles.put(goalhandle)
        # self.log.write_log_file(self.log.stdout_log, '[execute_git %d] %s\n' % str(self.queueGoalHandles))
        self.myknowledge.plan_pending_eval.put(goal)
        self.log.write_log_file(self.log.stdout_log, '[execute_git %d] %s\n' % (
        int(goal[0]['senderID']), str(self.myknowledge.plan_pending_eval)))
        self.myknowledge.lock.release()
        self.log.write_log_file(self.log.stdout_log,
                                '[execute_git %d] Current goal status: %s\n' % (
                                int(goal[0]['senderID']), goalhandle.get_goal_status()))

        timeout = time.time() + 10  # set timeout to be 10 seconds
        # self.log.write_log_file(self.log.stdout_log, '[execute_git %d] timeout: %s\n' % (int(goal[0]['senderID']), str(timeout)))

        while self.keep_track_threads[index]['task_status'] == 0:
            # self.log.write_log_file(self.log.stdout_log, '[execute_git] Current goal status: %s\n' % goalhandle.get_goal_status())
            # Let the thread wait for 10 sec, if nothing then return with -1 ~ FAIL
            if time.time() > timeout:
                rospy.loginfo('Request for agent with id: %d dropped', int(goal[0]['senderID']))
                self.log.write_log_file(self.log.stdout_log,
                                        '[execute_git %d] request dropped\n' % int(goal[0]['senderID']))
                self.server.git_accept_new_goal(goalhandle)

                self.log.write_log_file(self.log.stdout_log,
                                '[execute_git %d] Current goal status: %s\n' % (
                                int(goal[0]['senderID']), goalhandle.get_goal_status()))

                self.keep_track_threads[index]['task_status'] = 12
                break

        # self.log.write_log_file(self.log.stdout_log, '[execute_git] Task execution pending\n')
        # During execution some feedback might be available
        # self.server.publish_result(0,49)
        # print 'Thread: ' + str(self.keep_track_threads[index]['task_status']) + ' has returned (task_status)'

        rospy.loginfo('Request for agent with id: %d returned with status: %s', int(goal[0]['senderID']),
                      str(self.keep_track_threads[index]['task_status']))

        self.log.write_log_file(self.log.stdout_log, '[execute_git %d] Thread has returned'
                                                     ' with status: %d\n' % (int(goal[0]['senderID']),
                                                    self.keep_track_threads[index]['task_status']))
        result.act_outcome = self.keep_track_threads[index]['task_status']

        self.log.write_log_file(self.log.stdout_log,
                                '[execute_git %d] Before set succeeded\n' % int(goal[0]['senderID']))
        self.server.set_succeeded(goalhandle, result)
        self.log.write_log_file(self.log.stdout_log,
                                '[execute_git %d] Current goal status: %s\n' % (
                                int(goal[0]['senderID']), goalhandle.get_goal_status()))
        # self.server.set_succeeded(goalhandle)
        self.myknowledge.lock.acquire()
        self.keep_track_threads[index]['task_status'] = 10
        self.myknowledge.lock.release()
        self.log.write_log_file(self.log.stdout_log,
                                '[execute_git %d] Threads: %s\nResult %s\n' % (
                                int(goal[0]['senderID']), str(self.keep_track_threads), str(result)))

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
            self.log.write_log_file(self.log.stdout_log,
                                    '[fsm ' + str(self.simulation.fsm) + '] adaptive state: True\n')

            self.myknowledge.lock.acquire()
            self.myknowledge.old_state = self.mycore.state
            self.mycore.state = 1
            self.log.write_log_file(self.log.stdout_log,
                                    '[fsm ' + str(self.simulation.fsm) + '] Old state, and current state:' + str(
                                        self.myknowledge.old_state) + str(
                                        self.mycore.state) + '\n')
            self.myknowledge.lock.release()
        else:
            self.log.write_log_file(self.log.stdout_log,
                                    '[fsm ' + str(self.simulation.fsm) + '] adaptive state: False\n')

    def eval_temp_2(self):

        self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(self.simulation.interact) + ']\n')

        rate_depend = -1000

        if self.myknowledge.attempted_jobs == 0:
            self_esteem = 0.0
        else:
            self_esteem = 1.0 * self.myknowledge.completed_jobs / self.myknowledge.attempted_jobs

        if self.myknowledge.attempted_jobs_depend == 0:
            rate_depend = 0.0
        else:
            rate_depend = 1.0 * self.myknowledge.completed_jobs_depend / self.myknowledge.attempted_jobs_depend

        ## Take plan-request out of queue, and put the tasks into the queue for tasks the agent has committed to
        # careful with the queues below, there is no handling if it is empty!!
        # pdb.set_trace()
        plan = self.myknowledge.plan_pending_eval.get()
        # print 'This is the newly gotten plan ' + str(plan)
        aID = int(plan[0]['senderID'])
        aIDx = -1
        # print self.myknowledge.known_people
        # Find the index of this agent in known_people or add it if it is not there
        for x in self.myknowledge.known_people:
            if x[0] == aID:
                aIDx = self.myknowledge.known_people.index(x)
                self.log.write_log_file(self.log.stdout_log, 'aIDX = %d\n' % aIDx)
                break
        if not aIDx == -1:
            self.log.write_log_file(self.log.stdout_log, 'in known people\n')
            success = self.myknowledge.known_people[aIDx][1]
        else:
            self.log.write_log_file(self.log.stdout_log, 'in known people\n')
            success = 0.0

        ## Here put the new fuzzy evaluation function
        # accept = True
        dependencies_abil, dependencies_res, req_missing, task_importance, task_urgency, culture = self.simulation.sim_dependencies(self.myknowledge.service)
        req_goodness = random.random()

        accept, gamma = self.mycore.give_help(sum([self.mycore.sensmot, self.mycore.battery]), dependencies_abil,
                                       dependencies_res,
                                       self.mycore.self_esteem, task_urgency, task_importance, culture, req_goodness, success)
        # print accept
        self.log.write_log_file(self.log.stdout_log,
                                '[adapt ' + str(self.simulation.interact) + '] accept ' + str(accept) + '\n')

        gh = self.queueGoalHandles.get()
        self.log.write_log_file(self.log.stdout_log,
                                    '[adapt' + str(
                                        self.simulation.interact) + '] Current goal status: %s\n' % gh.get_goal_status())
        if accept:
            self.myknowledge.attempted_jobs += 1
            self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(self.simulation.interact) + '] adapted\n')
            # Take plan-request out of queue, and put the tasks into the queue for tasks the agent has committed to
            # careful with the queues below, there is no handling if it is empty!!

            self.server.git_accept_new_goal(gh)
            self.log.write_log_file(self.log.stdout_log,
                                    '[adapt' + str(
                                        self.simulation.interact) + '] Current goal status: %s\n' % gh.get_goal_status())

            self.log.write_log_file(self.log.stdout_log,
                                    '[adapt ' + str(self.simulation.interact) + '] ' + str(plan) + '\n\n')

            for x in plan:
                self.log.write_log_file(self.log.stdout_log,
                                        '[adapt ' + str(self.simulation.interact) + '] ' + str(x) + '\n')
                self.myknowledge.task_queue.put(x)

            self.log.write_log_file(self.log.stdout_log,
                                    '[adapt ' + str(self.simulation.interact) + '] put tasks in queue\n')

            self.myknowledge.count_posReq += 1
            self.myknowledge.attempted_jobs += 1

            self.myknowledge.lock.acquire()
            self.mycore.state = 2
            self.myknowledge.lock.release()

            # self.myknowledge.service = self.services[self.myknowledge.task_idx]

            self.myknowledge.helping = True
            self.log.write_log_file(self.log.stdout_log,
                                    '[adapt ' + str(self.simulation.interact) + '] helping: ' + str(
                                        self.myknowledge.helping) + '\n')
        else:
            # print 'keep at what you\'re doing'
            self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(self.simulation.interact) + '] do not adapt\n')
            self.server.git_accept_new_goal(gh)
            # self.server.set_preempted(gh)
            self.log.write_log_file(self.log.stdout_log,
                                    '[adapt' + str(
                                        self.simulation.interact) + '] Current goal status: %s\n' % gh.get_goal_status())

            index = next(index for (index, d) in enumerate(self.keep_track_threads) if d['senderId'] == aID)

            if self.is_thread_active(aID):

                self.keep_track_threads[index]['task_status'] = 12
                # self.keep_track_threads[0]['task_status'] = 1
                self.log.write_log_file(self.log.stdout_log,
                                        '[adapt' + str(self.simulation.interact) + '] Threads %s\n' % str(
                                            self.keep_track_threads))
            else:
                self.keep_track_threads[index]['task_status'] = 10

                self.log.write_log_file(self.log.stdout_log,
                                        '[adapt' + str(self.simulation.interact) + '] Not adapted, but thread not active anymore. Threads %s\n' % str(
                                            self.keep_track_threads))

            self.myknowledge.lock.acquire()
            self.mycore.state = self.myknowledge.old_state
            self.myknowledge.lock.release()

            # Record
            self.simulation.gamma_esteem.append(self.mycore.self_esteem)
            self.simulation.gamma_tu.append(task_urgency)
            self.simulation.gamma_ti.append(task_importance)
            self.simulation.gamma_culture.append(culture)
            self.simulation.gamma_candidate.append(success)
            self.simulation.gamma.append(gamma)
            if req_missing:
                self.simulation.gamma_deps.append(1)
            else:
                self.simulation.gamma_deps.append(0)
            self.simulation.gamma_health.append(sum([self.mycore.sensmot, self.mycore.battery]))
            self.simulation.gamma_bool.append(accept)
            self.simulation.gamma_req_goodness.append(req_goodness)

    def amIHelping(self, sender):
        if not sender == self.mycore.ID:
            return True
        else:
            return False

    def idle(self):
        # print 'im in idle'
        self.simulation.idle = self.simulation.inc_iterationstamps(self.simulation.idle)
        self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.idle) + '] idle\n')
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
                    return True
        return False

    def execute_v2(self):
        self.simulation.execute = self.simulation.inc_iterationstamps(self.simulation.execute)

        self.log.write_log_file(self.log.stdout_log,
                                '[execute ' + str(self.simulation.execute) + ']' + str(self.myknowledge.service) + '\n')
        self.log.write_log_file(self.log.stdout_log, '[execute ' + str(self.simulation.execute) + ']' + str(
            self.myknowledge.service_id) + '\n')
        self.log.write_log_file(self.log.stdout_log, '[execute ' + str(self.simulation.execute) + ']' + str(
            self.myknowledge.iteration) + '\n')

        if self.myknowledge.service_id == -1 and self.myknowledge.iteration == -1:
            if not self.myknowledge.task_queue.empty():
                self.myknowledge.service = self.myknowledge.task_queue.get()
                self.log.write_log_file(self.log.stdout_log, '[execute ' + str(self.simulation.execute) + ']' + str(
                    self.myknowledge.service) + '\n')

                self.myknowledge.service_id = int(self.myknowledge.service['id'])
                self.log.write_log_file(self.log.stdout_log, '[execute ' + str(self.simulation.execute) + ']' + str(
                    self.myknowledge.service_id) + '\n')

                self.myknowledge.iteration = 1
                self.log.write_log_file(self.log.stdout_log, '[execute ' + str(self.simulation.execute) + ']' + str(
                    self.myknowledge.iteration) + '\n')

                ## Detect task difficulty - from nr of required services
                self.myknowledge.difficulty = self.simulation.detect_difficulty(self.myknowledge.service)
                self.simulation.no_tasks_attempted[self.myknowledge.difficulty] += 1

                self.log.write_log_file(self.log.stdout_log,
                                        '[execute ' + str(self.simulation.execute) + '] Difficulty: ' + str(
                                            self.myknowledge.difficulty) + '\n')

                if not int(self.myknowledge.service['senderID'] == self.mycore.ID):
                    if self.is_thread_active(int(self.myknowledge.service['senderID'])):
                        self.log.write_log_file(self.log.stdout_log, '[execute ' + str(self.simulation.execute)
                                                + ']I am helping someone and their thread is still active\n')
                        self.execute_step_v4()
                    else:
                        self.log.write_log_file(self.log.stdout_log, '[execute ' + str(self.simulation.execute)
                                                + ']Thread not active anymore\n')
                else:
                    self.execute_step_v4()
            else:
                self.mycore.state = 0
                self.log.write_log_file(self.log.stdout_log,
                                        '[execute ' + str(self.simulation.execute) + '] My state: ' + str(
                                            self.mycore.state) + '\n')
        else:
            self.log.write_log_file(self.log.stdout_log,
                                    '[execute ' + str(self.simulation.execute) + '] continue working\n')
            self.execute_step_v4()

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
        self.log.write_log_file(self.log.stdout_log,
                                '[run_step ' + str(self.simulation.execute) + '] in execute_step\n')
        # print 'in execute_step'
        dependencies_abil, dependencies_res, req_missing, task_importance, task_urgency, culture = self.simulation.sim_dependencies(
            self.myknowledge.service)
        # print 'after dep'

        # This returns the best candidate id, and success measure
        success_chance, candidate_id, candidate_idx = self.mycore.best_candidate(self.myknowledge.known_people,
                                                                                 self.myknowledge.service, self.log)

        if candidate_id == self.myknowledge.service['senderID'] and not self.mycore.ID == self.myknowledge.service['senderID']:
            self.log.write_log_file(self.log.stdout_log,
                                    '[run_step ' + str(self.simulation.execute) + '] do not ask the same agent that asked you for help')
            success_chance = -1.0

        self.log.write_log_file(self.log.stdout_log,
                                '[run_step ' + str(self.simulation.execute) + '] inputs: %f, %f, health: %f\n' % (
                                    dependencies_abil, dependencies_res,
                                    sum([self.mycore.sensmot, self.mycore.battery])))

        start_time = timeit.default_timer()
        depend, theta = self.mycore.ask_4help(sum([self.mycore.sensmot, self.mycore.battery]), dependencies_abil,
                                              dependencies_res, self.mycore.self_esteem, task_urgency, task_importance,
                                              culture, success_chance)
        # depend_fuzzy = self.mycore.willing2ask_fuzzy(
        #     [sum([self.mycore.sensmot, self.mycore.battery]), 0.7, dependencies, 0.5])
        self.simulation.fuzzy_time.append(timeit.default_timer() - start_time)

        self.log.write_log_file(self.log.stdout_log,
                                '[run_step ' + str(self.simulation.execute) + '] ask for help: ' + str(
                                    depend) + '\n')

        if req_missing and not depend:
            self.simulation.required_missing_noreq = self.simulation.required_missing_noreq + 1
            self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(
                self.simulation.execute) + '] There should have been a request: ' + str(
                self.simulation.required_missing_noreq / float(self.simulation.required_missing)) + '\n')

        result = 0

        if depend:
            self.simulation.no_tasks_depend_attempted[self.myknowledge.difficulty] += 1
            if not candidate_id == -1:
                self.simulation.requests[self.myknowledge.difficulty] = self.simulation.requests[
                                                                            self.myknowledge.difficulty] + 1

                self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(
                    self.simulation.execute) + '] difficulty: %f, delay: %f, addi: %f\n' % (
                                            self.myknowledge.difficulty,
                                            self.simulation.delay[self.myknowledge.difficulty],
                                            self.simulation.additional_delay[self.myknowledge.difficulty]))
                self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(
                    self.simulation.execute) + '] Ask for help\n\n')

                # WRITE FUNCTION TO SELECT THE BEST KNOWN CANDIDATE -- you have this in Gitagent
                # if self.mycore.ID == 1:
                ######### Use the best agent known -- obviously a hardcoded value will not be used in future
                agent2ask = '/robot' + str(candidate_id) + '/brain_node'
                self.log.write_log_file(self.log.stdout_log, 'agent2ask is: ' +
                                        str(agent2ask) + '\n')
                ######### Make request to action_server
                # self.call_action_server(self.myknowledge.service, agent2ask)
                # print 'before blocking call'
                start = timeit.default_timer()
                result = self.call_blocking_action_server(self.myknowledge.service, agent2ask, candidate_idx)

                # TIME THE SERVER'S RESPONSE!!
                exec_time =  timeit.default_timer() - start
                self.simulation.exec_times[self.myknowledge.difficulty] = self.simulation.exec_times[
                                                                              self.myknowledge.difficulty] + exec_time
                self.log.write_log_file(self.log.stdout_log, 'exec_time: ' +
                                        str(exec_time) + '\n')
                self.myknowledge.service_id = -1
                self.myknowledge.iteration = -1

                # Assume that less energy is consumed when asking for help -- someone else is doing the deed
                self.mycore.battery_change(0.2 * int(self.myknowledge.service['energy']))
                self.simulation.no_tasks_depend_completed[self.myknowledge.difficulty] += 1
            else:
                # Count noones serves to identify those case in which the agent does not know anyone that could be of help
                self.myknowledge.COUNT_noones += 1
                self.myknowledge.service_id = -1
                self.myknowledge.iteration = -1

                # Assume that less energy is consumed when asking for help -- someone else is doing the deed
                self.mycore.battery_change(0.2 * int(self.myknowledge.service['energy']))

                self.log.write_log_file(self.log.stdout_log, 'No one to ask\n')
                self.log.write_log_file(self.log.stdout_log, str(self.myknowledge.known_people) + '\n')

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
            result = 1

            time.sleep(exec_time)
            self.myknowledge.service_id = -1
            self.myknowledge.iteration = -1

            self.myknowledge.completed_jobs += 1
            # diminish by the energy required by the task
            self.mycore.battery_change(int(self.myknowledge.service['energy']))
            self.simulation.no_tasks_completed[self.myknowledge.difficulty] += 1

        # In case I am helping some other agent, trigger response here
        self.log.write_log_file(self.log.stdout_log,
                                '[run_step ' + str(self.simulation.execute) + '] sender: %d\n' % int(
                                    self.myknowledge.service['senderID']))
        # pdb.set_trace()
        if self.amIHelping(int(self.myknowledge.service['senderID'])):
            # You need to count loops

            self.log.write_log_file(self.log.stdout_log,
                                    '[run_step ' + str(self.simulation.execute) + '] service %s, threads: %s\n' % (
                                    self.myknowledge.service, str(self.keep_track_threads)))

            index = next(index for (index, d) in enumerate(self.keep_track_threads) if d['senderId'] == int(self.myknowledge.service['senderID']))

            if self.is_thread_active(int(self.myknowledge.service['senderID'])):
                if result == 1:
                    self.keep_track_threads[index]['task_status'] = 1
                else:
                    self.keep_track_threads[index]['task_status'] = 0
                self.log.write_log_file(self.log.stdout_log,
                                        '[run_step ' + str(self.simulation.execute) + '] Threads %s\n' % str(
                                            self.keep_track_threads))
            else:
                self.keep_track_threads[index]['task_status'] = 10
                self.log.write_log_file(self.log.stdout_log,
                                        '[run_step ' + str(self.simulation.execute) + '] End of task, but thread not active anymore Threads %s\n' % str(
                                            self.keep_track_threads))

        if (sum(self.simulation.no_tasks_attempted) - sum(self.simulation.no_tasks_depend_attempted)) == 0:
            self.mycore.self_esteem = 0.0
        else:
            self.mycore.self_esteem = (sum(self.simulation.no_tasks_completed) - sum(
                self.simulation.no_tasks_depend_completed)) / float(
                sum(self.simulation.no_tasks_attempted) - sum(self.simulation.no_tasks_depend_attempted))
        # Record
        self.simulation.theta_esteem.append(self.mycore.self_esteem)
        self.simulation.theta_tu.append(task_urgency)
        self.simulation.theta_ti.append(task_importance)
        self.simulation.theta_culture.append(culture)
        self.simulation.theta_candidate.append(success_chance)
        self.simulation.theta.append(theta)
        if req_missing:
            self.simulation.theta_deps.append(1)
        else:
            self.simulation.theta_deps.append(0)
        self.simulation.theta_health.append(sum([self.mycore.sensmot, self.mycore.battery]))
        self.simulation.theta_bool.append(depend)
        # Inc to reach stop of simulation
        if self.myknowledge.service['senderID'] == self.mycore.ID:
            self.simulation.stopINC += 1
            print 'STOP INC: %d' % self.simulation.stopINC

        self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(
            self.simulation.execute) + '] STOP INC: %d\n' % self.simulation.stopINC)

    def regenerate(self):
        # print 'im in regenerate'
        self.simulation.regenerate = self.simulation.inc_iterationstamps(self.simulation.regenerate)

        self.debug_self()
        self.fix_bugs()

    def dead(self):
        # print 'im in dead'
        self.simulation.dead = self.simulation.inc_iterationstamps(self.simulation.dead)
        self.log.write_log_file(self.log.stdout_log, 'In dead - should return')

        self.evaluate_self()
        self.evaluate_environment()
        self.evaluate_selfmending()

        self.publish_bcast[0].publish(self.mycore.create_message('DIE', 'DIE'))
        self.reason = 'Simulation end - in the dead state'
        rospy.signal_shutdown(self.reason)
        rospy.on_shutdown(self.my_hook)

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

        if random.random() > 0.8:
            it = [100, 400, 700]
            en = [1, 10, 30]
            re = [50, 150, 350]
            ab = [['walk'], ['walk', 'talk'], ['walk', 'talk', 'smoke']]
            risurs = [['pringles'], ['pringles', 'brie'], ['pringles', 'brie', 'beer']]
            etime = [130, 1300, 2300]

            difficulty = -1

            for x in self.simulation.generated_tasks:
                if x < 50:
                    difficulty = self.simulation.generated_tasks.index(x)
                    break

            if difficulty == -1:
                return

            self.simulation.generated_tasks[difficulty] += 1
            self.log.write_log_file(self.log.stdout_log, '[generate goal ' + str(self.simulation.idle) + '] ' + str(self.simulation.generated_tasks) + '\n')

            senderId = self.mycore.ID
            planId = -random.randint(1, 100)
            tID = random.randint(1, 3)
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

            self.log.write_log_file(self.log.stdout_log,
                                    '[generate goal ' + str(self.simulation.idle) + '] Chosen service: ' + str(
                                        tasks) + '\n')

            for x in tasks:
                self.log.write_log_file(self.log.stdout_log,
                                        '[generate goal ' + str(self.simulation.idle) + '] ' + str(x) + '\n')
                self.myknowledge.task_queue.put(x)

            self.myknowledge.lock.acquire()
            self.mycore.state = 2
            self.myknowledge.lock.release()
        else:
            self.log.write_log_file(self.log.stdout_log, '[generate goal ' + str(
                self.simulation.idle) + '] do nothing - zot jepi atij qe rri kot :DD\n')

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

    def update_culture(self, help, expertise, load):
        pass

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
            print 'rospy is shutdown'

    def init_serve(self, agentid):
        myservice = '/robot' + str(agentid) + '/serve'
        # print 'DECLARING my service'
        srv = rospy.Service(myservice, Protocol_Srv, self.handle_serve)

    def handle_serve(self, request):
        pass

    def call_serve(self, server, myid, request, anyone_index):
        pass
