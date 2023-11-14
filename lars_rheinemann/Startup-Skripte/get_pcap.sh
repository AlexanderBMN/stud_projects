#!/bin/sh
sshpass -p 'user' ssh -o StrictHostKeyChecking=no user@192.168.2.87 "sudo llc rcap --HdrLen 52 --Interface cw-mon-rxa --Meta --RemoteHost 192.168.2.6 --RemotePort 51112"
