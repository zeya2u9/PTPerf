#!/bin/bash

kill -9 $(lsof -t -i:9050)
kill -9 $(lsof -t -i:7080)
kill $(ps aux | grep '[r]elay' | awk '{print $2}')
echo 'KILLED_PT_C_10'
