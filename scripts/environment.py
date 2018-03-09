#!/usr/bin/env python
import sys
import rospy
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time
from gitagent.msg import *
from gitagent.srv import *
from threading import Lock
import pdb

class Environment:
    def __init__(self, width_height, difficulty, f, w, v):

        self.msgtopic = rospy.Subscriber('/environment/msg_topic', Protocol_Msg, self.callback_env_msg)
        self.tracktopic = rospy.Subscriber('/environment/track_locs', Track_Loc, self.callback_agent_loc_msg)
        self.publish_init_loc = rospy.Publisher('/environment/init_locs', Init_Loc, queue_size=200)

        self.publish_fires = rospy.Publisher('/environment/fires', Fires_Info, queue_size=200)

        self.publish_fbase = rospy.Publisher('/environment/fbase', Fire_Base, queue_size=200)
        self.publish_abase = rospy.Publisher('/environment/abase', Ambulance_Base, queue_size=200)

        self.pof = rospy.Service('/environment/put_out', Put_Out_Fire, self.put_out)
        self.sv = rospy.Service('/environment/save_victim', Save_Victim, self.save_victim)

        self.lock = Lock()

        self.width = width_height[0]
        self.height = width_height[1]
        # Place initial fires uniformly accross the space
        # Each fire will be a dict with the following keys: xpos, ypos, intensity, victims
        self.agents_XY = []
        self.agents_ID = []
        self.ffbase = []
        self.abase = []

        self.fires = []
        self.fires_cpy = []
        #self.no_fires = int(difficulty[0] * self.width * self.height)
        self.no_fires = f
        self.no_victims = 0
        print self.no_fires
        fire_id = 1
        points = []
        for x in range(0, self.no_fires):
            xpos = random.randint(0, self.width)
            ypos = random.randint(0, self.height)
            points.append([xpos, ypos])
            #intensity = random.randint(1, 50) # NOT IMPLEMENTED: when fire reaches 100, the task is considered lost
            #victims = random.randint(1, 10)
            intensity = w # NOT IMPLEMENTED: when fire reaches 100, the task is considered lost
            victims = v
            self.no_victims += victims
            self.fires.append({'id': fire_id, 'xpos': xpos, 'ypos': ypos, 'intensity': intensity, 'victims': victims, 'status': 1, 'once': 0})
            fire_id += 1
        self.fires_cpy = self.fires
        rospy.loginfo(str(self.fires))
        rospy.loginfo("Fires: %d, Intensity: %d, victims: %d" % (self.no_fires, intensity, self.no_victims))
        #for x in self.fires:
            #print x
        #print [x['xpos'] for x in self.fires]
        self.saved = 0
        self.extinguished = 0
        # Generate initial positions for agents
        self.init_agentXY(20, 3, points)
        # Generate bases
        self.init_bases([1,1], points)
        #Generate 2D space
        self.fig, self.ax = plt.subplots()
        self.ln_fire, = plt.plot([],[], 'ro')
        self.ln_agents, = plt.plot([],[], 'bs')

        self.result = plt.text(2.,29., 'extinguished: ' + str(self.extinguished) + ', saved: ' + str(self.saved))

        ani = animation.FuncAnimation(self.fig, self.draw_agents, self.new_data, init_func=self.init_2DSpace, interval=200)#interval=2000
        plt.grid()
        plt.show()
        '''
        rospy.loginfo(msg="environment is closing")
        env.msgtopic.unregister()
        rospy.loginfo(msg="unregistered msgtopic")
        env.tracktopic.unregister()
        rospy.loginfo(msg="unregistered track")
        env.publish_fires.unregister()
        rospy.loginfo(msg="unregistered publish fires")
        env.publish_init_loc.unregister()
        rospy.loginfo(msg="unregistered publish init loc")
        '''
        # sys.exit()

    def run_env(self):
        pass

    def init_2DSpace(self):
        self.ax.set_xlabel('x-points')
        self.ax.set_ylabel('y-points')
        self.ax.set_title('2D Space')
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ln_fire.set_xdata(np.array([x['xpos'] for x in self.fires]))
        self.ln_fire.set_ydata(np.array([x['ypos'] for x in self.fires]))
        return self.ln_fire,

    def init_bases(self, no_bases, forbidden_points):
        # no_bases: [ff,amb]
        for i in range(0,no_bases[0]):
            stop = False
            while not stop:
                # pdb.set_trace()
                xpos = random.randint(0, self.width)
                ypos = random.randint(0, self.height)
                self.ffbase.append({'ffbase_id': i + 1, 'xpos': xpos, 'ypos': ypos})
                stop = True
                #if [xpos, ypos] not in forbidden_points:
                    #self.ffbase.append({'ffbase_id': i+1, 'xpos': xpos, 'ypos': ypos})
                    #stop = True
        print self.ffbase
        ids = [x['ffbase_id'] for x in self.ffbase]
        xpos = [x['xpos'] for x in self.ffbase]
        ypos = [x['ypos'] for x in self.ffbase]
        fb_msg = Fire_Base()
        fb_msg.id = ids
        fb_msg.xpos = xpos
        fb_msg.ypos = ypos
        i = 0
        while i < 10:
            self.publish_fbase.publish(fb_msg)
            i += 1
            time.sleep(1)

        for i in range(0, no_bases[1]):
            stop = False
            while not stop:
                # pdb.set_trace()
                xpos = random.randint(0, self.width)
                ypos = random.randint(0, self.height)
                self.abase.append({'abase_id': i + 1, 'xpos': xpos, 'ypos': ypos})
                stop = True
                #if [xpos, ypos] not in forbidden_points:
                    #self.abase.append({'abase_id': i + 1, 'xpos': xpos, 'ypos': ypos})
                    #stop = True
        print self.abase
        ids = [x['abase_id'] for x in self.abase]
        xpos = [x['xpos'] for x in self.abase]
        ypos = [x['ypos'] for x in self.abase]
        ab_msg = Ambulance_Base()
        ab_msg.id = ids
        ab_msg.xpos = xpos
        ab_msg.ypos = ypos
        i = 0
        while i < 10:
            self.publish_abase.publish(ab_msg)
            i += 1
            time.sleep(1)

    # Assumes nr of agents fixed from the beginning - needs to be changed to accommodate dynamic spawning of new agents
    def init_agentXY(self, no_agents, groups, forbidden_points): #fb, ambulance, police
        ag_id = 1
        for x in range(0, 16): #2*no_agents/3
            self.agents_XY.append({'id': ag_id, 'xpos': 0, 'ypos':0})
            ag_id += 1

        d = [[0,0], [0,1], [1,1], [1,0]]
        cn = 0
        for x in range(16, no_agents):
        #for x in range(0, 4):
            stop = False
            while not stop:
                #pdb.set_trace()
                xpos = random.randint(d[cn][0]*self.width/2, (d[cn][0]+1)*self.width/2)
                ypos = random.randint(d[cn][1]*self.height/2, (d[cn][1]+1)*self.height/2)
                #time.sleep(5)
                if [xpos, ypos] not in forbidden_points:
                    self.agents_XY.append({'id': ag_id, 'xpos': xpos, 'ypos': ypos})
                    stop = True
            cn += 1
            ag_id += 1

        ids = [x['id'] for x in self.agents_XY]
        xpos = [x['xpos'] for x in self.agents_XY]
        ypos = [x['ypos'] for x in self.agents_XY]
        print self.agents_XY
        print ids
        print forbidden_points
        initLoc_msg = Init_Loc()
        initLoc_msg.ids = ids
        initLoc_msg.xpos = xpos
        initLoc_msg.ypos = ypos
        i = 0
        while i < 10:
            print initLoc_msg
            self.publish_init_loc.publish(initLoc_msg)
            i += 1
            time.sleep(1)

    def new_data(self):
        #print "i am here"
        yield [[x['xpos'] for x in self.agents_XY], [x['ypos'] for x in self.agents_XY]]

    def draw_agents(self, points):
        msg = 'number of connections: %d' % self.publish_fires.get_num_connections()
        if self.publish_fires.get_num_connections() < 1:
            msg = "about to close"
            rospy.loginfo(msg)
            with open("/home/mfi01/catkin_ws/results_final", 'a+') as final:
                final.write(str(self.extinguished) + ' ' + str(self.saved) + ' ' + str(self.no_victims) + '\n')
            plt.close()
            #sys.exit()
        self.ln_agents.set_xdata(np.array(points[0]))
        self.ln_agents.set_ydata(np.array(points[1]))
        # self.ln_fire.set_color(c=self.fire_colors)
        '''
        for x in self.fires_cpy:
            self.lock.acquire()
            if x['intensity'] > 0:
                #x['intensity'] += 1
                pass
            else:
                x['intensity'] = -1000
                if x['once'] == 0:
                    self.extinguished += 1
                    x['once'] = 1
                    x['status'] = 0
            self.lock.release()
        '''

        self.result.set_text('extinguished/total: ' + str(self.extinguished) + '/' +str(self.no_fires) + ', saved/total: ' + str(self.saved)+'/'+ str(self.no_victims))

        fire = Fires_Info()
        fire.id = [x['id'] for x in self.fires]
        fire.xpos = [x['xpos'] for x in self.fires]
        fire.ypos = [x['ypos'] for x  in self.fires]
        fire.intensity = [x['intensity'] for x in self.fires]
        fire.victims = [x['victims'] for x in self.fires]
        fire.status = [x['status'] for x in self.fires]
        self.publish_fires.publish(fire)
        rospy.loginfo(rospy.get_caller_id() + ' current state: %s', str(self.fires))
        msg += "Fires: %s" % self.fires
        rospy.loginfo(msg)
        print [x['intensity'] for x in self.fires]
        return self.ln_agents,

    def callback_env_msg(self, data):
        #rospy.loginfo(rospy.get_caller_id() + " Callback-from-env_msg %s, %s", data.sender, data.content)
        try:
            if not int(data.sender) in self.agents_ID:
                #self.lock.acquire()
                rospy.loginfo(rospy.get_caller_id() + " Callback-from-env_msg %s, %s", data.sender, data.content)
                self.agents_ID.append(int(data.sender))
                #self.lock.release()
            else:
                #print "already registered, ignore"
                pass
        except:
            rospy.loginfo(
                "Unexpected error: " + str(sys.exc_info()) + ". Line: " + str(sys.exc_info()[2].tb_lineno))
            pass

    def callback_agent_loc_msg(self, data):
        rospy.loginfo(rospy.get_caller_id() + " Update agent location %d, %d, %d", data.id, data.xpos, data.ypos)
        for x in self.agents_XY:
            if x['id'] == data.id:
                x['xpos'] = data.xpos
                x['ypos'] = data.ypos
                break

    def put_out(self, req):
        rospy.loginfo(rospy.get_caller_id() + ' put out service')
        for x in self.fires:
            if x['id'] == req.fire_id:
                self.lock.acquire()
                x['intensity'] -= req.put_out_step


                if x['intensity'] > 0:
                    # x['intensity'] += 1
                    pass
                else:
                    x['intensity'] = -1000
                    if x['once'] == 0:
                        self.extinguished += 1
                        x['once'] = 1
                        x['status'] = 0


                self.lock.release()
                return x['intensity']

    def save_victim(self, req):
        rospy.loginfo(rospy.get_caller_id() + ' pick up victim')
        for x in self.fires:
            if x['id'] == req.fire_id:
                self.lock.acquire()
                x['victims'] -= req.get_victim
                if x['victims'] > 0:
                    self.saved += 1
                else:
                    x['victims'] = -1000
                    if x['once'] == 1:
                        self.saved += 1
                        x['once'] = 2

                self.lock.release()
                return x['victims']

    #Advanced
    def generate_fires(self):
        pass

if __name__ == '__main__':
    try:
        rospy.init_node('environment', anonymous=True)
        f = int(rospy.get_param('env_node/maxFires'))
        w = int(rospy.get_param('env_node/maxIntensity'))
        v = int(rospy.get_param('env_node/maxVictim'))
        msg = "fires: %d, intensity: %d, victims: %d" % (f,w,v)
        rospy.loginfo(msg)
        env = Environment([30,30], [0.005], f, w, v)
        time.sleep(5)
        #rospy.spin()
    except:
        rospy.loginfo("Unexpected error: " + str(sys.exc_info()) + ". Line: " + str(sys.exc_info()[2].tb_lineno))

