#!/bin/bash

#kill -9 $(lsof -t -i:9050)
kill -9 $(lsof -t -i:9011)
kill -9 $(lsof -t -i:9012)
kill -9 $(lsof -t -i:9013)
kill -9 $(lsof -t -i:9014)
kill -9 $(lsof -t -i:9015)
kill -9 $(lsof -t -i:9016)
kill -9 $(ps aux | grep '[a]lt_proxy_listener.py' | awk '{print $2}')
