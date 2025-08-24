#!/bin/bash

set -e

# env
export ROS_DISTRO=humble

# bashrc
echo "alias omni_python='/isaac-sim/python.sh'" >>~/.bashrc

echo "source /opt/ros/$ROS_DISTRO/setup.bash" >>~/.bashrc

echo "export SIM_ASSETS=/root/assets" >>~/.bashrc
echo "export SIM_REPO_ROOT=/root/workspace/main" >>~/.bashrc

echo "export ROS_DISTRO=humble" >>~/.bashrc
echo "export ROS_LOCALHOST_ONLY=1" >>~/.bashrc

# you can add more customized cmds here

# setup ros2 environment
source "/opt/ros/$ROS_DISTRO/setup.bash" --
# exec "$@"

#
/bin/bash