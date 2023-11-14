#!/bin/sh
sshpass -p 'user' ssh -o StrictHostKeyChecking=no user@192.168.2.87 "cd /mnt/rw/exampleETSI; ./rc.exampleETSI start obu"
