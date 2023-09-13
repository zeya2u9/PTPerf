#!/bin/bash

kill $(ps aux | grep '[m]od_client_listener.py' | awk '{print $2}')
kill $(ps aux | grep '[m]od_client_listener2.py' | awk '{print $2}')
kill $(ps aux | grep '[i]nt_client.py' | awk '{print $2}')
kill $(ps aux | grep '[c]amoufler_socks.py' | awk '{print $2}')
echo 'Killed PT_C_8'

kill $(ps aux | grep ' [t]or ' | awk '{print $2}')
kill $(ps aux | grep '[s]erver_int.py' | awk '{print $2}')
kill $(ps aux | grep '[a]lt_proxy_listener.py' | awk '{print $2}')
echo 'Killed PT_S_8'
