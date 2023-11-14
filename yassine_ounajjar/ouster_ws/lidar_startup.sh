#!/bin/bash
# OS0 - 122116000117
# OS1 - 992111000483
# OS2 - 992111000489

# CAR
# OS0 LEFT - 122116000094 - 169.254.224.2
# OS0 RIGHT - 122116000117 - 169.254.112.236
# OS1 TOP - 122111000018	- 169.254.223.189

# Get IP address of Lidar
# ping os-122116000117.local -c 1 -q

# Lidar OS0 with Camera Setup 169.254.112.236
#gnome-terminal --command="bash -c 'source ~/Desktop/Marek_Leonie/ros_workspace/devel/setup.bash && \
#roslaunch ouster_ros ouster.launch sensor_hostname:=169.254.112.236 lidar_mode:=1024x20 viz:=false sensor_name:=OS0 \
#metadata:=$HOME/.ros/169.254.112.236.json'"

# workingDirectory="/home/ameise/Desktop/Marek_Leonie"
#workingDirectory="/home/yaouit/myworkspace/ameise_ws"

# Lidar OS0 169.254.224.2
gnome-terminal -- bash -c "source /home/ameise/Yassine_GIT/ouster_ws/devel/setup.bash && \
roslaunch ouster_ros ouster.launch sensor_hostname:=192.168.2.13 lidar_mode:=1024x20 viz:=false sensor_name:=OS0_RIGHT tf_prefix:=1 metadata:=/home/ameise/Yassine_GIT/192.168.2.13.json "

sleep 2
# Lidar OS1 169.254.141.135
gnome-terminal -- bash -c "source /home/ameise/Yassine_GIT/ouster_ws/devel/setup.bash && \
roslaunch ouster_ros ouster.launch sensor_hostname:=192.168.2.11 lidar_mode:=1024x20 viz:=false sensor_name:=OS0_LEFT tf_prefix:=2 metadata:=/home/ameise/Yassine_GIT/192.168.2.11.json"
#sleep 2

# Lidar OS2 169.254.86.233
#gnome-terminal -- bash -c "source /home/ameise/Yassine_GIT/ouster_ws/devel/setup.bash && \
#roslaunch ouster_ros ouster.launch sensor_hostname:=192.168.1.52 lidar_mode:=1024x10 viz:=false sensor_name:=OS1_TOP metadata:=/home/ameise/Yassine_GIT/192.168.1.52.json"
