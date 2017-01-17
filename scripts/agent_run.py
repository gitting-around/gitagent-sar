#!/usr/bin/env python
import sys
import rospy
import agent0
import simulation
import mylogging
from gitagent.msg import *
from gitagent.srv import *
import traceback
import time
from threading import Lock
import numpy as np
import pdb


class GitAgent(agent0.Agent0):
    def bcasts_brain_callback(self, data):
        rospy.loginfo(rospy.get_caller_id() + " Callback-from-env-mpunit %s, %s", data.sender, data.content)

        # callback_bc modified ONLY here
        self.simulation.callback_bc = self.simulation.inc_iterationstamps(self.simulation.callback_bc)
        print 'SIM', self.simulation.callback_bc

        # self.register_new_people(data)
        self.process_bc_request(data)

    def process_bc_request(self, data):

        self.log.write_log_file(self.log.stdout_callback,
                                '[callback ' + str(self.simulation.callback_bc) + '][ROSPY] I am: %d, I heard %d\n' % (
                                self.mycore.ID, int(data.sender)))
        # Register new individual - Note that what comes from msg_PUnit is always new
        # However, in the case additional planners are added this code must be changed appropriately
        self.register_sender(data)

        # Process the request based on the performative
        if data.performative == 'highlevelplan':
            # Add the plan/task in the request in the plan_eval queue
            plan = filter(None, data.content.split('\n'))
            planId = plan.pop(0)
            plan = filter(None, plan[0].split('$'))
            plan.pop(0)
            plan = filter(None, plan[0].split('#'))
            self.log.write_log_file(self.log.stdout_callback,
                                    '[callback ' + str(self.simulation.callback_bc) + ']' + str(plan) + '\n\n')

            tasks = self.simulation.string2dict(plan, planId, data.sender)
            self.log.write_log_file(self.log.stdout_callback,
                                    '[callback ' + str(self.simulation.callback_bc) + '] ' + str(tasks) + '\n\n')
            self.myknowledge.plan_pending_eval.put(tasks)
            self.log.write_log_file(self.log.stdout_callback,
                                    '[callback ' + str(self.simulation.callback_bc) + '] new plan into queue\n\n')

    def register_sender(self, data):
        guy_id_srv = []
        if not data.performative == 'highlevelplan':
            guy_id_srv = [int(data.sender), -1]
            guy_id_srv.append([int(x) for x in filter(None, data.content.split('|'))])
            exp = []
            self.log.write_log_file(self.log.stdout_callback,
                                    '[callback ' + str(self.simulation.callback_bc) + '] ' + str(guy_id_srv) + '\n')
            self.log.write_log_file(self.log.stdout_callback,
                                    '[callback ' + str(self.simulation.callback_bc) + '] ' + str(guy_id_srv[2]) + '\n')
            for x in range(0, len(guy_id_srv[2])):
                exp.append(-1)
            guy_id_srv.append(exp)
            self.log.write_log_file(self.log.stdout_callback,
                                    '[callback ' + str(self.simulation.callback_bc) + '] ' + str(guy_id_srv) + '\n')
        else:
            self.log.write_log_file(self.log.stdout_callback,
                                    '[callback ' + str(self.simulation.callback_bc) + ']' + str(data) + '\n')
            guy_id_srv = [int(data.sender), -1]
            guy_id_srv.append([])
            exp = []
            guy_id_srv.append(exp)

        self.myknowledge.lock.acquire()
        self.myknowledge.known_people.append(guy_id_srv)
        self.myknowledge.helping_interactions.append(0)
        self.myknowledge.total_interactions.append(0)
        temp_values = []
        for x in range(0, len(guy_id_srv[2])):
            temp_values.append([0, 0])
        self.myknowledge.capability_expertise.append(temp_values)
        self.myknowledge.lock.release()

        self.log.write_log_file(self.log.stdout_callback,
                                '[callback ' + str(self.simulation.callback_bc) + '] known people ' + str(
                                    self.myknowledge.known_people) + '\n')

        self.log.write_log_file(self.log.stdout_callback,
                                '[callback ' + str(self.simulation.callback_bc) + '] capability_expertise ' + str(
                                    self.myknowledge.capability_expertise) + '\n')

    def init_inputs(self, inputs):
        for x in inputs:
            rospy.Subscriber(x[0], Protocol_Msg, getattr(self, x[1]))

    def handle_serve(self, request):
        idx = -1

        print 'HANDLING'
        self.myknowledge.lock.acquire()
        self.simulation.handle = self.simulation.handle + 1
        local_handle = self.simulation.handle
        if int(request.sender) in self.myknowledge.current_client:
            idx = self.myknowledge.current_client.index(int(request.sender))
            self.myknowledge.service_resp[idx] = False
            self.myknowledge.service_resp_content[idx] = -1
            self.myknowledge.service_req[idx] = int(request.content)
            self.adaptive_state[idx] = True
            print 'HANDLING3'
        else:
            self.myknowledge.service_req.append(int(request.content))
            self.myknowledge.current_client.append(int(request.sender))
            self.myknowledge.service_resp.append(False)
            self.myknowledge.service_resp_content.append(-1)
            idx = self.myknowledge.current_client.index(int(request.sender))
            self.adaptive_state.append(True)
            print 'HANDLING4'
        print 'HANDLING5'
        self.log.write_log_file(self.log.stdout_handle, '[handle_serve ' + str(
            local_handle) + '] request.content: ' + request.content + '\n' + '[handle_serve ' + str(
            local_handle) + '] request.id: ' + str(request.sender) + '\n' + '[handle_serve ' + str(
            local_handle) + '] ' + 'Receiving request from: %d, for task: %d. Current client: %d\n' % (
                                int(request.sender), self.myknowledge.service_req[idx],
                                self.myknowledge.current_client[idx]) + '[handle_serve ' + str(
            local_handle) + '] service_resp: %s\n' % str(self.myknowledge.service_resp[idx]))

        ## normally here would be a good place for filters ;)
        timeout = time.time() + 30  # stop loop 30 sec from now

        self.myknowledge.lock.release()

        while not self.myknowledge.service_resp[idx]:
            # time.sleep(0.1)

            if time.time() > timeout:
                self.myknowledge.lock.acquire()
                self.myknowledge.timeouts = self.myknowledge.timeouts + 1
                self.myknowledge.service_resp_content[idx] = -1
                self.adaptive_state[idx] = False
                self.log.write_log_file(self.log.stdout_handle,
                                        '[handle_serve ' + str(local_handle) + '] timeout, id: ' + str(
                                            self.myknowledge.current_client[idx]) + ' current adapt step: ' + str(
                                            self.simulation.interact) + '\n')
                self.myknowledge.lock.release()
                break

        reply_to = str(self.myknowledge.service_resp_content[idx])
        self.myknowledge.lock.acquire()
        self.log.write_log_file(self.log.stdout_handle, '[handle_serve ' + str(
            local_handle) + '] request outgoing ' + reply_to + ', client id' + str(
            self.myknowledge.current_client[idx]) + ' current adapt step: ' + str(self.simulation.interact) + '\n')
        self.myknowledge.lock.release()

        return reply_to

    def call_serve(self, server, myid, request, anyone_index):

        print 'im here in call serve'
        other_service = '/robot' + str(server) + '/serve'
        print other_service
        self.simulation.call = self.simulation.call + 1
        print self.simulation.call

        self.log.write_log_file(self.log.stdout_log,
                                '[call_serve ' + str(self.simulation.call) + '] ' + 'I am %d calling: %s\n' % (
                                self.mycore.ID, other_service))

        self.myknowledge.lock.acquire()
        self.myknowledge.total_interactions[anyone_index] = self.myknowledge.total_interactions[anyone_index] + 1
        self.myknowledge.lock.release()

        service_idx = self.myknowledge.known_people[anyone_index][2].index(int(request))
        print service_idx
        self.myknowledge.lock.acquire()
        self.myknowledge.capability_expertise[anyone_index][service_idx][1] = \
        self.myknowledge.capability_expertise[anyone_index][service_idx][1] + 1
        self.myknowledge.lock.release()

        rospy.wait_for_service(other_service, timeout=60)
        try:
            self.log.write_log_file(self.log.stdout_log, '[call_serve ' + str(
                self.simulation.call) + '] ' + 'inside try block, time: %s\n' % str(time.time()))
            serve = rospy.ServiceProxy(other_service, Protocol_Srv)

            resp1 = serve('serveme', str(myid), 1, 'shqip', 'shenanigans', 'none', 'reply_with', request, 'prot')
            print resp1.reply_to

            self.log.write_log_file(self.log.stdout_log, '[call_serve ' + str(
                self.simulation.call) + '] ' + 'resp1.outgoing: %s\n' % resp1.reply_to)
            if not int(resp1.reply_to) == -1:
                self.myknowledge.lock.acquire()
                self.myknowledge.helping_interactions[anyone_index] = self.myknowledge.helping_interactions[
                                                                          anyone_index] + 1
                self.myknowledge.lock.release()

                if int(resp1.reply_to) == 1:
                    self.myknowledge.lock.acquire()
                    self.myknowledge.capability_expertise[anyone_index][service_idx][0] = \
                    self.myknowledge.capability_expertise[anyone_index][service_idx][0] + 1
                    self.myknowledge.lock.release()

            # Calculate perceived willingness
            self.myknowledge.lock.acquire()
            self.myknowledge.known_people[anyone_index][1] = self.myknowledge.helping_interactions[
                                                                 anyone_index] / float(
                self.myknowledge.total_interactions[anyone_index])
            self.myknowledge.lock.release()

            self.log.write_log_file(self.log.stdout_log, '[call_serve ' + str(
                self.simulation.call) + '] ' + 'perceived willingness from server: %d, is: %f\n' % (
                                    server, self.myknowledge.known_people[anyone_index][1]))
            # Calculate perceived expertise for the service
            self.myknowledge.lock.acquire()
            self.myknowledge.known_people[anyone_index][3][service_idx] = \
            self.myknowledge.capability_expertise[anyone_index][service_idx][0] / float(
                self.myknowledge.capability_expertise[anyone_index][service_idx][1])
            self.myknowledge.lock.release()

            self.log.write_log_file(self.log.stdout_log, '[call_serve ' + str(
                self.simulation.call) + '] ' + 'perceived expertise from server: %d, is: %f\n' % (server,
                                                                                                  self.myknowledge.known_people[
                                                                                                      anyone_index][3][
                                                                                                      service_idx]) + '[call_serve ' + str(
                self.simulation.call) + '] ' + 'capability expertise: ' + str(
                self.myknowledge.capability_expertise) + '\n')

            # Update perceived culture
            self.update_culture(
                float(sum(self.myknowledge.helping_interactions)) / float(sum(self.myknowledge.total_interactions)),
                self.myknowledge.capability_expertise, 1)

            return resp1.reply_to
        except rospy.ServiceException, e:
            self.log.write_log_file(self.log.stdout_log, '[call_serve ' + str(
                self.simulation.call) + '] ' + 'Service call failed: %s, at time %s' % (e, str(time.time())))
            self.myknowledge.conn_reset = self.myknowledge.conn_reset + 1
            pass

    def update_culture(self, help, expertise, load):
        # self.myknowledge.culture = [x + y for x, y in zip(self.myknowledge.culture, [help, expertise, load])]
        # expertise = [[[2,4],[3,5],[1,2]], [[3,3],[3,7],[1,2]], [[5,6],[7,8],[1,2]]]

        self.myknowledge.culture[0] = help

        total_expertise = np.sum(np.sum(expertise, axis=1), axis=0)
        self.myknowledge.culture[1] = float(total_expertise[0]) / float(total_expertise[1])

        self.myknowledge.culture[2] = load
        self.log.write_log_file(self.log.stdout_log,
                                '[call_serve ' + str(self.simulation.call) + '] ' + 'Culture: ' + str(
                                    self.myknowledge.culture) + ' ' + str([help, expertise, load]) + '\n')

        self.log.write_log_file(self.log.stdout_log,
                                '[call_serve ' + str(self.simulation.call) + '] ' + 'Culture: ' + str(help) + '\n')


