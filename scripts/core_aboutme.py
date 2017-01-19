#!/usr/bin/env python
import sys
import random
import mylogging
from gitagent.msg import *
import time
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import pdb


class Core:
    def __init__(self, willingness, ID, battery, sensors, actuators, motors):
        # willingness - [theta, delta]
        self.willingness = willingness
        # Willingness to ask for assistance
        self.ask = False

        # Willingness to give assistance
        self.give = False

        # Thresholds -- percentage of affordance
        self.LOW = 0.3
        self.HIGH = 0.7

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
        self.battery = battery

        # 3 arrays which keep the states for sensors, actuators, motors
        self.sensors = sum(sensors)
        self.actuators = sum(actuators)
        self.motors = sum(motors)
        self.sensmot = sum([self.sensors, self.actuators, self.motors])

        # This is the minimum value for the battery levels in which it could be
        # considered that the agent works properly
        self.battery_min = 300
        self.sensmot_min = 300
        self.self_esteem = 1.0

        # This could be an array, in which each element represents health over some dimension
        self.check_health()

        print self.willingness
        print self.state
        print self.battery

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

    def ask_5help(self, health, abilities, resources, self_esteem, task_urgency, task_importance, culture,
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
            self.state = 4

    def best_candidate(self, known_people, task, log):
        #pdb.set_trace()
        # Assume that agent's can do the tasks
        #print known_people
        success_chance = -1
        agent_id = -1
        agent_idx = -1

        # Find in known people the subset of agents that can do the task
        subset = []
        if known_people:
            #print 'known people not empty'
            #print 'task id type ' + str(type(task['id']))
            for x in known_people:
                print  x[2]
                if task['id'] in x[2]:
                    subset.append(x)
            print subset
            if subset:
                if random.random() < 0.4:
                    # Choose an agent randomly
                    #print 'random'
                    agent_idx = random.randint(0, len(subset) - 1)
                    print subset[agent_idx][0]
                    success_chance = subset[agent_idx][1]
                    print success_chance
                    log.write_log_file(log.stdout_log, 'Randomly chosen: %d\n' % subset[agent_idx][0])
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
                log.write_log_file(log.stdout_log, 'No one to ask for this task\n')
                #print 'no one for this task'
        else:
            #print 'no one'
            log.write_log_file(log.stdout_log, 'No one to ask \n')

        return success_chance, agent_id, agent_idx

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
            for x in raw_content:
                content = content + str(x[0]) + '|'
        return content

    def goal2string(self, goal):
        # pdb.set_trace()
        abil = ''
        for x in goal['abilities']:
            abil = abil + str(x) + ','
        eloc = str(goal['endLoc'][0]) + ',' + str(goal['endLoc'][1])
        sloc = str(goal['startLoc'][0]) + ',' + str(goal['startLoc'][1])
        res = ''
        for x in goal['resources']:
            res = res + str(x) + ','
        equip = ''
        print goal['equipment']
        for x in goal['equipment']:
            for y in x:
                equip = equip + str(y) + ','
            equip = equip + '|'
        # Basically it is being assumed that only one goal passes through -- change this to send plans
        goal = abil + ' ' + str(goal['estim_time']) + ' ' + str(goal['senderID']) + ' ' + str(
            goal['energy']) + ' ' + str(goal['iterations']) + ' ' + str(goal['id']) + ' ' + goal[
                   'name'] + ' ' + eloc + ' ' + str(goal['planID']) + ' ' + equip + ' ' + sloc + ' ' + str(
            goal['reward']) + ' ' + res + ' ' + str(goal['noAgents']) + '\n'
        return goal

    def string2goal(self, line, log):
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

        return {'senderID': senderId, 'planID': planId, 'id': tID, 'iterations': iterations, 'energy': energy,
                'reward': reward, 'name': tName, 'startLoc': startLoc, 'endLoc': endLoc, 'noAgents': noAgents,
                'equipment': equipment, 'abilities': abilities, 'resources': res, 'estim_time': estim_time}

    def string2goalPlan(self, lines, log):
        # halloumi, 15.8918374114 1 46 8 56 randomCrap 5,6 -8 pip,|pop,|pup,| 2,3 41 mozarella, 3
        plan = []
        lines = filter(None, lines.split('\n'))
        log.write_log_file(log.stdout_log, '[string2goal] lines: %s\n' % lines)
        for line in lines:
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % line)
            line = filter(None, line.split(' '))
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % line)
            abilities = [x for x in filter(None, line[0].split(','))]
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % abilities)
            estim_time = float(line[1])
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %f\n' % estim_time)
            senderId = line[2]
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % senderId)
            energy = int(line[3])
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % energy)
            iterations = int(line[4])
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % iterations)
            tID = int(line[5])
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % tID)
            tName = line[6]
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % tName)
            endLoc = [x for x in filter(None, line[7].split(','))]
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % endLoc)
            planId = line[8]
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % planId)
            equipment = [filter(None, x.split(',')) for x in filter(None, line[9].split('|'))]
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % equipment)
            startLoc = [x for x in filter(None, line[10].split(','))]
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % startLoc)
            reward = int(line[11])
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % reward)
            res = [x for x in filter(None, line[12].split(','))]
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %s\n' % res)
            noAgents = int(line[13])
            # log.write_log_file(log.stdout_log, '[string2goal] goal content: %d\n' % noAgents)

            plan.append({'senderID': senderId, 'planID': planId, 'id': tID, 'iterations': iterations, 'energy': energy,
                         'reward': reward, 'name': tName, 'startLoc': startLoc, 'endLoc': endLoc, 'noAgents': noAgents,
                         'equipment': equipment, 'abilities': abilities, 'resources': res, 'estim_time': estim_time})

        log.write_log_file(log.stdout_log, '[string2goal] plan content: %s\n' % plan)

        return plan

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
