#!/bin/bash


sshpass -p <server-pass> ssh root@<server-ip> "./psiphon-tunnel-core-binaries/start_11.sh > /dev/null 2>&1 & " &
sleep 3

cd /root/pTesting/psiphon-tunnel-core-binaries/linux/
./psiphon-tunnel-core-x86_64  -config ./client.config &
sleep 1
tor -f /etc/tor/torrc-psiphon
sleep 1
echo 'PSIPHON-CLIENT_Started'
