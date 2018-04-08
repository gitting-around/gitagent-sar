#!/usr/bin/env python
# Parent class of agent, implementing the core parts of the theoretical concept
# Framework v1.0
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
import Queue
import turtle
import pdb
import traceback


class Visualizer():
    def __init__(self):

        self.turtle_queue = Queue.Queue()
        self.turtles = []
        # Of the form: [[id, pos], ...]
        # [[1, [2, 3]],[2, [6, 7]],[3, [1, 1]],[4, [9, 8]], ...]
        self.logistics = []
        self.colors = []

        rospy.init_node('visualizer', anonymous=True)
        rospy.Subscriber('/environment/agent_position', Protocol_Msg, self.put2queue)
        print 'i started'

        # init turtley stuff
        turtle.Screen()

    def put2queue(self, data):

        self.turtle_queue.put(data)

    def is_it_new(self, data):

        turtle_id = int(data.sender)
        print 'TURTLE ' + str(turtle_id)
        new = True

        for x in self.logistics:
            if turtle_id == x[0]:
                new = False

        pos = [float(x) for x in filter(None, data.content.split('|'))]
        print pos
        if new:

            self.turtles.append(turtle.Turtle())
            self.colors.append([random.random(), random.random(), random.random()])
            print self.colors
            self.logistics.append([turtle_id, pos])

        else:
            # only update position
            for x in self.logistics:
                if x[0] == turtle_id:
                    x[1] = pos
        print self.logistics
        print self.colors
        print self.turtles

    def draw_agents(self, data):
        print 'in the draw function'
        # pdb.set_trace()
        self.is_it_new(data)
        for x in self.logistics:
            print x
            if x[0] == int(data.sender):
                self.turtles[self.logistics.index(x)].color(self.colors[self.logistics.index(x)])
                self.turtles[self.logistics.index(x)].setx(x[1][0])
                self.turtles[self.logistics.index(x)].sety(x[1][1])


if __name__ == '__main__':
    stderr_file = '/home/ubuntu/catkin_ws/results/error_viz'
    f = open(stderr_file, 'w+')
    orig_stderr = sys.stderr
    sys.stderr = f

    stdout_file = '/home/ubuntu/catkin_ws/results/stdout_viz'
    s = open(stdout_file, 'w+')
    orig_stdout = sys.stdout
    try:
        visualize = Visualizer()
        while True:
            # This will block until there is something new in the queue:)
            data = visualize.turtle_queue.get()
            visualize.draw_agents(data)
    except rospy.ROSInterruptException:
        traceback.print_exc()
        raise
    except (AttributeError, TypeError, ValueError, NameError):
        traceback.print_exc()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc()
        raise
    finally:
        sys.stderr = orig_stderr
        f.close()
        sys.stdout = orig_stdout
        s.close()
