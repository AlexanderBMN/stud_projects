#!/bin/sh
# launcher für die GUI
cd /
cd /home/Documents/SPAT
echo "establishing connection to obu"
sh start_etsi.sh &
sleep 10
sh start_netcat.sh &
sh get_gps.sh &
sh get_pcap.sh &
python3 gui.py
echo "killing all scripts"
pkill -fx 'nc -u -v -l -n 51113'
pkill -f get_gps.sh
pkill -f get_pcap.sh
cd /

