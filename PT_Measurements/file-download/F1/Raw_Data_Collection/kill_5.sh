#!/bin/bash

kill $(ps aux | grep '[c]k-client' | awk '{print $2}')
echo 'killed PT_C_5'

sshpass -p <server-pass> ssh root@<server-ip> "kill \$(ps aux | grep '[c]k-server' | awk '{print \$2}')"
sshpass -p <server-pass> ssh root@<server-ip> "kill \$(ps aux | grep '[t]or' | awk '{print \$2}')"
echo 'killed PT_S_5'