if __name__ == '__main__':

    # sys.stdout = s

    rospy.init_node('agent', anonymous=True)
    # define the three core elements of the agent, its id, delta and theta value ###
    agent_id = rospy.get_param('brain_node/myID')
    delta = rospy.get_param('brain_node/myDelta')
    theta = rospy.get_param('brain_node/myTheta')
    depends = rospy.get_param('brain_node/myDepend')
    ##############################################################################
    stderr_file = '/home/mfi01/catkin_ws/results/error_brain' + str(agent_id)
    f = open(stderr_file, 'w+')
    orig_stderr = sys.stderr
    sys.stderr = f

    stdout_file = '/home/mfi01/catkin_ws/results/stdout_brain'
    s = open(stdout_file, 'w+')
    orig_stdout = sys.stdout
    rospy.loginfo('Agent with id: %d, delta: %f, theta: %f, has started successfully', agent_id, delta, theta)
    # Define the inputs/outputs to the agent (sensors, such as vision, tactile, message input etc)###
    # They will be given as topic names
    # This example consists of only the message channel
    # [[topic_name, callback_function], [], ...]
    inputs = [['bcasts_brain', 'bcasts_brain_callback']]
    sensors = [200]

    outputs = ['bcasts', '/environment/agent_position']
    actuators = [200]
    motors = []
    # Give a list of function names that represent the capabilities of the agent
    sim = simulation.Simulation0()

    agentfile = "conf_" + str(agent_id)
    # Read agent configuration file
    agent_conf = sim.read_agent_conf(agentfile)
    print agent_conf
    # From the list of services select 30% (this number can be modified) for the agent to be providing - at random
    # [id time energy reward ...] ... -> dependencies on other services for instance 4 5 2 1
    # Active_servs format: [[5, 100, 3705, 42], [6, 97, 5736, 19], [9, 96, 9156, 4]]
    active_servs = sim.select_services(agent_id, depends)

    # Health specification
    battery = 10000
    ################################################################################################
    popSize = 2
    provaNr = 2
    agent = GitAgent(agent_id, agent_conf, active_servs, [theta, delta], sim, popSize, provaNr, depends, battery, sensors,
                     actuators, motors)
    agent.log.write_log_file(agent.log.stdout_log, 'active_serve ' + str(active_servs) + '\n')

    try:
        agent.fsm()
    # time.sleep(200)
    except rospy.ROSInterruptException:
        traceback.print_exc()
        raise
    except (AttributeError, TypeError, ValueError, NameError):
        traceback.print_exc()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc()
        raise
    finally:
        # Write out number of help requests and approx finishing time
        agent.log.write_log_file(agent.log.stdout_log, 'in finally')
        # pdb.set_trace()
        results_filename = '/home/mfi01/catkin_ws/results/test/pop_size.' + str(popSize) + '/prova.' + str(
            provaNr) + '/results_' + str(agent_id) + '_' + str(delta) + '_' + str(depends)

        # Write out times it takes for the logic to return
        for x in agent.simulation.fuzzy_time:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')

        # reqE      reqM        reqH        timeE       timeM       timeH

        agent.log.write_log_file(results_filename, str(agent.simulation.requests[0]) + '         ' + str(agent.simulation.requests[1])
                                 + '            ' + str(agent.simulation.requests[2]) + '       ' + str(agent.simulation.exec_times[0])
                                 + '        ' + str(agent.simulation.exec_times[1]) + '         ' + str(agent.simulation.exec_times[2]) + '\n'
                                 + str(agent.simulation.required_missing_noreq) + '\n')

        # Factor track
        for x in agent.mycore.factor_track:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Jobs attempted
        agent.log.write_log_file(results_filename, '%d\n' % agent.myknowledge.attempted_jobs)

        # TA  TDA TC  TDC
        for x in agent.simulation.no_tasks_attempted:
            agent.log.write_log_file(results_filename, str(x) + ' ')
        for x in agent.simulation.no_tasks_depend_attempted:
            agent.log.write_log_file(results_filename, str(x) + ' ')
        for x in agent.simulation.no_tasks_completed:
            agent.log.write_log_file(results_filename, str(x) + ' ')
        for x in agent.simulation.no_tasks_depend_completed:
            agent.log.write_log_file(results_filename, str(x) + ' ')
        for x in agent.simulation.no_self_tasks_completed:
            agent.log.write_log_file(results_filename, str(x) + ' ')
        for x in agent.simulation.no_self_tasks_completed:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')

        # Theta
        for x in agent.simulation.theta:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Esteem
        for x in agent.simulation.theta_esteem:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Task urgency
        for x in agent.simulation.theta_tu:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Task importance
        for x in agent.simulation.theta_ti:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Culture
        for x in agent.simulation.theta_culture:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Candidate
        for x in agent.simulation.theta_candidate:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Dependencies (required)
        for x in agent.simulation.theta_deps:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Health
        for x in agent.simulation.theta_health:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Theta_bool
        for x in agent.simulation.theta_bool:
            if x:
                agent.log.write_log_file(results_filename, str(1) + ' ')
            else:
                agent.log.write_log_file(results_filename, str(0) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        #pdb.set_trace()
        # Gamma
        for x in agent.simulation.gamma:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Esteem
        for x in agent.simulation.gamma_esteem:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Task urgency
        for x in agent.simulation.gamma_tu:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Task importance
        for x in agent.simulation.gamma_ti:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Culture
        for x in agent.simulation.gamma_culture:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Candidate
        for x in agent.simulation.gamma_candidate:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Dependencies (required)
        for x in agent.simulation.gamma_deps:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Health
        for x in agent.simulation.gamma_health:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        # Gamma_bool
        for x in agent.simulation.gamma_bool:
            if x:
                agent.log.write_log_file(results_filename, str(1) + ' ')
            else:
                agent.log.write_log_file(results_filename, str(0) + ' ')

        agent.log.write_log_file(results_filename, '\n')

        # Gamma request goodness
        for x in agent.simulation.gamma_req_goodness:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        agent.log.write_log_file(results_filename, '\n')
        #pdb.set_trace()
        # exec_times
        for x in agent.simulation.exec_times_depend:
            agent.log.write_log_file(results_filename, str(x) + ' ')

        sys.stderr = orig_stderr
        f.close()
        sys.stdout = orig_stdout
        s.close()
