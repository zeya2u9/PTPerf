#!/bin/bash

cd /root/pTesting/ptadapter/
ptadapter -C ptadapter_c.ini &
sleep 2
ncat -v 127.0.0.1 3128 &
