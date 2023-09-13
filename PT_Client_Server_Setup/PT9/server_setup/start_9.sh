#!/bin/bash

#iptables -I INPUT -p udp --dport 5300 -j ACCEPT
#iptables -t nat -I PREROUTING -i eth0 -p udp --dport 53 -j REDIRECT --to-ports 5300

cd /path/to/dnstt/dnstt-server/
tor -f torrc &
echo -e "\nstarted tor on server"
sleep 20

./dnstt-server -udp :5300 -privkey-file server.key t.ptransports.xyz 127.0.0.1:9001 &
# > /dev/null 2>&1" &
echo -e "started dnstt server"
