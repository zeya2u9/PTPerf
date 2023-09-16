#!/bin/bash


sshpass -p <server-pass> ssh root@<server-ip> "cd && ./root/dnstt/dnstt-server/killer.sh > /dev/null 2>&1" > /dev/null 2>&1
sshpass -p <server-pass> ssh root@<server-ip> "kill \$(ps aux | grep '[d]nstt' | awk '{print \$2}')"
sshpass -p <server-pass> ssh root@<server-ip> "kill \$(ps aux | grep '[t]or ' | awk '{print \$2}')"

echo -e "KILLED dnstt-server and tor on server"

kill -9 $(lsof -t -i:9050) > /dev/null 2>&1
kill -9 $(ps aux | grep "dnstt" | awk 'NR==1{print $2}') > /dev/null 2>&1
kill -9 $(ps aux | grep "dnstt" | awk 'NR==1{print $2}') > /dev/null 2>&1
echo -e "KILLED dnstt-client and tor on client"
echo "done"
