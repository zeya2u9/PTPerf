#!/bin/bash

kill $(ps aux | grep '[s]tegotorus' | awk '{print $2}')
echo 'Killed PT_C_4'

sshpass -p <server-pass> ssh root@<server-ip> "kill \$(ps aux | grep '[s]tegotorus' | awk '{print \$2}')"
sshpass -p <server-pass> ssh root@<server-ip> "kill \$(ps aux | grep '[t]or' | awk '{print \$2}')"
echo 'Killed PT_S_4'
