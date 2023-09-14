#!/bin/bash

source deactivate
kill $(ps aux | grep '[m]ario' | awk '{print $2}')
echo 'killed PT_C_2'

sshpass -p <server-pass> ssh root@<server-ip> "kill \$(ps aux | grep '[m]arionette_server' | awk '{print \$2}')"
sshpass -p <server-pass> ssh root@<server-ip> "kill \$(ps aux | grep '[s]ocksserver' | awk '{print \$2}')"
sshpass -p <server-pass> ssh root@<server-ip> "kill \$(ps aux | grep '[t]or' | awk '{print \$2}')"
echo 'killed PT_S_2'
