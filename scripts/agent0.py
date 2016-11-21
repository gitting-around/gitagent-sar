#!/usr/bin/env python
#Parent class of agent, implementing the core parts of the theoretical concept
#Framework v1.0
import sys
import time
import mylogging
import core_aboutme
import knowledge
import simulation
import rospy
from gitagent.msg import *
from gitagent.srv import *
from threading import Lock
import random

class Agent0:
	def __init__(self, ID, inputs, outputs, services, init_knowledge, languages, protocols, willingness, simulation, popSize, provaNr, depend_nr, battery, sensors, actuators, motors):

		#logging class
		self.log = mylogging.Logging(popSize, provaNr, ID, willingness[1], depend_nr)

		#They will contain arrays of topic's names ###
		self.inputs = inputs
		self.publish_bcast = []
		self.outputs = outputs
		self.init_inputs(self.inputs)
		self.init_outputs(self.outputs)
		self.init_serve(ID)
		##############################################

		#Enumerated lists for each ###
		self.services = services
		self.languages = languages
		self.protocols = protocols
		#############################

		#Variables manipulated by multiple threads ###
		self.adaptive_state = []
		##############################################

		#Contains info specific to the internal state of the agent such as: state, health attributes etc.
		self.mycore = core_aboutme.Core(willingness, ID, battery, sensors, actuators, motors)
		self.log.write_log_file(self.log.stdout_log, 'init gitagent ' + str(self.mycore.sensmot) + '\n')
		#Contains mixed info #########################
		self.myknowledge = knowledge.Knowledge0()

		#use simulation functions
		self.simulation = simulation

	def fsm(self):
		while True:
			self.change_selfstate()
			#normally you might want to estimate a value that corresponds to the cost of each cycle
			self.mycore.battery_change(-1)
			self.mycore.sensory_motor_state_mockup()
			self.mycore.check_health()
			#funksioni meposhte mund te ekzekutohet ne paralel --> per tu zhvilluar me tej ne nje moment te dyte
			self.publish2sensormotor(self.services)
			self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + '] current state: ' + str(self.mycore.state) + '\n')

			##MOVE ###############################################################################
			self.myknowledge.position2D = self.simulation.move(self.myknowledge.position2D)
			self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + '] self.myknowledge.position2D: ' + str(self.myknowledge.position2D) + '\n')
			if not rospy.is_shutdown():
				self.publish_bcast[1].publish(self.mycore.create_message(self.myknowledge.position2D, 'position'))
			######################################################################################

			self.fsm_step()

	def fsm_step(self):
		self.simulation.fsm = self.simulation.inc_iterationstamps(self.simulation.fsm)

		if self.mycore.state == 0:
			self.idle()
		elif self.mycore.state == 1:
			self.interact()
		elif self.mycore.state == 2:
			self.execute()
		elif self.mycore.state == 3:
			self.regenerate()
		elif self.mycore.state == 4:
			self.dead()

		#time.sleep(1)	

	def change_selfstate(self):
		print 'ADAPTIVE STATE: ', self.adaptive_state
		self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + '] adaptive state: ' + str(self.adaptive_state) + '\n')

		self.myknowledge.lock.acquire()
		if True in self.adaptive_state:
			self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + '] current client_index: ' + str(self.myknowledge.client_index) + '\n')
			self.myknowledge.old_client_index = self.myknowledge.client_index
			self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + '] ' + str(self.adaptive_state) + ' ' + str(self.myknowledge.current_client) + '\n')
			self.myknowledge.client_index = self.adaptive_state.index(True)

			self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + '] ' + str(self.adaptive_state) + ' ' + str(self.myknowledge.current_client) + '\n')
			self.myknowledge.old_state = self.mycore.state
			self.mycore.state = 1
			self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.fsm) + '] ' + str(self.adaptive_state) + ' ' + str(self.myknowledge.current_client) + '\n')
			self.adaptive_state[self.adaptive_state.index(True)] = False
		self.myknowledge.lock.release()

	def idle(self):
		print 'im in idle'
		self.simulation.idle = self.simulation.inc_iterationstamps(self.simulation.idle)
		self.log.write_log_file(self.log.stdout_log, '[fsm ' + str(self.simulation.idle) + ']\n')
		self.generate_goal()
		self.commit2goal()

	def interact(self):
		print 'im in interact'
		self.simulation.interact = self.simulation.inc_iterationstamps(self.simulation.interact)

		self.eval_temp()

		self.evaluate_my_state()
		self.evaluate_agent()
		self.evaluate_request()
		self.commit2agent()

	def execute(self):
		print 'im in execute'
		self.simulation.execute = self.simulation.inc_iterationstamps(self.simulation.execute)

		self.plan2goal()
		self.execute_step(self.myknowledge.service, self.myknowledge.iteration)
	
	def execute_step(self, service, iteration):

		timeout = time.time() + 10
		depend = self.resolve_dependencies(service)
		print 'depend: ', depend

		if iteration <= service[1] and not depend:
			print 'iteration: ', iteration
			self.myknowledge.iteration = self.myknowledge.iteration + 1
			self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] Doing task %d, iteration: %d\n' % (service[0], iteration))

			if self.myknowledge.iteration > service[1]:
				self.mycore.state = 0
				self.myknowledge.iteration = 1

				self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] client_index %d, helping %s\n' % (self.myknowledge.client_index, self.myknowledge.helping))
				print 'helping: ', self.myknowledge.helping
				if self.myknowledge.helping:
					self.myknowledge.service_req[self.myknowledge.client_index] = -1
					if random.random() > 0: #it will always succeed
						self.myknowledge.lock.acquire()
						self.myknowledge.service_resp_content[self.myknowledge.client_index] = 1
						self.myknowledge.lock.release()
						self.myknowledge.completed_jobs = self.myknowledge.completed_jobs + 1
						self.myknowledge.collected_reward = self.myknowledge.collected_reward + service[3]

						self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] Helping, Task %d, done, wandering again\n' % service[0])

					else:
						self.myknowledge.lock.acquire()
						self.myknowledge.service_resp_content[self.myknowledge.client_index] = 0
						self.myknowledge.lock.release()
						self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] Helping, Task %d, failed, wandering again\n' % service[0])

					self.myknowledge.lock.acquire()
					self.myknowledge.service_resp[self.myknowledge.client_index] = True
					self.myknowledge.lock.release()
					self.myknowledge.helping = False
					self.myknowledge.client_index = -1
				else:
					self.myknowledge.completed_jobs = self.myknowledge.completed_jobs + 1
					self.myknowledge.collected_reward = self.myknowledge.collected_reward + service[3]

					self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] Task %d, done, wandering again\n' % service[0])
			print 'compl jobs: ', self.myknowledge.completed_jobs
		elif iteration <= service[1] and depend:
			self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] Doing task %d, iteration. Depend is true\n' % service[0])

			stringing = str(service[4])
			if not len(self.myknowledge.known_people) == 0:
				anyone = False
				anyone_id = []
				anyone_id_idx = []
				subset_known = []
				anyone_index = -1
				jj = -1

				for x in self.myknowledge.known_people:
					if service[4] in x[2]:
						subset_known.append(x)
						anyone_id.append(x[0])
						anyone = True
						anyone_id_idx.append(self.myknowledge.known_people.index(x))

				self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] anyone_id: ' + str(anyone_id) + '\n' + '[run_step ' + str(self.simulation.execute) + '] anyone_id_idx: ' + str(anyone_id_idx) + '\n' + '[run_step ' + str(self.simulation.execute) + '] subset: ' + str(subset_known) + '\n')

				if anyone:
					## function to choose the server -- right now random from the list above
					if self.simulation.execute < self.myknowledge.steps_b4_equilibrium:
						jj = random.randint(0, len(anyone_id) - 1)
						self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] jj at random: %d\n' % jj)
					else:
						if random.random() < 0.8:
							jj = subset_known.index(max(subset_known, key=lambda x: x[1]))
							self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] jj using lambda function: %d\n' % jj)
						else:
							jj = random.randint(0, len(anyone_id) - 1)
							self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] jj at random after equilibrium: %d\n' % jj)
					anyone_index = anyone_id_idx[jj]
					server = anyone_id[jj]

					self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] anyone_id: ' + str(anyone_id[jj]) + '\n' + '[run_step ' + str(self.simulation.execute) + '] anyone_index: ' + str(anyone_index) + '\n' + '[run_step ' + str(self.simulation.execute) + '] server: ' + str(server) + '\n')

					server_resp = -1000
					print 'i am %d, asking for %d' %(self.mycore.ID, int(server))
					try:
						server_resp = int(self.call_serve(server, self.mycore.ID, stringing, anyone_index))
					except:
						self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] it went to heell ' + str(server_resp) + '\n')
						self.simulation.hell = self.simulation.hell + 1
						server_resp = -1
						pass

					print 'checking after service return: ' + str(server_resp)
					self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] checking after service return: ' + str(server_resp) + '\n')
					self.mycore.state = 0
					self.myknowledge.iteration = 1

					if server == self.myknowledge.client_index:
						self.myknowledge.count_loops = self.myknowledge.count_loops + 1
						self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] counting loops + 1' + '\n')
					#here is where you update the values for the agent's expertise and perceived willingness to help
					if server_resp == 1:
						self.myknowledge.completed_jobs = self.myknowledge.completed_jobs + 1
						self.myknowledge.completed_jobs_depend = self.myknowledge.completed_jobs_depend + 1
						self.myknowledge.collected_reward = self.myknowledge.collected_reward + service[3]

						print 'Task %d, done, wandering again with help' % service[0]
						self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] Task %d, done, wandering again\n' % service[0])
					else:
						prob = random.random()
						self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] prob %d: \n' % prob)
						if prob <= 0.3:
							self.myknowledge.completed_jobs = self.myknowledge.completed_jobs + 1
							self.myknowledge.completed_jobs_depend = self.myknowledge.completed_jobs_depend + 1
							self.myknowledge.collected_reward = self.myknowledge.collected_reward + service[3]
							self.myknowledge.depend_myself = self.myknowledge.depend_myself + 1

							self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] Task %d, done by myslef, after failed help request\n' % service[0])
							print 'task done by self, after failed request'
							server_resp = 1
						else:
							self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] Task %d, failed, both help request and by myself\n' % service[0])
							print 'failed, both myself and with help'

					if self.myknowledge.helping:
						self.myknowledge.lock.acquire()
						self.myknowledge.service_req[self.myknowledge.client_index] = -1
						self.myknowledge.service_resp_content[self.myknowledge.client_index] = server_resp
						self.myknowledge.service_resp[self.myknowledge.client_index] = True
						self.myknowledge.lock.release()
						self.myknowledge.helping = False
						self.myknowledge.client_index = -1
				else:
					server_resp = 0

					self.myknowledge.COUNT_noones = self.myknowledge.COUNT_noones + 1
					self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] no one to ask that has this capability\n' + '[run_step ' + str(self.simulation.execute) + '] Doing task %d\n' % service[0])
					print 'no one to ask for this'

					self.mycore.state = 0
					if self.myknowledge.helping:
						self.myknowledge.lock.acquire()
						self.myknowledge.service_req[self.myknowledge.client_index] = -1
						self.myknowledge.service_resp_content[self.myknowledge.client_index] = server_resp
						self.myknowledge.service_resp[self.myknowledge.client_index] = True
						self.myknowledge.lock.release()
						self.myknowledge.helping = False
						self.myknowledge.client_index = -1
				#self.service_req = -1 --- careful with this one
			else:
				self.myknowledge.COUNT_noones = self.myknowledge.COUNT_noones + 1
				self.log.write_log_file(self.log.stdout_log, '[run_step ' + str(self.simulation.execute) + '] no one to ask\n' + '[run_step ' + str(self.simulation.execute) + '] Doing task %d\n' % service[0])
				print 'no one to ask'
				server_resp = 0
				if self.myknowledge.helping:
					self.myknowledge.lock.acquire()
					self.myknowledge.service_req[self.myknowledge.client_index] = -1
					self.myknowledge.service_resp_content[self.myknowledge.client_index] = server_resp
					self.myknowledge.service_resp[self.myknowledge.client_index] = True
					self.myknowledge.lock.release()
					self.myknowledge.helping = False
					self.myknowledge.client_index = -1
				self.mycore.state = 0


	def regenerate(self):
		print 'im in regenerate'
		self.simulation.regenerate = self.simulation.inc_iterationstamps(self.simulation.regenerate)

		self.debug_self()
		self.fix_bugs()

	def dead(self):
		print 'im in dead'
		self.simulation.dead = self.simulation.inc_iterationstamps(self.simulation.dead)

		self.evaluate_self()
		self.evaluate_environment()
		self.evaluate_selfmending()

	#MUST be overriden in the child class, depending on the different types of inputs!
	def init_inputs(self, inputs):
		pass

	def init_outputs(self, outputs):
		for x in outputs:
			self.publish_bcast.append(rospy.Publisher(x, Protocol_Msg, queue_size=200))
		print self.publish_bcast

	def generate_goal(self):
		if random.random() > 0.7:
			self.myknowledge.task_idx = random.randint(1, len(self.services)) - 1 #randint(a,b) kthen int ne [a,b]
			self.myknowledge.service = self.services[self.myknowledge.task_idx]

			self.myknowledge.attempted_jobs = self.myknowledge.attempted_jobs + 1

			print "task_idx %d: " % self.myknowledge.task_idx
			print "service selected ", self.myknowledge.service
			print "all services ", self.services

			if len(self.myknowledge.service) > 4:
				self.myknowledge.attempted_jobs_depend = self.myknowledge.attempted_jobs_depend + 1

			self.log.write_log_file(self.log.stdout_log, '[wander ' + str(self.simulation.idle) + '] Chosen service: ' + str(self.myknowledge.service) + '\n')

			self.mycore.state = 2
		else:
			self.log.write_log_file(self.log.stdout_log, '[wander ' + str(self.simulation.idle) + '] do nothing - zot jepi atij qe rri kot :DD\n')
			print "some crap"

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

	def eval_temp(self):
		for x in self.services:
			if x[0] == self.myknowledge.service_req[self.myknowledge.client_index]:
				self.myknowledge.task_idx = self.services.index(x)

		#Decide if it is good to accept request

		self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(self.simulation.interact) + '] client: %d, service_resp: %s\n' % (self.myknowledge.current_client[self.myknowledge.client_index], str(self.myknowledge.service_resp[self.myknowledge.client_index])) + '[adapt ' + str(self.simulation.interact) + '] old serve: %s\n' % (str(self.myknowledge.service)))

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

		accept = self.keep_request(self.myknowledge.current_client[self.myknowledge.client_index], self.services[self.myknowledge.task_idx], self.myknowledge.old_state, self.myknowledge.service, rate, rate_depend)
		if self.simulation.handle > 0:
			self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(self.simulation.interact) + '] handled = %d\n' % (self.simulation.handle))
			self.myknowledge.timeouts_xinteract.append(1.0 * self.myknowledge.timeouts/self.simulation.handle)
		else:
			self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(self.simulation.interact) + '] nope, nope, nope\n')
			print 'nope'

		self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(self.simulation.interact) + '] accept ' + str(accept) + '\n')

		if accept:
			self.myknowledge.count_posReq = self.myknowledge.count_posReq + 1
			self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(self.simulation.interact) + '] adapted\n')

			self.myknowledge.attempted_jobs = self.myknowledge.attempted_jobs + 1

			self.myknowledge.iteration = 1
			self.mycore.state = 2
			self.myknowledge.service = self.services[self.myknowledge.task_idx]

			if len(self.myknowledge.service) > 4:
				self.myknowledge.attempted_jobs_depend = self.myknowledge.attempted_jobs_depend + 1

			self.myknowledge.helping = True
			self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(self.simulation.interact) + '] service: ' + str(self.myknowledge.service) + '\n' + '[adapt ' + str(self.simulation.interact) + '] helping: ' + str(self.myknowledge.helping) + '\n')

		else:
			print 'keep at what you\'re doing'
			#praktikisht e le pergjysem kerkesen
			self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(self.simulation.interact) + '] keep at what you\'re doing\n' + '[adapt ' + str(self.simulation.interact) + '] before if: current client_index: ' + str(self.myknowledge.client_index) + '\n')
			if not self.myknowledge.client_index == -1:
				self.myknowledge.lock.acquire()
				self.myknowledge.service_req[self.myknowledge.client_index] = -1
				self.myknowledge.service_resp_content[self.myknowledge.client_index] = -1
				self.myknowledge.service_resp[self.myknowledge.client_index] = True
				self.myknowledge.lock.release()
			
			self.myknowledge.client_index = self.myknowledge.old_client_index
			self.log.write_log_file(self.log.stdout_log, '[adapt ' + str(self.simulation.interact) + '] after old state: current client_index: ' + str(self.myknowledge.client_index) + '\n')

			self.mycore.state = self.myknowledge.old_state		

	def keep_request(self, client, new_service, state, old_service, jobs_dropped, depend_done):
		accept = False
		## what you need to make only one agent dynamic ############################################################################################################
		if self.mycore.ID == 7:
			drop_rate = jobs_dropped - self.myknowledge.past_jobs_dropped
			self.log.write_log_file(self.log.stdout_log, '[dep_delta] dropped: %f, past_dropped: %f, past delta: %f\n' % (jobs_dropped, self.myknowledge.past_jobs_dropped, self.mycore.willingness[1]))

			#self.delta = self.delta - (jobs_dropped - self.past_jobs_dropped) * jobs_dropped
			if jobs_dropped > self.myknowledge.HIGH:
				self.mycore.willingness[1] = self.mycore.willingness[1] - self.myknowledge.step
				self.log.write_log_file(self.log.stdout_log, '[dep_delta] delta decreased %f by step %f\n'%(self.mycore.willingness[1], self.myknowledge.step))
			elif jobs_dropped < self.myknowledge.LOW:
				self.mycore.willingness[1] = self.mycore.willingness[1] + self.myknowledge.step
				self.log.write_log_file(self.log.stdout_log, '[dep_delta] delta increased %f by step %f\n'%(self.mycore.willingness[1], self.myknowledge.step))
			elif abs(drop_rate) >= 0.01:
				self.log.write_log_file(self.log.stdout_log, '[dep_delta] entered else, L < jb_d < H\n')
				inc_dec = 1 if drop_rate >= 0 else -1
				self.mycore.willingness[1] = self.mycore.willingness[1] - inc_dec*self.myknowledge.step
				self.log.write_log_file(self.log.stdout_log, '[dep_delta] delta change %f by step %f, inc_dec = %d\n'%(self.mycore.willingness[1], self.myknowledge.step, inc_dec))
			else:
				self.log.write_log_file(self.log.stdout_log, '[dep_delta] delta doesn\'t change, else condition, %f by step %f\n'%(self.mycore.willingness[1], self.myknowledge.step))	
				print 'no change'

			#fit to [0,1]
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

		self.log.write_log_file(self.log.stdout_log, '[dep_delta] moving_delta_sorted = %s\n' % str(self.myknowledge.moving_delta_sorted))
		self.log.write_log_file(self.log.stdout_log, '[dep_delta] moving_drop_jobs = %s\n' % str(self.myknowledge.moving_drop_jobs))

		match = False
		if self.myknowledge.moving_delta:
			for x in self.myknowledge.moving_delta:
				if client in x:
					self.myknowledge.moving_delta[self.myknowledge.moving_delta.index(x)].append(self.mycore.willingness[1])
					match = True
					break
			if not match:
				self.myknowledge.moving_delta.append([client, self.mycore.willingness[1]])
		else:
			self.myknowledge.moving_delta.append([client, self.mycore.willingness[1]])

		check_rand = random.random()

		if check_rand < self.mycore.willingness[1]:
			accept = True
		
		print 'ACCEPT: ', accept

		return accept

	def publish2sensormotor(self, raw_content):
		if not rospy.is_shutdown():
			print rospy.get_name()
			self.publish_bcast[0].publish(self.mycore.create_message(raw_content, ''))
		else:
			print 'rospy is shutdown'

	def init_serve(self, agentid):
		myservice = '/robot' + str(agentid) + '/serve'
		print 'DECLARING my service'
		srv = rospy.Service(myservice, Protocol_Srv, self.handle_serve)

	def handle_serve(self, request):
		pass

	def call_serve(self, server, myid, request, anyone_index):
		pass

