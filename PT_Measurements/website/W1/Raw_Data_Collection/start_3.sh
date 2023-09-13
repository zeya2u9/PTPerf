#!/bin/bash


sleep 1
/usr/bin/ss-local -c /etc/shadowsocks-libev/config.json &
sleep 2
tor -f /etc/tor/torrc-shadow
sleep 10
