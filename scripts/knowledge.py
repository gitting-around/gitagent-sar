#!/usr/bin/env python
# Parent class of agent, implementing the core parts of the theoretical concept
# Framework v1.0
import sys
from threading import Lock
import random
import Queue


class Knowledge0:
    def __init__(self):
        ## use to differentiate between when I'm doing something for me and for others.
        self.helping = False

        # use this variable to count the instances in which an agent asks for help the same agent who asked it for help in the first place
        self.count_posReq = 0
        self.COUNT_noones = [0,0,0]
        self.count_loops = 0

        self.steps_b4_equilibrium = 100

        self.lock = Lock()
        self.lock_cb = Lock()

        self.attempted_jobs = 0
        self.completed_jobs = 0
        self.attempted_jobs_depend = 0
        self.completed_jobs_depend = 0
        self.depend_myself = 0
        self.collected_reward = 0

        self.old_state = 0
        self.own_progress = -1
        self.task_urgency = -1

        ## These vars are manipulated by multiple threads ###
        self.current_client = []
        self.service_req = []
        self.service_resp = []
        self.service_resp_content = []
        #####################################################

        self.task_queue = Queue.Queue()
        self.plan_pending_eval = Queue.Queue()

        self.client_index = -1
        self.old_client_index = -1

        # Agent cultures
        # Array - [total helpfulness, total expertise, total load]
        self.culture = [-1, -1, -1]

        # follows the indexing of known_people
        self.helping_interactions = []
        self.total_interactions = []

        # example format [[[e1-pos-inter, e1-tot-inter], [e2-pos-inter, e2-tot-inter] ...], ..], for serv1, serv2.... for the first guy in known_people
        self.capability_expertise = []

        self.timeouts = 0

        self.timeouts_xinteract = []

        self.task_idx = -1

        self.changed_servs = 1

        self.service = []
        self.service_id = -1
        self.iteration = -1
        self.difficulty = -1

        self.known_people = []
        # If an agent receives a request from another, without it being in its list, it will be put here

        self.moving_delta = []
        self.moving_delta_sorted = []
        self.moving_drop_jobs = []
        self.moving_depend_done = []

        self.past_jobs_dropped = 0
        self.HIGH = 0.7
        self.LOW = 0.3
        self.step = 0.05

        # Knowledge regarding position in a 2D space
        self.position2D = [-1, -1]
        # kmS/secS
        self.speed = [80,120]
