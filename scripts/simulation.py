#!/usr/bin/env python
# Parent class of agent, implementing the core parts of the theoretical concept
# Framework v1.0
import sys
import random
import math
import time
import pdb


class Simulation0:
    def __init__(self):
        ## The attributes below serve as a timestamp for each function called ######
        # handle_serve, call_serve, callback_bc, wander, adapt, run_step, fsm
        self.handle = 0
        self.call = 0
        self.callback_bc = 0
        self.idle = 0
        self.interact = 0
        self.execute = 0
        self.fsm = 0
        self.regenerate = 0
        self.dead = 0
        self.hell = 0

        ##Default value for delay when request is issued
        self.additional_delay = [0.05, 0.1, 0.2]

        # Time taken by tasks of different difficulties, easy, medium, hard
        self.delay = [0.1, 0.5, 1.0]

        self.dep_prob = 0.2

        ##Values to be measured
        # First element contains requests produced by easy tasks, second by medium, third by difficult tasks
        self.requests = [0, 0, 0]

        # Plans received: easy, medium, difficult
        self.no_plans = [0, 0, 0]

        # Tasks executed: easy, medium, difficult
        self.no_tasks = [0, 0, 0]

        self.no_tasks_attempted = [0, 0, 0]
        self.no_tasks_completed = [0, 0, 0]

        self.no_tasks_depend_attempted = [0, 0, 0]
        self.no_tasks_depend_completed = [0, 0, 0]

        # Contains the time consumed by the fuzzy algorithm on each run
        self.fuzzy_time = []

        # Tasks executed: easy, medium, difficult
        self.exec_times = [0, 0, 0]

        # An error is considered the one in which the system returns no request when there is a required res/abil missing
        self.required_missing = 0
        self.required_missing_noreq = 0

        # Keep track of simulate task_urgency and importance
        self.task_give_urgency = []
        self.task_ask_urgency = []

        self.task_give_importance = []
        self.task_ask_importance = []

        # Stopping criterion - count how many jobs the agent is doing that came from the planner, when 150 is reached, simulation can end
        self.STOP = 150
        self.stopINC = 0
        # Generate tasks such that 50 of each difficulty are executed.
        # Follows the indexing self.requests
        self.generated_tasks = [0, 0, 0]

        # Values to record
        self.theta_esteem = []
        self.theta_tu = []
        self.theta_ti = []
        self.theta_culture = []
        self.theta_candidate = []
        self.theta_deps = []
        self.theta = []
        self.theta_health = []
        self.theta_bool = []
        self.exec_times_depend = []

        self.gamma_esteem = []
        self.gamma_tu = []
        self.gamma_ti = []
        self.gamma_culture = []
        self.gamma_candidate = []
        self.gamma_deps = []
        self.gamma = []
        self.gamma_health = []
        self.gamma_bool = []
        self.gamma_req_goodness = []

    # self.stdout_log = 'RESULT/pop_size.'+str(popSize) +'/prova.'+str(provaNr)+'/stdout_' + str(ID) + '_' + str(delta) +'_'+ str(depend_nr)
    # self.stdout_callback = 'RESULT/pop_size.'+str(popSize) +'/prova.'+str(provaNr)+'/stdout_callback' + str(ID) + '_' + str(delta) +'_'+ str(depend_nr)
    # self.stdout_handle = 'RESULT/pop_size.'+str(popSize) +'/prova.'+str(provaNr)+'/stdout_handle' + str(ID) + '_' + str(delta) +'_'+ str(depend_nr)

    def detect_difficulty(self, service):
        if len(service['abilities']) == 1:
            return 0
        elif len(service['abilities']) == 2:
            return 1
        elif len(service['abilities']) == 3:
            return 2
        else:
            return 3

    def sim_dependencies_fuzzy(self, service):
        # Each ability and resource adds to the probability of a dependency being raised -- considering abilities as required, and resources as optional for the sake of current implementation simplicity
        required = 0
        optional = 0
        req_missing = False

        for x in service['abilities']:
            if random.random() > self.dep_prob:
                required = required + 1

        for x in service['resources']:
            if random.random() > self.dep_prob:
                optional = optional + 1

        if required < len(service['abilities']):
            dependency_state = 0.3
            self.required_missing = self.required_missing + 1
            req_missing = True
        elif required == len(service['abilities']) and optional < len(service['resources']):
            dependency_state = 0.6
        elif required == len(service['abilities']) and optional == len(service['resources']):
            dependency_state = 1.0
        else:
            dependency_state = -10000

        return (dependency_state, req_missing)

    def sim_dependencies(self, service):
        # Each ability and resource adds to the probability of a dependency being raised -- considering abilities as required, and resources as optional for the sake of current implementation simplicity
        # Abilities are considered as required, whilst resources as optional -- this of course could be changed based on the
        # needs
        required = 0
        optional = 0
        req_missing = False

        for x in service['abilities']:
            if random.random() > self.dep_prob:
                required = required + 1

        for x in service['resources']:
            if random.random() > self.dep_prob:
                optional = optional + 1

        if required < len(service['abilities']):
            dependency_abil = 0.0
            self.required_missing = self.required_missing + 1
            req_missing = True
        else:
            dependency_abil = 1.0

        if optional < len(service['resources']):
            dependency_res = 0.6
        else:
            dependency_res = 1.0

        task_importance = random.random()
        task_urgency = random.random()
        culture = random.random()
        best_candidate = random.random()

        return dependency_abil, dependency_res, req_missing, task_importance, task_urgency, culture

    def read_agent_conf(self, filename):

        with open('/home/mfi01/catkin_ws/src/gitagent/scripts/' + filename) as f:
            lines = f.read().splitlines()

        battery = int(lines[0])
        vel = float(lines[1])
        sens = [x.split(',') for x in lines[2].split('|')]
        act = [x for x in lines[3].split(',')]
        mot = [x for x in lines[4].split(',')]
        sloc = [x for x in lines[5].split(',')]
        abil = [x for x in lines[6].split(',')]
        res = [x for x in lines[7].split(',')]
        serve = [x for x in lines[8].split(',')]
        knowl = [x for x in lines[9].split(',')]
        lang = [x for x in lines[10].split(',')]
        prots = [x for x in lines[11].split(',')]

        return {'battery': battery, 'velocity': vel, 'sensors': sens, 'actuators': act, 'motors': mot,
                'startLocation': sloc, 'abilities': abil, 'resources': res, 'services': serve, 'knowledge': knowl,
                'languages': lang, 'protocols': prots}

    def execute_task(self, task):
        pass

    def insert_delay(self):
        time.sleep(self.delay)

    # moves randomly
    def move(self, xypos):

        minimum = -10
        maximum = 10
        xupdate = random.uniform(minimum, maximum)
        yupdate = random.uniform(minimum, maximum)
        xypos[0] = xypos[0] + xupdate
        xypos[1] = xypos[1] + yupdate

        return xypos

    def inc_iterationstamps(self, iteration_stamp):
        iteration_stamp = iteration_stamp + 1
        return iteration_stamp

    def simulate_give_params(self):
        request_goodness = random.random()
        self.req_goodness.append(request_goodness)
        task_urgency = random.random()
        self.task_give_urgency.append(task_urgency)
        task_importance = random.random()
        self.task_give_importance.append(task_importance)

        return request_goodness, task_importance, task_urgency

    def simulate_ask_params(self):
        task_urgency = random.random()
        self.task_ask_urgency.append(task_urgency)
        task_importance = random.random()
        self.task_ask_importance.append(task_importance)

        return task_importance, task_urgency

    def get_tasks(self, filename):
        # Task Format ###########################################
        # id iter energy reward name startLocation endLocation noAgents equipment[[sensors],[actuators], [motors]] abilities resources estimated_time
        # pdb.set_trace()
        tasks = []
        with open('/home/mfi01/catkin_ws/src/gitagent/scripts/service_spec/' + filename) as f:
            lines = f.read().splitlines()

        for line in lines:
            line = line.split(' ')
            tID = int(line[0])
            iterations = int(line[1])
            energy = int(line[2])
            reward = int(line[3])
            tName = line[4]
            startLoc = [x for x in line[5].split(',')]
            endLoc = [x for x in line[6].split(',')]
            noAgents = int(line[7])
            equipment = [x.split(',') for x in line[8].split('|')]
            abilities = [x for x in line[9].split(',')]
            res = [x for x in line[10].split(',')]
            estim_time = float(line[11])
            tasks.append({'id': tID, 'iterations': iterations, 'energy': energy, 'reward': reward, 'name': tName,
                          'startLoc': startLoc, 'endLoc': endLoc, 'noAgents': noAgents, 'equipment': equipment,
                          'abilities': abilities, 'resources': res, 'estim_time': estim_time})
            print line

        return tasks, lines

    def string2dict(self, lines, planId, senderId):
        tasks = []
        for line in lines:
            line = line.split(' ')
            tID = int(line[0])
            iterations = int(line[1])
            energy = int(line[2])
            reward = int(line[3])
            tName = line[4]
            startLoc = [x for x in line[5].split(',')]
            endLoc = [x for x in line[6].split(',')]
            noAgents = int(line[7])
            equipment = [x.split(',') for x in line[8].split('|')]
            abilities = [x for x in line[9].split(',')]
            res = [x for x in line[10].split(',')]
            estim_time = float(line[11])
            tasks.append({'senderID': senderId, 'planID': planId, 'id': tID, 'iterations': iterations, 'energy': energy,
                          'reward': reward, 'name': tName, 'startLoc': startLoc, 'endLoc': endLoc, 'noAgents': noAgents,
                          'equipment': equipment, 'abilities': abilities, 'resources': res, 'estim_time': estim_time})
            print line

        return tasks

    # trick to emulate the selection of a couple of services the agent can provide
    def select_services(self, agent_id, depend_nr):
        # Anatomy of service
        # [id, iterations, energy, reward, [mandatory resources], [optional resources], permission, urgency, estimated_time, [known dependencies (no array for now, just one)]]
        try:  # try to do it with relative paths
            filename = '/home/mfi01/catkin_ws/src/gitagent/scripts/service_spec/services_list_' + str(depend_nr)
            service_file = open(filename, 'r')

            active_servs = []
            for line in service_file:
                active_servs.append([int(i) for i in line.split('	')])
            service_file.close()

            nr_srvs = len(active_servs)

            ## for each agent with id, choose total_servs/2, starting from index = id ######
            indices = []
            for i in range(agent_id - 1, agent_id + nr_srvs / 2 - 1):
                if i > nr_srvs - 1:
                    indices.append(i % len(active_servs))
                else:
                    indices.append(i)
            active_servs = [active_servs[i] for i in indices]
            ################################################################################

            ## Random way to choose services #########################################
            # remove 80% of services
            srv_remove = int(0.7 * nr_srvs)
            # for i in range(1, srv_remove + 1):
            # ind = random.randint(0, len(active_servs)-1)
            # active_servs.pop(ind)
            ##########################################################################
            return active_servs
        except IOError:
            print "Error: can\'t find file or read service_list file"
