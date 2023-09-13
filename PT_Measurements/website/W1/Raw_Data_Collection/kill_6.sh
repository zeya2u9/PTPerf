#!/bin/bash

kill $(ps aux | grep ' [t]or ' | awk '{print $2}')
echo 'Killed_PT_6'
