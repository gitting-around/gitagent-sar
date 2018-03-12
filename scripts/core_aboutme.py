#!/usr/bin/env python
import sys
import random
import mylogging
from gitagent.msg import *
import time
import numpy as np

#import skfuzzy as fuzz
#from skfuzzy import control as ctrl
import rospy
import pdb


class Core:
    def __init__(self, willingness, ID, battery, sensors, actuators, motors, memory):
        # willingness - [gamma, delta]
        self.willingness = willingness
        # Willingness to ask for assistance
        self.ask = False

        # Willingness to give assistance
        self.give = False

        # Thresholds -- percentage of affordance
        self.LOW = 0.0
        msg = "CORE: low: %f" % (self.LOW)
        rospy.loginfo(msg)
        self.HIGH = 0.7
        self.MEDium = 0.5

        # start always in idle
        self.state = 0

        # Keep track of which factor has influenced the decision to give help
        # health abilities resources self-esteem task_urgency task_importance
        self.factor_track = [0, 0, 0, 0, 0, 0]
        self.factor_track_give = [0, 0, 0, 0, 0, 0, 0]
        # start always in idle
        self.state = 0

        # agent name (unique -- it has to uniquely point to some agent)
        self.ID = ID

        # Battery levels
        #self.battery = battery
        self.battery = 1.0

        # 3 arrays which keep the states for sensors, actuators, motors
        self.sensors = sum(sensors)
        self.actuators = sum(actuators)
        self.motors = sum(motors)
        self.sensmot = sum([self.sensors, self.actuators, self.motors])

        # This is the minimum value for the battery levels in which it could be
        # considered that the agent works properly
        #self.battery_min = 300
        self.battery_min = 0.3
        self.sensmot_min = 300
        self.self_esteem = 0.5

        # This could be an array, in which each element represents health over some dimension
        self.check_health()

        self.gamma = self.willingness[0]
        self.delta = self.willingness[1]

        self.gamma_in_time = []
        self.delta_in_time = []

        self.step = 0.05
        self.considerable_change = 0.0

        self.env_risk = 0.0
        self.ag_risk = []
        self.performance = 0.0

        self.arisk = {}

        self.drop_rate = 0.0

        self.memory = memory
        self.ten_shots = []

        self.amIblocking = False

        self.active_people_ids = []

    # Function will return True if decided to ask for help, or False otherwise
    def ask_4help(self, health, abilities, resources, self_esteem, task_urgency, task_importance, culture,
                  best_candidate):
        self.ask = False
        theta = -1.0
        # 4400 is the starting value for energy
        health /= float(4800)

        if health < self.LOW:
            self.factor_track[0] += 1
            theta = 1.0
        else:
            if abilities < self.LOW:
                theta = 1.0
                self.factor_track[1] += 1
            else:
                if resources < self.LOW:
                    theta = 1.0
                    self.factor_track[2] += 1
                else:
                    if self_esteem < self.HIGH:
                        if task_urgency > self.LOW or task_importance > self.LOW:
                            #theta = max([task_urgency, task_importance])
                            theta = (task_importance + task_importance)/float(2)
                            self.factor_track[3] += 1
                        else:
                            if culture > self.LOW and best_candidate > self.LOW:
                                #theta = max([culture, best_candidate])
                                theta = (culture + best_candidate)/float(2)
                                self.factor_track[4] += 1
                    else:
                        if culture > self.HIGH and best_candidate > self.HIGH:
                            if task_urgency > self.LOW or task_importance > self.LOW:
                                #theta = max([task_urgency, task_importance])
                                theta = (task_importance + task_urgency)/float(2)
                                self.factor_track[5] += 1

        if random.random() <= theta:
            return True, theta
        else:
            return False, theta

    def ask_5help(self, health, abilities, resources):
        self.ask = False
        theta = -1.0
        # 4400 is the starting value for energy
        health /= float(4800)

        if health < self.LOW:
            self.factor_track[0] += 1
            theta = 1.0
        else:
            if abilities < self.LOW:
                theta = 1.0
                self.factor_track[1] += 1
            else:
                if resources < self.LOW:
                    theta = 1.0
                    self.factor_track[2] += 1

        if random.random() <= theta:
            return True, theta
        else:
            return False, theta

    def ask_6help(self, health, abilities, resources, self_esteem, t_urgency, t_importance, culture, best_candidate):
        self.ask = False
        theta = -1.0
        # 4400 is the starting value for energy
        health /= float(4800)

        if health < self.LOW:
            self.factor_track[0] += 1
            theta = 1.0
        else:
            if abilities < self.LOW:
                theta = 1.0
                self.factor_track[1] += 1
            else:
                if resources < self.LOW:
                    theta = 1.0
                    self.factor_track[2] += 1
                else:
                    theta = np.mean([self_esteem, t_importance, t_urgency, culture, best_candidate])

        if random.random() <= theta:
            return True, theta
        else:
            return False, theta

    # Function will return True if decided to give help, or False otherwise
    def give_help(self, health, abilities, resources, self_esteem, task_urgency, task_importance, culture, request_goodness, perceived_help):
        # pdb.set_trace()
        self.give = True
        gamma = 1.0

        if health < self.LOW:
            self.factor_track_give[0] += 1
            gamma = -1.0
        else:
            if abilities < self.LOW:
                self.factor_track_give[1] += 1
                gamma = -1.0
            else:
                if resources < self.LOW:
                    self.factor_track_give[2] += 1
                    gamma = -1.0
                else:
                    if request_goodness < self.LOW:
                        self.factor_track_give[3] += 1
                        gamma = -1.0
                    else:
                        if self_esteem < self.LOW:
                            self.factor_track_give[4] += 1
                            gamma = self_esteem
                        else:
                            if perceived_help < self.LOW:
                                self.factor_track_give[5] += 1
                                gamma = perceived_help
                            else:
                                if self.state == 2:
                                    if task_urgency > self.LOW or task_importance > self.LOW:
                                        self.factor_track_give[6] += 1
                                        gamma = (task_urgency + task_importance)/float(2)

        if random.random() <= gamma:
            return True, gamma
        else:
            return False, gamma

    # This function can perform some 'health' analysis on the state of different parts of the system.
    def check_health(self):
        if self.battery <= self.battery_min or self.sensmot <= self.sensmot_min:
            # Levels not acceptable ---> change state to dead
            if not self.state == 3:
                self.state = 4

    def best_candidate(self, known_people, task, log, senderID):
        #pdb.set_trace()
        # Assume that agent's can do the tasks
        #print known_people
        try:
            success_chance = -1
            agent_id = -1
            agent_idx = -1

            # Find in known people the subset of agents that can do the task
            subset = []
            subset_unknown = []
            subset_proxies = []
            if known_people:
                # print 'known people not empty'
                # print 'task id type ' + str(type(task['id']))
                for x in known_people:
                    print x[2]
                    #if task['id'] in x[2]:
                    #CAREFUL - does not consider case when x[2] is a list itself, i.e. when there are multiple abilities required
                    if x[2][0] in task['abilities']:
                        if not senderID == x[0] and not x[0] in task['ac_senders']:
                            subset.append(x)
                            if int(x[1]) == -1:
                                subset_unknown.append(x)
                    if x[2][0] == 'proxy':
                        if not senderID == x[0] and not x[0] in task['ac_senders']:
                            subset_proxies.append(x)

                print subset
                msg = "subset of known people that can do the job: %s" % str(subset)
                log.write_log_file(log.stdout_log, msg)
                if subset:
                    if random.random() < 0.4:
                        # Choose an agent randomly
                        #print 'random'
                        if subset_unknown:
                            agent_idx = random.randint(0, len(subset_unknown) - 1)
                            print subset_unknown[agent_idx][0]
                            success_chance = subset_unknown[agent_idx][1]
                            print success_chance
                            agent_id = subset_unknown[agent_idx][0]
                        else:
                            agent_idx = random.randint(0, len(subset) - 1)
                            print subset[agent_idx][0]
                            success_chance = subset[agent_idx][1]
                            print success_chance
                            log.write_log_file(log.stdout_log, 'Randomly chosen: %d\n' % subset[agent_idx][0])
                            agent_id = subset[agent_idx][0]
                    else:
                        # Select the one which has been most helpful in the past
                        #print 'lambda'
                        agent_idx = subset.index(max(subset, key=lambda x: x[1]))

                        print subset[agent_idx][0]
                        success_chance = subset[agent_idx][1]
                        print success_chance
                        log.write_log_file(log.stdout_log, 'lambda chosen: %d\n' % subset[agent_idx][0])

                        agent_id = subset[agent_idx][0]
                    # Find the corresponding id in known_people
                    for x in known_people:
                        if x[0] == agent_id:
                            #print 'element found'
                            agent_idx = known_people.index(x)
                            #print agent_idx
                            log.write_log_file(log.stdout_log, 'index: %d\n' % agent_idx)
                else:
                    # In case ambulance agents cannot find other ambulances, then can ask police officers for help
                    msg = 'looking for proxies\n'
                    log.write_log_file(log.stdout_log, msg)
                    if 'transport_victim' in task['abilities']:
                        #pdb.set_trace()
                        if subset_proxies:
                            msg = 'No ambulance to ask, try fire police\n'
                            log.write_log_file(log.stdout_log, msg)
                            agent_idx = random.randint(0, len(subset_proxies) - 1)
                            print subset_proxies[agent_idx][0]
                            success_chance = subset_proxies[agent_idx][1]
                            print success_chance
                            msg = 'Randomly chosen proxy: %d\n' % subset_proxies[agent_idx][0]
                            log.write_log_file(log.stdout_log, msg)
                            agent_id = subset_proxies[agent_idx][0]
                            for x in known_people:
                                if x[0] == agent_id:
                                    # print 'element found'
                                    agent_idx = known_people.index(x)
                                    # print agent_idx
                                    msg = 'index: %d\n' % agent_idx
                        else:
                            msg = 'No proxies for this task\n'
                            log.write_log_file(log.stdout_log, msg)
                    else:
                        msg = 'No one to ask for this task\n'
                        log.write_log_file(log.stdout_log, msg)
                    #print 'no one for this task'
            else:
                #print 'no one'
                log.write_log_file(log.stdout_log, 'No one to ask \n')

            return success_chance, agent_id, agent_idx
        except:
            msg = "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno)
            log.write_log_file(log.stdout_log, msg)

    def best_candidate_list(self, known_people, task, log, senderID):
        try:

            # Find in known people the subset of agents that can do the task
            subset = []
            subset_proxies = []
            sorted_subset = []
            msg = "known_people: %s" % str(known_people)
            log.write_log_file(log.stdout_log, msg)
            if known_people:
                # print 'known people not empty'
                # print 'task id type ' + str(type(task['id']))
                #pdb.set_trace()
                for x in known_people:
                    print x[2]
                    #if task['id'] in x[2]:
                    #CAREFUL - does not consider case when x[2] is a list itself, i.e. when there are multiple abilities required
                    if x[2][0] in task['abilities']:
                        if not senderID == x[0] and not x[0] in task['ac_senders']:
                            t = list(x)
                            t.append(known_people.index(x))
                            subset.append(t)
                    if x[2][0] == 'proxy':
                        if not senderID == x[0] and not x[0] in task['ac_senders']:
                            t = list(x)
                            t.append(known_people.index(x))
                            subset_proxies.append(t)

                # [ [9, -1, ['transport_victim'], [-1]], ... ]
                # put -1 ones first
                sorted_subset = sorted(subset, key=lambda x: int(x[1]))

                msg += "subset of known people that can do the job: %s, sorted: %s" % (str(subset), str(sorted_subset))
                log.write_log_file(log.stdout_log, msg)

                if subset:
                    # In case ambulance agents cannot find other ambulances, then can ask police officers for help
                    msg += 'looking for proxies\n'
                    log.write_log_file(log.stdout_log, msg)
                    if 'transport_victim' in task['abilities']:
                        if subset_proxies:
                            sorted_proxies = sorted(subset_proxies, key=lambda x: int(x[1]))
                            msg += 'No ambulance to ask, try fire police\n'
                            sorted_subset = sorted_subset + sorted_proxies
                            log.write_log_file(log.stdout_log, msg)
                        else:
                            msg += 'No proxies for this task\n'
                            log.write_log_file(log.stdout_log, msg)
                else:
                    msg += 'No one to ask for this task\n'
                    log.write_log_file(log.stdout_log, msg)
                    #print 'no one for this task'
            else:
                #print 'no one'
                log.write_log_file(log.stdout_log, 'No one to ask \n')
            return sorted_subset
        except:
            msg += "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno)
            log.write_log_file(log.stdout_log, msg)

    def battery_change(self, change):
        self.battery = self.battery - change

    # It might be possible to introduce random issues here, i.e. aggravate the change of 'health'
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
        # print message
        return message

    def create_msg_content(self, raw_content, tipmsg):
        content = ''
        if tipmsg == 'position':
            for x in raw_content:
                content = content + str(x) + '|'
        elif tipmsg == 'DIE':
            content = 'DIE'
        else:
            #rospy.loginfo("raw_content: %s", str(raw_content))
            for x in raw_content:
                #rospy.loginfo("raw_content: %s", x)
                content = content + str(x) + '|'
        return content

    def goal2string(self, log, goal):
        #pdb.set_trace()
        try:
            abil = ''
            # ADD the quantity!!!
            for x in goal['abilities']:
                abil = abil + str(x) + ':' + str(goal['abilities'][x])  + ','
            eloc = str(goal['endLoc'][0]) + ',' + str(goal['endLoc'][1])
            sloc = str(goal['startLoc'][0]) + ',' + str(goal['startLoc'][1])
            # ADD the quantity!!!
            res = ''
            for x in goal['resources']:
                res = res + str(x) + ':' + str(goal['resources'][x]) + ','
            equip = ''
            print goal['equipment']
            for x in goal['equipment']:
                for y in x:
                    equip = equip + str(y) + ','
                equip = equip + '|'
            # Basically it is being assumed that only one goal passes through -- change this to send plans
            ac_snd = ''
            for x in goal['ac_senders']:
                ac_snd += str(x) + ','

            goal = abil + ' ' + str(goal['estim_time']) + ' ' + str(goal['senderID']) + ' ' + str(
                goal['energy']) + ' ' + str(goal['iterations']) + ' ' + str(goal['id']) + ' ' + goal[
                       'name'] + ' ' + eloc + ' ' + str(goal['planID']) + ' ' + equip + ' ' + sloc + ' ' + str(
                goal['reward']) + ' ' + res + ' ' + str(goal['noAgents']) + ' ' + str(goal['simulation_finish']) + ' ' + ac_snd + '\n'

            msg = "CORE: goal2string: " + str(goal)
            log.write_log_file(log.stdout_log, msg)
            return goal
        except:
            msg = "CORE: Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno)
            log.write_log_file(log.stdout_log, msg)

    def string2goal(self, line, log):
        try:
            # halloumi, 15.8918374114 1 46 8 56 randomCrap 5,6 -8 pip,|pop,|pup,| 2,3 41 mozarella, 3
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % line)
            line = filter(None, line.split(' '))
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % line)
            abilities = [x for x in filter(None, line[0].split(','))]
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % abilities)
            estim_time = float(line[1])
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %f\n' % estim_time)
            senderId = line[2]
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % senderId)
            energy = int(line[3])
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % energy)
            iterations = int(line[4])
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % iterations)
            tID = int(line[5])
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % tID)
            tName = line[6]
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % tName)
            endLoc = [x for x in filter(None, line[7].split(','))]
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % endLoc)
            planId = line[8]
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % planId)
            equipment = [filter(None, x.split(',')) for x in filter(None, line[9].split('|'))]
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % equipment)
            startLoc = [x for x in filter(None, line[10].split(','))]
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % startLoc)
            reward = int(line[11])
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % reward)
            res = [x for x in filter(None, line[12].split(','))]
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % res)
            noAgents = int(line[13])
            log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % noAgents)
            ac_snd = [int(x) for x in filter(None, line[14].split(','))]

            return {'senderID': senderId, 'planID': planId, 'id': tID, 'iterations': iterations, 'energy': energy,
                    'reward': reward, 'name': tName, 'startLoc': startLoc, 'endLoc': endLoc, 'noAgents': noAgents,
                    'equipment': equipment, 'abilities': abilities, 'resources': res, 'estim_time': estim_time, 'ac_senders': ac_snd}
        except:
            log.write_log_file(log.stdout_log, "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))

    def string2goalPlan(self, lines, log):
        # halloumi, 15.8918374114 1 46 8 56 randomCrap 5,6 -8 pip,|pop,|pup,| 2,3 41 mozarella, 3
        try:
            plan = []
            lines = filter(None, lines.split('\n'))
            log.write_log_file(log.stdout_log, '[string2goal] lines: %s\n' % lines)
            for line in lines:
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % line)
                line = filter(None, line.split(' '))
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % line)
                abilities = [x for x in filter(None, line[0].split(','))]
                t = {}
                for x in abilities:
                    a = [y for y in x.split(':')]
                    t.update({a[0]:float(a[1])})
                abilities = t
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % abilities)
                estim_time = float(line[1])
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %f\n' % estim_time)
                senderId = line[2]
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % senderId)
                energy = float(line[3])
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % energy)
                iterations = int(float(line[4]))
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % iterations)
                tID = int(float(line[5]))
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % tID)
                tName = line[6]
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % tName)
                endLoc = [float(x) for x in filter(None, line[7].split(','))]
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % endLoc)
                planId = line[8]
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % planId)
                equipment = [filter(None, x.split(',')) for x in filter(None, line[9].split('|'))]
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % equipment)
                startLoc = [float(x) for x in filter(None, line[10].split(','))]
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % startLoc)
                reward = int(float(line[11]))
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % reward)
                res = [x for x in filter(None, line[12].split(','))]
                t = {}
                for x in res:
                    a = [y for y in x.split(':')]
                    t.update({a[0]:float(a[1])})
                res = t
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % res)
                noAgents = int(line[13])
                # log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % noAgents)
                simulation_finish = float(line[14])
                log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % noAgents)
                ac_snd = [int(x) for x in filter(None, line[15].split(','))]

                plan.append({'senderID': senderId, 'planID': planId, 'id': tID, 'iterations': iterations, 'energy': energy,
                             'reward': reward, 'name': tName, 'startLoc': startLoc, 'endLoc': endLoc, 'noAgents': noAgents,
                             'equipment': equipment, 'abilities': abilities, 'resources': res, 'estim_time': estim_time, 'simulation_finish': simulation_finish, 'ac_senders': ac_snd})

            log.write_log_file(log.stdout_log, '[string2goal] plan content: %s\n' % plan)

            return plan
        except:
            log.write_log_file(log.stdout_log, "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))
    '''
    def willing2ask_fuzzy(self, inputs):
        # Define some parameters
        hmin = 400
        hmax = 4500
        hdiff = 10

        unitmin = 0
        unitmax = 1
        unitdiff = 0.1

        # Define antecedents (inputs): holds variables and membership functions
        # Health represents an aggregation of the values for battery, sensor, actuator and motor condition
        health = ctrl.Antecedent(np.arange(hmin, hmax, hdiff), 'health')

        # Best known agent to ask, in which helpfulness and success rate are combined beforehand, using a dot product
        best_agent = ctrl.Antecedent(np.arange(unitmin, unitmax, unitdiff), 'best_agent')

        # The environment represents a combined value of the danger associated with physical obstacles, and the general culture of the population
        # as in the case of the best known agent, these can be combined using a dot product
        environment = ctrl.Antecedent(np.arange(unitmin, unitmax, unitdiff), 'environment')

        # Agent abilities and resources needed in the scope of one task could also be combined in order to be represented by one fuzzy input
        abil_res = ctrl.Antecedent(np.arange(unitmin, unitmax, unitdiff), 'abil_res')
        abil_res['some'] = fuzz.trapmf(abil_res.universe, [0.0, 0.0, 0.4, 0.4])
        abil_res['all_&optional'] = fuzz.trapmf(abil_res.universe, [0.6, 0.6, 1.0, 1.0])
        # abil_res.view()
        # The agent's own progress wrt to tasks, or plans in general could also serve as a trigger to interact or not
        own_progress = ctrl.Antecedent(np.arange(unitmin, unitmax, unitdiff), 'own_progress')

        # Fuzzy output, the willingness to ask for help
        willingness = ctrl.Consequent(np.arange(unitmin, unitmax, unitdiff), 'willingness')

        # Auto membership function population
        health.automf(3)
        best_agent.automf(3)
        environment.automf(3)
        own_progress.automf(3)
        willingness.automf(3)

        # health.view()
        # willingness.view()

        # Define rules
        rules = []

        ## either poor health or only some of abilities and resources are enough to have high willingness to ask for help
        rules.append(ctrl.Rule(health['poor'] | abil_res['some'] | own_progress['poor'], willingness['good']))
        rules.append(ctrl.Rule((health['good'] | health['average']) & abil_res['all_&optional'] & (
        own_progress['good'] | own_progress['average']), willingness['poor']))
        # rules.append(ctrl.Rule(best_agent['good'] & health['average'] & abil_res['all_&optional'], willingness['average']))
        # rules.append(ctrl.Rule(best_agent['poor'] & health['average'] & abil_res['all_&optional'], willingness['poor']))

        ## View rules graphically
        # rule1.view()

        # inputs = [4400, 0.7, 0.3, 0.5]

        interact_ctrl = ctrl.ControlSystem(rules)
        interact = ctrl.ControlSystemSimulation(interact_ctrl)
        interact.input['health'] = inputs[0]
        # interact.input['best_agent'] = inputs[1]
        interact.input['abil_res'] = inputs[2]
        interact.input['own_progress'] = inputs[3]

        interact.compute()

        print interact.output['willingness']
        test = random.random()
        print test
        # The function will return depend either true or false, either ask or don't ask for help
        if test < interact.output['willingness']:
            return True
        else:
            return False
    '''
    # Simple models for delta and gamma
    def classic_delta(self, tasks_dropped, tasks_attempted):

        old = self.drop_rate
        if not tasks_attempted == 0:
            self.drop_rate = 1.0 * tasks_dropped/tasks_attempted

        if self.drop_rate < self.LOW:
            self.delta += 0.01
        elif self.drop_rate > self.HIGH:
            self.delta -= 0.01
        else:
            if (self.drop_rate - old) > 0.01:
                self.delta -= 0.01
            elif (self.drop_rate - old) < - 0.01:
                self.delta += 0.01

        if self.delta > 1.0:
            self.delta = 1.0
        elif self.delta < 0.0:
            self.delta = 0.0

        if random.random() <= self.delta:
            return True, self.delta, self.drop_rate
        else:
            return False, self.delta, self.drop_rate

    def classic_gamma(self, tasks_dropped, tasks_attempted):

        old = self.drop_rate
        if not tasks_attempted == 0:
            self.drop_rate = 1.0 * tasks_dropped/tasks_attempted

        if self.drop_rate < self.LOW:
            self.gamma -= 0.01
        elif self.drop_rate > self.HIGH:
            self.gamma += 0.01
        else:
            if (self.drop_rate - old) > 0.01:
                self.gamma += 0.01
            elif (self.drop_rate - old) < - 0.01:
                self.gamma -= 0.01

        if self.gamma > 1.0:
            self.gamma = 1.0
        elif self.gamma < 0.0:
            self.gamma = 0.0

        if random.random() <= self.gamma:
            return True, self.gamma, self.drop_rate
        else:
            return False, self.gamma, self.drop_rate

    # Willingness to give help

    def delta5(self, log, energy_diff, abil, equip, knowled, tools, env_risk, ag_risk, performance, dif_task_tradeoff,  culture, aID):
        try:
            self.delta = 0
            if energy_diff < 0:
                f1 = -1
            else:
                f1 = energy_diff
            msg = "energy: %f, f1: %f\n" % (energy_diff,f1)
            log.write_log_file(log.stdout_log, msg)
            if abil == 0:
                f2 = -1
            else:
                f2 = abil
            msg = "abil: %f, f2: %f\n" % (abil, f2)
            log.write_log_file(log.stdout_log, msg)
            if equip == 0:
                f3 = -1
            else:
                f3 = equip
            msg = "equip: %f, f3: %f\n" % (equip, f3)
            log.write_log_file(log.stdout_log, msg)
            if knowled == 0:
                f4 = -1
            else:
                f4 = knowled
            msg = "knowled: %f, f4: %f\n" % (knowled, f4)
            log.write_log_file(log.stdout_log, msg)
            if tools == 0:
                f5 = -1
            else:
                f5 = tools
            msg = "tools: %f, f4: %f\n" % (tools, f5)
            log.write_log_file(log.stdout_log, msg)
            f6 = performance-self.LOW
            f7 = dif_task_tradeoff-self.LOW
            f8 = self.LOW-env_risk
            f9 = self.LOW-ag_risk[0]
            self.delta = self.willingness[1] + (f1+f2+f3+f4+f5+f6+f7+f8+f9)/float(9)
            msg = "mu: %f, f6: %f\n" % (performance, f6)
            msg += "trade: %f, f7: %f\n" % (dif_task_tradeoff, f7)
            msg += "env: %f, f8: %f\n" % (env_risk, f8)
            msg += "arisk: %f, f9: %f\n" % (ag_risk[0], f9)
            msg += "delta: %f, delta0: %f\n" % (self.delta, self.willingness[1])
            log.write_log_file(log.stdout_log, msg)
            self.delta_in_time.append([self.delta, time.strftime("%H:%M:%S", time.gmtime(time.time()))])
            if self.delta > 1.0:
                self.delta = 1.0
            elif self.delta < 0.0:
                self.delta = 0.0

            if random.random() <= self.delta:
                return True, self.delta
            else:
                return False, self.delta
        except:
            msg = "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno)
            log.write_log_file(log.stdout_log, msg)

    def gamma3(self, log, energy_diff, abil, equip, knowled, tools, env_risk, ag_risk, performance, dif_task_progress, culture, aID):
        try:
            self.gamma = 0
            if energy_diff > 0:
                self.gamma = 1.0
                msg = "energy: %f" % (energy_diff)
                self.gamma_in_time.append([self.gamma,time.strftime("%H:%M:%S", time.gmtime(time.time()))])
                log.write_log_file(log.stdout_log, msg)
                return True, self.gamma
            else:
                f1 = energy_diff
                msg = "energy: %f, f1: %f" % (energy_diff, f1)
                log.write_log_file(log.stdout_log, msg)
                if abil == 0:
                    self.gamma = 1.0
                    msg = "abil: %f" % (abil)
                    self.gamma_in_time.append([self.gamma,time.strftime("%H:%M:%S", time.gmtime(time.time()))])
                    log.write_log_file(log.stdout_log, msg)
                    return True, self.gamma
                else:
                    f2 = -abil
                    msg = "abil: %f, f2: %f" % (abil, f2)
                    log.write_log_file(log.stdout_log, msg)
                    if equip == 0:
                        self.gamma = 1.0
                        msg = "equip: %f" % (equip)
                        self.gamma_in_time.append([self.gamma,time.strftime("%H:%M:%S", time.gmtime(time.time()))])
                        log.write_log_file(log.stdout_log, msg)
                        return True, self.gamma
                    else:
                        f3 = -equip
                        msg = "equip: %f, f3: %f" % (equip, f3)
                        log.write_log_file(log.stdout_log, msg)
                        if knowled == 0:
                            self.gamma = 1.0
                            msg = "knowled: %f" % (knowled)
                            self.gamma_in_time.append([self.gamma,time.strftime("%H:%M:%S", time.gmtime(time.time()))])
                            log.write_log_file(log.stdout_log, msg)
                            return True, self.gamma
                        else:
                            f4 = -knowled
                            msg = "knowled: %f, f4: %f" % (knowled, f4)
                            log.write_log_file(log.stdout_log, msg)
                            if tools == 0:
                                self.gamma = 1.0
                                msg = "tools: %f" % (tools)
                                self.gamma_in_time.append([self.gamma,time.strftime("%H:%M:%S", time.gmtime(time.time()))])
                                log.write_log_file(log.stdout_log, msg)
                                return True, self.gamma
                            else:
                                f5 = -tools
                                msg = "tools: %f, f5: %f" % (tools, f5)
                                log.write_log_file(log.stdout_log, msg)
                                #pdb.set_trace()
                                f6 = self.LOW-performance
                                f7 = self.LOW-dif_task_progress
                                f8 = env_risk-self.LOW
                                f9 = self.LOW-ag_risk
                                self.gamma = self.willingness[0] + (f1+f2+f3+f4+f5+f6+f7+f8+f9)/float(9)

                                msg = "low: %f, mu: %f, f6: %f\n" % (self.LOW, performance, f6)
                                msg += "progress: %f, f7: %f\n" % (dif_task_progress, f7)
                                msg += "env: %f, f8: %f\n" % (env_risk, f8)
                                msg += "arisk: %f, f9: %f\n" % (ag_risk, f9)
                                msg += "gamma: %f, gammma0: %f\n" % (self.gamma, self.willingness[0])
                                log.write_log_file(log.stdout_log, msg)
                                self.gamma_in_time.append([self.gamma,time.strftime("%H:%M:%S", time.gmtime(time.time()))])
                                if self.gamma > 1.0:
                                    self.gamma = 1.0
                                elif self.gamma < 0.0:
                                    self.gamma = 0.0

                                if random.random() <= self.gamma:
                                    return True, self.gamma
                                else:
                                    return False, self.gamma
        except:
            msg = "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno)
            log.write_log_file(log.stdout_log, msg)

    def deltaD(self, energy_diff, abil, equip, knowled, tools, env_risk, ag_risk, performance, dif_task_tradeoff, _tradeoff, culture, aID):
        try:
            self.delta = 0
            msg = '\ndeltaD: delta %f\n' % self.delta
            msg += 'energydiff: %f\n' % energy_diff
            rospy.loginfo(msg)

            self.delta += 1 - self.battery_min/float(energy_diff)
            msg += 'delta: %f, percentage: %f\n' % (self.delta, self.battery_min/float(energy_diff))
            rospy.loginfo(msg)
            msg = '\n ariks: %s\n' % (str(self.arisk))
            rospy.loginfo(msg)
            if abil == 0:
                self.delta += -1
            else:
                self.delta += abil # we assume accuracy is one
            if equip == 0:
                self.delta += -1
            else:
                self.delta += equip
            if knowled == 0:
                self.delta += -1
            else:
                self.delta += knowled
            if tools == 0:
                self.delta += -1
            else:
                self.delta += tools

            msg += 'delta: %f\n' % self.delta
            rospy.loginfo(msg)

            if env_risk < self.LOW:
                self.delta += 1 - env_risk
            elif env_risk > self.HIGH:
                self.delta -= env_risk
            elif abs(env_risk - self.env_risk) > self.considerable_change:
                if not self.env_risk == 0:
                    self.delta -= (env_risk - self.env_risk)/float(env_risk + self.env_risk)
                else:
                    self.delta -= env_risk - self.env_risk

            if not self.env_risk == 0:
                msg += 'env risk: %f, delta: %f, percent: %f\n' % (env_risk, self.delta, (env_risk - self.env_risk)/float(env_risk + self.env_risk))
            else:
                msg += 'env risk: %f, delta: %f, percent: %f\n' % (env_risk, self.delta, env_risk - self.env_risk)

            rospy.loginfo(msg)

            if aID in self.arisk:
                if ag_risk[0] < self.LOW:
                    self.delta += 1 - ag_risk[0]
                elif ag_risk[0] > self.HIGH:
                    self.delta -= ag_risk[0]
                elif ag_risk[0] - self.arisk[aID] > self.considerable_change:
                    if not self.arisk[aID] == 0:
                        self.delta -= (ag_risk[0] - self.arisk[aID])/float(ag_risk[0] + self.arisk[aID])
                    else:
                        self.delta -= ag_risk[0] - self.arisk[aID]
            else:
                self.arisk.update({aID:0})
                if ag_risk[0] < self.LOW:
                    self.delta += 1 - ag_risk[0]
                elif ag_risk[0] > self.HIGH:
                    self.delta -= ag_risk[0]
                elif ag_risk[0] - self.arisk[aID] > self.considerable_change:
                    if not self.arisk[aID] == 0:
                        self.delta -= (ag_risk[0] - self.arisk[aID])/float(ag_risk[0] + self.arisk[aID])
                    else:
                        self.delta -= ag_risk[0] - self.arisk[aID]
            msg = "\n arisk: %f, dict: %s" % (ag_risk[0], str(self.arisk[aID]))
            rospy.loginfo(msg)
            if not self.arisk[aID] == 0:
                msg += 'ag risk: %f, delta: %f, percent: %f\n' % (ag_risk[0], self.delta, (ag_risk[0] - self.arisk[aID])/float(ag_risk[0] + self.arisk[aID]))
            else:
                msg += 'ag risk: %f, delta: %f, percent: %f\n' % (ag_risk[0], self.delta, ag_risk[0] - self.arisk[aID])

            rospy.loginfo(msg)

            if performance < self.LOW:
                self.delta -= 1 - performance
            elif performance > self.HIGH:
                self.delta += performance
            elif abs(performance - self.performance) > self.considerable_change:
                if not self.performance == 0:
                    self.delta += (performance - self.performance)/float(performance + self.performance)
                else:
                    self.delta += performance - self.performance

            if not self.performance == 0:
                msg += 'performance: %f, delta: %f, percent: %f\n' % (performance, self.delta, (performance - self.performance)/float(performance + self.performance))
            else:
                msg += 'performance: %f, delta: %f, percent: %f\n' % (performance, self.delta, performance - self.performance)

            rospy.loginfo(msg)

            if dif_task_tradeoff < self.LOW:
                self.delta -= 1 - dif_task_tradeoff
            elif dif_task_tradeoff > self.HIGH:
                self.delta += dif_task_tradeoff
            if abs(dif_task_tradeoff) > self.considerable_change:
                self.delta += dif_task_tradeoff

            if not _tradeoff == 0:
                msg += 'tradeoff: %f, delta: %f, percent: %f\n' % (dif_task_tradeoff, self.delta, (dif_task_tradeoff)/float(_tradeoff))
            else:
                msg += 'tradeoff: %f, delta: %f, percent: %f\n' % (dif_task_tradeoff, self.delta, dif_task_tradeoff)

            self.env_risk = env_risk
            self.performance = performance
            self.arisk[aID] = ag_risk[0]

            self.delta = self.willingness[1] + self.delta/float(9)

            msg += "\n delta: %f" % self.delta
            rospy.loginfo(msg)

            if self.delta > 1.0:
                self.delta = 1.0
            elif self.delta < 0.0:
                self.delta = 0.0

            if random.random() <= self.delta:
                return True, self.delta
            else:
                return False, self.delta

        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))

    def deltaD_no_chain(self, energy_diff, abil, equip, knowled, tools, env_risk, ag_risk, performance, dif_task_tradeoff, _tradeoff, culture, aID):
        try:
            self.delta = 0
            msg = '\ndeltaD: delta %f\n' % self.delta
            msg += 'energydiff: %f\n' % energy_diff
            rospy.loginfo(msg)

            if energy_diff < self.battery_min:
                self.delta = 0.0
                return False, self.delta
            else:
                self.delta += 1 - self.battery_min/float(energy_diff)
            msg += 'delta: %f, percentage: %f\n' % (self.delta, self.battery_min/float(energy_diff))
            rospy.loginfo(msg)
            msg = '\n ariks: %s\n' % (str(self.arisk))
            rospy.loginfo(msg)
            if abil == 0:
                self.delta = 0.0
                return False, self.delta
            else:
                self.delta += abil # we assume accuracy is one
            if equip == 0:
                self.delta = 0.0
                return False, self.delta
            else:
                self.delta += equip
            if knowled == 0:
                self.delta = 0.0
                return False, self.delta
            else:
                self.delta += knowled
            if tools == 0:
                self.delta = 0.0
                return False, self.delta
            else:
                self.delta += tools

            msg += 'delta: %f\n' % self.delta
            rospy.loginfo(msg)

            if env_risk < self.LOW:
                self.delta += 1 - env_risk
            elif env_risk > self.HIGH:
                self.delta -= env_risk
            elif abs(env_risk - self.env_risk) > self.considerable_change:
                if not self.env_risk == 0:
                    self.delta -= (env_risk - self.env_risk)/float(env_risk + self.env_risk)
                else:
                    self.delta -= env_risk - self.env_risk

            if not self.env_risk == 0:
                msg += 'env risk: %f, delta: %f, percent: %f\n' % (env_risk, self.delta, (env_risk - self.env_risk)/float(env_risk + self.env_risk))
            else:
                msg += 'env risk: %f, delta: %f, percent: %f\n' % (env_risk, self.delta, env_risk - self.env_risk)

            rospy.loginfo(msg)

            if aID in self.arisk:
                if ag_risk[0] < self.LOW:
                    self.delta += 1 - ag_risk[0]
                elif ag_risk[0] > self.HIGH:
                    self.delta -= ag_risk[0]
                elif ag_risk[0] - self.arisk[aID] > self.considerable_change:
                    if not self.arisk[aID] == 0:
                        self.delta -= (ag_risk[0] - self.arisk[aID])/float(ag_risk[0] + self.arisk[aID])
                    else:
                        self.delta -= ag_risk[0] - self.arisk[aID]
            else:
                self.arisk.update({aID:0})
                if ag_risk[0] < self.LOW:
                    self.delta += 1 - ag_risk[0]
                elif ag_risk[0] > self.HIGH:
                    self.delta -= ag_risk[0]
                elif ag_risk[0] - self.arisk[aID] > self.considerable_change:
                    if not self.arisk[aID] == 0:
                        self.delta -= (ag_risk[0] - self.arisk[aID])/float(ag_risk[0] + self.arisk[aID])
                    else:
                        self.delta -= ag_risk[0] - self.arisk[aID]
            msg = "\n arisk: %f, dict: %s" % (ag_risk[0], str(self.arisk[aID]))
            rospy.loginfo(msg)
            if not self.arisk[aID] == 0:
                msg += 'ag risk: %f, delta: %f, percent: %f\n' % (ag_risk[0], self.delta, (ag_risk[0] - self.arisk[aID])/float(ag_risk[0] + self.arisk[aID]))
            else:
                msg += 'ag risk: %f, delta: %f, percent: %f\n' % (ag_risk[0], self.delta, ag_risk[0] - self.arisk[aID])

            rospy.loginfo(msg)

            if performance < self.LOW:
                self.delta -= 1 - performance
            elif performance > self.HIGH:
                self.delta += performance
            elif abs(performance - self.performance) > self.considerable_change:
                if not self.performance == 0:
                    self.delta += (performance - self.performance)/float(performance + self.performance)
                else:
                    self.delta += performance - self.performance

            if not self.performance == 0:
                msg += 'performance: %f, delta: %f, percent: %f\n' % (performance, self.delta, (performance - self.performance)/float(performance + self.performance))
            else:
                msg += 'performance: %f, delta: %f, percent: %f\n' % (performance, self.delta, performance - self.performance)

            rospy.loginfo(msg)

            if dif_task_tradeoff < self.LOW:
                self.delta -= 1 - dif_task_tradeoff
            elif dif_task_tradeoff > self.HIGH:
                self.delta += dif_task_tradeoff
            if abs(dif_task_tradeoff) > self.considerable_change:
                self.delta += dif_task_tradeoff

            if not _tradeoff == 0:
                msg += 'tradeoff: %f, delta: %f, percent: %f\n' % (dif_task_tradeoff, self.delta, (dif_task_tradeoff)/float(_tradeoff))
            else:
                msg += 'tradeoff: %f, delta: %f, percent: %f\n' % (dif_task_tradeoff, self.delta, dif_task_tradeoff)

            self.env_risk = env_risk
            self.performance = performance
            self.arisk[aID] = ag_risk[0]

            self.delta = self.willingness[1] + self.delta/float(9)

            msg += "\n delta: %f" % self.delta
            rospy.loginfo(msg)

            if self.delta > 1.0:
                self.delta = 1.0
            elif self.delta < 0.0:
                self.delta = 0.0

            if random.random() <= self.delta:
                return True, self.delta
            else:
                return False, self.delta

        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))

    def gammaG(self, energy_diff, abil, equip, knowled, tools, env_risk, ag_risk, performance, dif_task_progress, _progress, culture, aID):

        try:
            self.gamma = 0

            msg = '\ngammaG: gamma %f\n' % self.gamma
            msg += 'energydiff: %f\n' % energy_diff
            if energy_diff < self.battery_min:
                self.gamma = 1.0
                return True, self.gamma
            else:
                self.gamma -= 1 - self.battery_min/float(energy_diff)
                msg += 'gamma: %f, percentage: %f\n' % (self.gamma, self.battery_min/float(energy_diff))

                if abil == 0:
                    self.gamma = 1.0
                    return True, self.gamma
                else:
                    self.gamma -= abil

                if equip == 0:
                    self.gamma = 1.0
                    return True, self.gamma
                else:
                    self.gamma -= equip
                if knowled == 0:
                    self.gamma = 1.0
                    return True, self.gamma
                else:
                    self.gamma -= knowled
                if tools == 0:
                    self.gamma = 1.0
                    return True, self.gamma
                else:
                    self.gamma -= tools

                msg += 'gamma: %f\n' % self.gamma

                if env_risk < self.LOW:
                    self.gamma -= 1 - env_risk
                elif env_risk > self.HIGH:
                    self.gamma += env_risk
                elif abs(env_risk - self.env_risk) > self.considerable_change:
                    if not self.env_risk == 0:
                        self.gamma += (env_risk - self.env_risk)/float(env_risk + self.env_risk)
                    else:
                        self.gamma += env_risk - self.env_risk

                if not self.env_risk == 0:
                    msg += 'env risk: %f, gamma: %f, percent: %f\n' % (env_risk, self.gamma, (env_risk - self.env_risk)/float(env_risk + self.env_risk))
                else:
                    msg += 'env risk: %f, gamma: %f, percent: %f\n' % (env_risk, self.gamma, abs(env_risk - self.env_risk))

                if aID in self.arisk:
                    if ag_risk < self.LOW:
                        self.gamma += 1 - ag_risk
                    elif ag_risk > self.HIGH:
                        self.gamma -= ag_risk
                    elif ag_risk - self.arisk[aID] > self.considerable_change:
                        if not self.arisk[aID] == 0:
                            self.gamma -= (ag_risk - self.arisk[aID])/float(ag_risk + self.arisk[aID])
                        else:
                            self.gamma -= ag_risk - self.arisk[aID]
                else:
                    self.arisk.update({aID:0})
                    if ag_risk < self.LOW:
                        self.gamma += 1 - ag_risk
                    elif ag_risk > self.HIGH:
                        self.gamma -= ag_risk
                    elif ag_risk - self.arisk[aID] > self.considerable_change:
                        if not self.arisk[aID] == 0:
                            self.gamma -= (ag_risk - self.arisk[aID])/float(ag_risk + self.arisk[aID])
                        else:
                            self.gamma -= ag_risk - self.arisk[aID]

                if not self.arisk[aID] == 0:
                    msg += 'ag risk: %f, gamma: %f, percent: %f\n' % (ag_risk, self.gamma, (ag_risk - self.arisk[aID])/float(self.arisk[aID]))
                else:
                    msg += 'ag risk: %f, gamma: %f, percent: %f\n' % (ag_risk, self.gamma, ag_risk - self.arisk[aID])

                if performance < self.LOW:
                    self.gamma += 1 - performance
                elif performance > self.HIGH:
                    self.gamma -= performance
                elif abs(performance - self.performance) > self.considerable_change:
                    if not self.performance == 0:
                        self.gamma -= (performance - self.performance)/float(performance + self.performance)
                    else:
                        self.gamma -= performance - self.performance

                if not self.performance == 0:
                    msg += 'performance: %f, gamma: %f, percent: %f\n' % (performance, self.gamma, (performance - self.performance)/float(self.performance))
                else:
                    msg += 'performance: %f, gamma: %f, percent: %f\n' % (performance, self.gamma, performance - self.performance)

                #pdb.set_trace()

                if dif_task_progress < self.LOW:
                    self.gamma += 1 - dif_task_progress
                elif dif_task_progress > self.HIGH:
                    self.gamma -= dif_task_progress
                elif abs(dif_task_progress) > self.considerable_change:
                    self.gamma -= dif_task_progress

                msg += 'progress: %f, gamma: %f, percent: %f\n' % (dif_task_progress, self.gamma, dif_task_progress)

            rospy.loginfo(msg)

            self.gamma = self.willingness[0] + self.gamma/float(9)
            msg += "\n gamma: %f" % self.gamma
            rospy.loginfo(msg)
            if self.gamma > 1.0:
                self.gamma = 1.0
            elif self.gamma < 0.0:
                self.gamma = 0.0

            self.env_risk = env_risk
            self.performance = performance
            self.arisk[aID] = ag_risk

            if random.random() <= self.gamma:
                return True, self.gamma
            else:
                return False, self.gamma
        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line nr: " + str(sys.exc_info()[2].tb_lineno))

    def b_delta(self, energy_diff, abil, equip, knowled, tools, env_risk, ag_risk, performance, dif_task_tradeoff, culture, ag_id):

        if self.memory == 0:
            self.delta = self.willingness[1]
        if energy_diff < self.battery_min:
            self.delta = 0.0
            return False, self.delta
        else:
            self.delta += self.step
            if abil == 0:
                self.delta -= self.step
            else:
                self.delta += self.step
            if equip == 0:
                self.delta -= self.step
            else:
                self.delta += self.step
            if knowled == 0:
                self.delta -= self.step
            else:
                self.delta += self.step
            if tools == 0:
                self.delta -= self.step
            else:
                self.delta += self.step

            if env_risk < self.LOW:
                self.delta += self.step
            elif env_risk > self.HIGH:
                self.delta -= self.step
            else:
                if abs(env_risk - self.env_risk) > self.considerable_change:
                    self.delta -= np.sign(env_risk - self.env_risk) * self.step

            if ag_risk >= 0.5:
                self.delta -= self.step
            else:
                self.delta += self.step

            if performance < self.LOW:
                self.delta -= self.step
            elif performance > self.HIGH:
                self.delta += self.step
            else:
                if abs(performance - self.performance) > self.considerable_change:
                    self.delta += np.sign(performance - self.performance) * self.step

            if abs(dif_task_tradeoff) > self.considerable_change:
                self.delta += np.sign(dif_task_tradeoff) * self.step

        self.env_risk = env_risk
        self.performance = performance

        '''
        if not self.ID == 1:
            if ag_risk >= 0.5 and culture <= 0.5:
                self.delta = 0.1
                for x in self.ten_shots:
                    if ag_id == x[0]:
                        x[1].append(ag_risk)
            elif (ag_risk < 0.5 and culture > 0.5) or (ag_risk < 0.5 and culture <= 0.5):
                self.delta += 5 * self.step
            elif ag_risk >= 0.5 and culture > 0.5:
                for x in self.ten_shots:
                    if ag_id == x[0]:
                        if len(x[1]) < 3:
                            x[1].append(ag_risk)
                            self.delta -= self.step
                        else:
                            self.delta = 0.1
        '''

        if self.delta > 1.0:
            self.delta = 1.0
        elif self.delta < 0.0:
            self.delta = 0.0

        if random.random() <= self.delta:
            return True, self.delta
        else:
            return False, self.delta

    def b_delta_2(self, energy_diff, abil, equip, knowled, tools, env_risk, ag_risk, performance, dif_task_tradeoff):

        if self.memory == 0:
            self.delta = self.willingness[1]
        if energy_diff < self.battery_min:
            self.delta = 0.0
            return False, self.delta
        else:
            self.delta += self.step
            if abil == 0:
                return False, self.delta
            else:
                self.delta += self.step
            if equip == 0:
                return False, self.delta
            else:
                self.delta += self.step
            if knowled == 0:
                return False, self.delta
            else:
                self.delta += self.step
            if tools == 0:
                return False, self.delta
            else:
                self.delta += self.step

            if env_risk < self.LOW:
                self.delta += self.step
            elif env_risk > self.HIGH:
                self.delta -= self.step
            else:
                if abs(env_risk - self.env_risk) > self.considerable_change:
                    self.delta -= np.sign(env_risk - self.env_risk) * self.step

            if ag_risk >= 0.5:
                self.delta -= self.step
            else:
                self.delta += self.step

            if performance < self.LOW:
                self.delta -= self.step
            elif performance > self.HIGH:
                self.delta += self.step
            else:
                if abs(performance - self.performance) > self.considerable_change:
                    self.delta += np.sign(performance - self.performance) * self.step

            if abs(dif_task_tradeoff) > self.considerable_change:
                self.delta += np.sign(dif_task_tradeoff) * self.step

        self.env_risk = env_risk
        self.performance = performance

        if self.delta > 1.0:
            self.delta = 1.0
        elif self.delta < 0.0:
            self.delta = 0.0

        if random.random() <= self.delta:
            return True, self.delta
        else:
            return False, self.delta

    def b_gamma(self, energy_diff, abil, equip, knowled, tools, env_risk, ag_risk, performance, dif_task_progress):

        if self.memory == 0:
            self.gamma = self.willingness[0]
        if energy_diff < self.battery_min:
            self.gamma = 1.0
            return True, self.gamma
        else:
            self.gamma -= self.step
            if abil == 0:
                self.gamma = 1.0
                return True, self.gamma
            else:
                self.gamma -= self.step
            if equip == 0:
                self.gamma = 1.0
                return True, self.gamma
            else:
                self.gamma -= self.step
            if knowled == 0:
                self.gamma = 1.0
                return True, self.gamma
            else:
                self.gamma -= self.step
            if tools == 0:
                self.gamma = 1.0
                return True, self.gamma
            else:
                self.gamma -= self.step

            if env_risk < self.LOW:
                self.gamma -= self.step
            elif env_risk > self.HIGH:
                self.gamma += self.step
            else:
                if abs(env_risk - self.env_risk) > self.considerable_change:
                    self.gamma += np.sign(env_risk - self.env_risk) * self.step

            if ag_risk >= 0.5:
                self.gamma -= self.step
            else:
                self.gamma += self.step

            if performance < self.LOW:
                self.gamma += self.step
            elif performance > self.HIGH:
                self.gamma -= self.step
            else:
                if abs(performance - self.performance) > self.considerable_change:
                    self.gamma -= np.sign(performance - self.performance) * self.step

            if abs(dif_task_progress) > self.considerable_change:
                self.gamma -= np.sign(dif_task_progress) * self.step

        if self.gamma > 1.0:
            self.gamma = 1.0
        elif self.gamma < 0.0:
            self.gamma = 0.0

        if random.random() <= self.gamma:
            return True, self.gamma
        else:
            return False, self.gamma
