#!/usr/bin/env bash
./mean.py "static_0_05" trials/trial1/static_0.05/static_total trials/trial2/static_0.05/static_total trials/trial3/static_0.05/static_total
./mean.py "static_0_125" trials/trial1/static_0.125/static_total trials/trial2/static_0.125/static_total trials/trial3/static_0.125/static_total
./mean.py "static_0_2" trials/trial1/static_0.2/static_total trials/trial2/static_0.2/static_total trials/trial3/static_0.2/static_total

./mean.py "nomem_0_05" trials/trial1/nomem_0.05/dynamic_total trials/trial2/nomem_0.05/dynamic_total trials/trial3/nomem_0.05/dynamic_total
./mean.py "nomem_0_125" trials/trial1/nomem_0.125/dynamic_total trials/trial2/nomem_0.125/dynamic_total trials/trial3/nomem_0.125/dynamic_total
./mean.py "nomem_0_2" trials/trial1/nomem_0.2/dynamic_total trials/trial2/nomem_0.2/dynamic_total trials/trial3/nomem_0.2/dynamic_total

./mean.py "mem_0_05" trials/trial1/mem_0.05/dynamic_total trials/trial2/mem_0.05/dynamic_total trials/trial3/mem_0.05/dynamic_total
./mean.py "mem_0_125" trials/trial1/mem_0.125/dynamic_total trials/trial2/mem_0.125/dynamic_total trials/trial3/mem_0.125/dynamic_total
./mean.py "mem_0_2" trials/trial1/mem_0.2/dynamic_total trials/trial2/mem_0.2/dynamic_total trials/trial3/mem_0.2/dynamic_total
