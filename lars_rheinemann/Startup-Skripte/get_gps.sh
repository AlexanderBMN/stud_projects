#!/bin/sh
# GPS Daten von OBU abholen
sshpass -p 'user' ssh -o StrictHostKeyChecking=no user@192.168.2.87 "gpspipe -r |  nc -u 192.168.2.6 51113"
