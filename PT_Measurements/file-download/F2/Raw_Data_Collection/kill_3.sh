#!/bin/bash

kill $(ps aux | grep '[s]s-local' | awk '{print $2}')
kill $(ps aux | grep '[t]or' | awk '{print $2}')
echo 'killed PT_C_3'

sshpass -p  <server-pass> ssh root@<server-ip> "kill \$(ps aux | grep '[s]s-server' | awk '{print \$2}')"
echo 'killed PT_S_3'
