#!/bin/bash

kill -9 $(lsof -t -i:9050)
echo 'PT13_Tor Killed'
