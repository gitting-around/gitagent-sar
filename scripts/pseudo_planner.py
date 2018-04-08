#!/usr/bin/env python
import sys
import time
import simulation
import rospy
from gitagent.msg import *
from gitagent.srv import *
import random
import math
import pdb
import traceback


# Plan format
# [[agent1, [task_ids]], [agent2, [task_ids]], ...]
# Plan message format
# Plan ID --- and maybe other metadata
# agentID | taskID taskID
# agentID | taskID taskID
# ...
# agentID | taskID taskID

# Task format
# Keep mine for now, but it will need to change

class PseudoPlanner:
    def __init__(self, plan):

        self.plan4agents = plan
        rospy.init_node('pseudo_planner', anonymous=True)
        self.publish_plan = rospy.Publisher('/environment/plan', Protocol_Msg, queue_size=200)

        self.used_planID = []

        sim = simulation.Simulation0()
        self.tasks, self.unformattedTasks = sim.get_tasks('specs')

    def create_message(self, plan):
        message = Protocol_Msg()
        message.performative = 'highlevelplan'
        message.sender = '0'
        message.rank = 10
        message.receiver = 'all'
        message.language = 'shqip'
        message.ontology = 'shenanigans'
        message.urgency = 'INFO'
        message.content = self.create_msg_content(plan)
        message.timestamp = time.strftime('%X', time.gmtime())
        return message

    def create_msg_content(self, plan):

        # content = str(plan[0]) + '\n'
        # plan.pop(0)
        # for x in plan:
        # content = content + str(x[0]) + '|'
        # for y in x[1]:
        # content = content + str(y)
        # if x[1].index(y) < len(x[1])-1:
        # content = content  + ' '
        # if plan.index(x) < len(plan)-1:
        # content = content + '\n'

        # pdb.set_trace()
        print plan
        content = str(plan[0]) + '\n'
        plan.pop(0)
        for x in plan:
            content = content + str(x[0]) + '$'
            for y in x[1]:
                content = content + str(y) + '#'

        print content
        return content

    def publish_new_plan(self, repeat_loop):

        plan = self.create_message(self.plan4agents)
        rate = rospy.Rate(10)  # 10Hz

        while not rospy.is_shutdown():
            self.publish_plan.publish(plan)
            print 'PUBLISHED'
            rate.sleep()

    def generate_plan(self, agents, plan_length, plan_complexity):
        # agents - list of ids
        # tasks - list of dictionaries, each dictonary represents a task
        # plan_length - int determining the number of tasks - to be kept fixed
        # plan_complexity - 0, 1, 2 - low, medium, high

        # pdb.set_trace()
        plan = []
        plan_id = random.randint(1, 100)
        plan.append(plan_id)

        for x in agents:
            temp = []
            if plan_complexity == 0:
                for i in range(0, int(math.floor(0.75 * plan_length))):
                    temp.append(self.unformattedTasks[0])
                for i in range(0, int(math.floor(0.25 * plan_length))):
                    temp.append(self.unformattedTasks[1])
            elif plan_complexity == 1:
                for i in range(0, int(math.floor(0.50 * plan_length))):
                    temp.append(self.unformattedTasks[0])
                for i in range(0, int(math.floor(0.25 * plan_length))):
                    temp.append(self.unformattedTasks[1])
                for i in range(0, int(math.floor(0.25 * plan_length))):
                    temp.append(self.unformattedTasks[2])
            elif plan_complexity == 2:
                for i in range(0, int(math.floor(0.20 * plan_length))):
                    temp.append(self.unformattedTasks[0])
                for i in range(0, int(math.floor(0.25 * plan_length))):
                    temp.append(self.unformattedTasks[1])
                for i in range(0, int(math.floor(0.50 * plan_length))):
                    temp.append(self.unformattedTasks[2])
            plan.append([x, temp])

        print plan

        self.plan4agents = plan


if __name__ == '__main__':
    stderr_file = '/home/ubuntu/.ros/RESULT/error_plan'
    f = open(stderr_file, 'w+')
    orig_stderr = sys.stderr
    sys.stderr = f

    stdout_file = '/home/ubuntu/.ros/RESULT/stdout_plan'
    s = open(stdout_file, 'w+')
    orig_stdout = sys.stdout
    try:
        plan = [1, [1, [2]], [2, [4]], [3, [7]]]
        repeat_loop = 1200000
        pplanner = PseudoPlanner(plan)
        pplanner.generate_plan([1], 10, 0)
        pplanner.publish_new_plan(repeat_loop)
        rospy.spin()
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
