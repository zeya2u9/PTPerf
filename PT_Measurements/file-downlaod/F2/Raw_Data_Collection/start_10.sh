#!/bin/bash

cd /root/pTesting/MassBrowser/
yarn run relay:dev &
yarn run client:dev &
tor -f /etc/tor/torrc-mass &
#


echo 'STARTED_MassBrowser' 


