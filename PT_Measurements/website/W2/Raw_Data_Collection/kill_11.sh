#!/bin/bash

kill -9 $(lsof -t -i:9050) > /dev/null 2>&1
kill -9 $(ps aux | grep "psiphon" | awk 'NR==1{print $2}') > /dev/null 2>&1

echo -e "PTC_11_KILLED"

sshpass -p  <server-pass> ssh root@<server-ip> "kill \$(ps aux | grep '[p]siphon' | awk '{print \$2}')"
echo -e "PTS_11_KILLED"
