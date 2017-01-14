/*********************************************************************
*
* Software License Agreement (BSD License)
*
*  Copyright (c) 2008, Willow Garage, Inc.
*  All rights reserved.
*
*  Redistribution and use in source and binary forms, with or without
*  modification, are permitted provided that the following conditions
*  are met:
*
*   * Redistributions of source code must retain the above copyright
*     notice, this list of conditions and the following disclaimer.
*   * Redistributions in binary form must reproduce the above
*     copyright notice, this list of conditions and the following
*     disclaimer in the documentation and/or other materials provided
*     with the distribution.
*   * Neither the name of Willow Garage, Inc. nor the names of its
*     contributors may be used to endorse or promote products derived
*     from this software without specific prior written permission.
*
*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
*  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
*  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
*  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
*  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
*  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
*  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
*  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
*  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
*  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
*  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
*  POSSIBILITY OF SUCH DAMAGE.
*
* Author: Eitan Marder-Eppstein
*********************************************************************/
#ifndef ACTIONLIB_SIMPLE_ACTION_SERVER_H_
#define ACTIONLIB_SIMPLE_ACTION_SERVER_H_

#include <boost/thread/condition.hpp>
#include <ros/ros.h>
#include <actionlib/server/action_server.h>
#include <actionlib/action_definition.h>

namespace actionlib {
  template <class ActionSpec>
  class SimpleActionServer {
    public:
      //generates typedefs that we'll use to make our lives easier
      ACTION_DEFINITION(ActionSpec);

      typedef typename ActionServer<ActionSpec>::GoalHandle GoalHandle;
      typedef boost::function<void (const GoalConstPtr&)> ExecuteCallback;

      SimpleActionServer(std::string name, ExecuteCallback execute_cb, bool auto_start);

      SimpleActionServer(std::string name, bool auto_start);

      ROS_DEPRECATED SimpleActionServer(std::string name, ExecuteCallback execute_cb = NULL);

      SimpleActionServer(ros::NodeHandle n, std::string name, ExecuteCallback execute_cb, bool auto_start);

      SimpleActionServer(ros::NodeHandle n, std::string name, bool auto_start);

      ROS_DEPRECATED SimpleActionServer(ros::NodeHandle n, std::string name, ExecuteCallback execute_cb = NULL);

      ~SimpleActionServer();

      boost::shared_ptr<const Goal> acceptNewGoal();

      bool isNewGoalAvailable();


      bool isPreemptRequested();

      bool isActive();

      void setSucceeded(const Result& result = Result(), const std::string& text = std::string(""));

      void setAborted(const Result& result = Result(), const std::string& text = std::string(""));


      void publishFeedback(const FeedbackConstPtr& feedback);

      void publishFeedback(const Feedback& feedback);

      void setPreempted(const Result& result = Result(), const std::string& text = std::string(""));

      void registerGoalCallback(boost::function<void ()> cb);

      void registerPreemptCallback(boost::function<void ()> cb);

      void start();

      void shutdown();

    private:
      void goalCallback(GoalHandle goal);

      void preemptCallback(GoalHandle preempt);

      void executeLoop();

      ros::NodeHandle n_;

      boost::shared_ptr<ActionServer<ActionSpec> > as_;

      GoalHandle current_goal_, next_goal_;

      bool new_goal_, preempt_request_, new_goal_preempt_request_;

      boost::recursive_mutex lock_;

      boost::function<void ()> goal_callback_;
      boost::function<void ()> preempt_callback_;
      ExecuteCallback execute_callback_;

      boost::condition execute_condition_;
      boost::thread* execute_thread_;

      boost::mutex terminate_mutex_;
      bool need_to_terminate_;
  };
};

//include the implementation here
#include <actionlib/server/simple_action_server_imp.h>
#endif
