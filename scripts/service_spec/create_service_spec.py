#!/usr/bin/env python

import sys
import random

def generate_service_spec():
	no_serve = int(input("Enter number of services: "))
	service_spec = []

	#[id, iterations, energy, reward, [mandatory resources], [optional resources], permission, urgency, estimated_time, [known dependencies (no array for now, just one)]]
	# permission, urgency, and estimated_time won't be put here, the question is where?
	for i in range(1, no_serve + 1):
		no_iter = random.randint(1, 1000)
                energy = random.randint(100, 1000)
                reward = random.randint(1000, 4000)

		no_mresources = int(input("Enter number of mandatory resources: "))
		mresources = []
		for j in range(1, no_mresources + 1):
			risurs = int(input("Type next mandatory resource from 1 to 50: "))
			mresources.append(risurs)

		no_oresources = int(input("Enter number of optional resources: "))
		oresources = []
		for j in range(1, no_oresources + 1):
			risurs = int(input("Type next optional resource from 1 to 50: "))
			oresources.append(risurs)

		no_deps = int(input("Enter number of dependencies on other services: "))
		dependencies = []
		for j in range(1, no_deps + 1):
			deps = int(input("Type next dependency from 1 to " + str(no_deps) + ": "))
			dependencies.append(deps)

		print no_iter, energy, reward, mresources, oresources, dependencies

		service_spec.append([no_iter, energy, reward, mresources, oresources, dependencies])
	print service_spec
	return service_spec

def write_array2file(filename, specs):
	with open(filename, 'a+') as f:
		for i in specs:
			f.write(str(i) + '\n')

if __name__=='__main__':
	specs = generate_service_spec()
	write_array2file('specs', specs)
