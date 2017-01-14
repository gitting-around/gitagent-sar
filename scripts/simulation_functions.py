#!/usr/bin/env python
# no license, for the love of god

import sys
import random


# trick to emulate the selection of a couple of services the agent can provide
def select_services(agent_id, depend_nr):
    try:  # try to do it with relative paths
        filename = '/home/mfi01/catkin_ws/src/GITagent/scripts/services_list_' + str(depend_nr)
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
