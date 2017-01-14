#!/usr/bin/env python
import sys
import random
import traceback
import time
import pdb


class Willingness:
    def __init__(self):

        # Willingness to ask for assistance
        self.ask = False

        # Willingness to give assistance
        self.give = False

        # Thresholds -- percentage of affordance
        self.LOW = 0.3
        self.High = 0.7

    # Function will return True if decided to ask for help, or False otherwise
    def ask_4help(self, health, abilities, resources, self_esteem, task_urgency, task_importance, culture,
                  best_candidate):

        self.ask = False

        if health < self.LOW:
            return True
        else:
            if abilities < self.LOW:
                return True
            else:
                if resources < self.LOW:
                    return True
                else:
                    if self_esteem < self.HIGH:
                        if task_urgency > self.LOW or task_importance > self.LOW:
                            return True
                        else:
                            if culture > self.LOW and best_candidate > self.LOW:
                                return True
                    else:
                        if culture > self.HIGH and best_candidate > self.HIGH:
                            if task_urgency > self.LOW or task_importance > self.LOW:
                                return True

    # Function will return True if decided to give help, or False otherwise
    def give_help(self):
        pass
