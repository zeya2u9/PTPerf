#!/bin/bash

kill -9 $(lsof -t -i:9011)
kill -9 $(lsof -t -i:9012)
kill -9 $(lsof -t -i:9013)
kill -9 $(lsof -t -i:9016)
echo 'Killed PT_C_8'

sshpass -p  <server-pass> ssh root@<server-ip> "kill -9 \$(lsof -t -i:9050)"
sshpass -p  <server-pass> ssh root@<server-ip> "kill -9 \$(lsof -t -i:9014)" 
sshpass -p  <server-pass> ssh root@<server-ip> "kill -9 \$(lsof -t -i:9015)"
sshpass -p  <server-pass> ssh root@<server-ip> "kill -9 \$(ps aux | grep '[a]lt_proxy_listener.py' | awk '{print \$2}')"
echo 'Killed PT_S_8'
