#!/bin/bash

cd /root/marionette/
source /root/anaconda2/envs/formari/bin/activate formari
./bin/marionette_client --server_ip <server-ip> --client_ip 127.0.0.1 --client_port 8079 --format dummy &
