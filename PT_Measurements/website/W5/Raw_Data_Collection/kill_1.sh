#!/bin/bash

kill $(ps aux | grep '[o]bfs4' | awk '{print $2}')
echo 'Killed PT_C_1'

sshpass -p <server-pass> ssh root@<server-ip> "kill \$(ps aux | grep '[o]bfs4' | awk '{print \$2}')"
echo 'Killed PT_S_1'
