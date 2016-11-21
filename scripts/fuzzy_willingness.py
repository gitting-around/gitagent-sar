#!/usr/bin/env python
#Fuzzy algorithm which considers only one input --> health

import sys
import random
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

#Define some parameters
hmin = 400
hmax = 4000
hdiff = 10

unitmin = 0
unitmax = 1
unitdiff = 0.1

#Define antecedents (inputs): holds variables and membership functions
#Health represents an aggregation of the values for battery, sensor, actuator and motor condition
health = ctrl.Antecedent(np.arange(hmin, hmax, hdiff), 'health')

#Best known agent to ask, in which helpfulness and success rate are combined beforehand, using a dot product
best_agent = ctrl.Antecedent(np.arange(unitmin, unitmax, unitdiff), 'best_agent')

#The environment represents a combined value of the danger associated with physical obstacles, and the general culture of the population
#as in the case of the best known agent, these can be combined using a dot product
environment = ctrl.Antecedent(np.arange(unitmin, unitmax, unitdiff), 'environment')

#Agent abilities and resources needed in the scope of one task could also be combined in order to be represented by one fuzzy input
abil_res = ctrl.Antecedent(np.arange(unitmin, unitmax, unitdiff), 'abil_res')
abil_res['some'] = fuzz.trapmf(abil_res.universe, [0.0, 0.0, 0.4, 0.4])
abil_res['all_&optional'] = fuzz.trapmf(abil_res.universe, [0.6, 0.6, 1.0, 1.0])
abil_res.view()
#The agent's own progress wrt to tasks, or plans in general could also serve as a trigger to interact or not
own_progress = ctrl.Antecedent(np.arange(unitmin, unitmax, unitdiff), 'own_progress')

#Fuzzy output, the willingness to ask for help
willingness = ctrl.Consequent(np.arange(unitmin, unitmax, unitdiff), 'willingness')

#Auto membership function population
health.automf(3)
best_agent.automf(3)
environment.automf(3)
own_progress.automf(3)
willingness.automf(3)

#health.view()
#willingness.view()

#Define rules
rules = []

## either poor health or only some of abilities and resources are enough to have high willingness to ask for help
rules.append(ctrl.Rule(health['poor'] | abil_res['some'] | own_progress['poor'], willingness['good']))
rules.append(ctrl.Rule((health['good'] | health['average']) & abil_res['all_&optional'] & (own_progress['good'] | own_progress['average']), willingness['poor']))
rules.append(ctrl.Rule(best_agent['good'] & health['average'] & abil_res['all_&optional'], willingness['average']))
rules.append(ctrl.Rule(best_agent['poor'] & health['average'] & abil_res['all_&optional'], willingness['poor']))

# 

## View rules graphically
#rule1.view()

tipping_ctrl = ctrl.ControlSystem(rules)
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
tipping.input['health'] = 2000
tipping.input['best_agent'] = 0.5
tipping.input['abil_res'] = 0.7
tipping.input['own_progress'] = 0.3

tipping.compute()

print tipping.output['willingness']
willingness.view(sim=tipping)

#while True:
#	pass
