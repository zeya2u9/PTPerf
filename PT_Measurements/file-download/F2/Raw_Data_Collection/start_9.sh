#!/bin/bash

sshpass -p <server-pass> ssh root@<server-ip> "./dnstt/start_9.sh > /dev/null 2>&1 & " &
#echo -e "\ns
sleep 25


cd /root/dnstt/dnstt-client/
echo -e "entering dnstt-client directory"

./dnstt-client -doh https://doh.opendns.com/dns-query -pubkey-file server.pub t.ptransports.xyz 127.0.0.1:7000 > /dev/null 2>&1 & 
echo -e "started dnstt client in bg"
sleep 5

tor -f /root/dnstt/dnstt-client/torrc > /dev/null 2>&1 &
echo -e "started tor on client"

echo -e "dnstt ready to run\n"
echo -e "you can use command:\ncurl --proxy socks5://127.0.0.1:9050/ https://ifconfig.me/\nto verify if dnstt is functional"
