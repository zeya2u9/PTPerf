Marionette Server Setup
-----------------------

0. Clone marionette repository
$ git clone https://github.com/marionette-tg/marionette.git
$ cd marionette

1. setup a virtual environment for python 2.7 and activate it
$sudo apt install python2 virtualenv
$virtualenv -p python2.7 mario
$source mario/bin/activate

2. add dependencies and build marionette
$sudo apt-get install git libgmp-dev python-dev curl
#remove regex2dfa from requirements.txt, it needs some correction then building from its source
$sudo pip install -r requirements.txt
$python setup.py build
$sudo python setup.py install

One fix: regex2dfa must be built from its modified source since it contains some error in its replace.h file present in "regex2dfa/third_party/openfst/src/include/fst/replace.h"
         - change in line 1253 ->template CacheBaseImpl<typename   to ->CacheBaseImpl<typename
$git clone https://github.com/kpdyer/regex2dfa.git
$cd /regex2dfa/third_party/openfst/src/include/fst
$vi replace.h
#make changes and save it
$./configure
$make

3. copy torrc-basic from server-setup folder to your machine 

4. start marionette server 
#replace <server-ip> with the IP address of the machine
$tor -f /etc/tor/torrc-basic 
$./bin/marionette_server --server_ip <server-ip> --proxy_ip 127.0.0.1 --proxy_port 8081 --format dummy&


Marionette Client Setup
----------------------

0. Clone marionette repository
$ git clone https://github.com/marionette-tg/marionette.git
$ cd marionette

1. setup a virtual environment for python 2.7 and activate it
$sudo apt install python2 virtualenv
$virtualenv -p python2.7 mario
$source mario/bin/activate

2. add dependencies and build marionette
$sudo apt-get install git libgmp-dev python-dev curl
#remove regex2dfa line from requirements.txt
$sudo pip install -r requirements.txt
$python setup.py build
$sudo python setup.py install

One fix: regex2dfa must be built from its modified source since it contains some error in its replace.h file present in "regex2dfa/third_party/openfst/src/include/fst/replace.h"
         - change in line 1253 ->template CacheBaseImpl<typename   to ->CacheBaseImpl<typename
$git clone https://github.com/kpdyer/regex2dfa.git
$cd /regex2dfa/third_party/openfst/src/include/fst
$vi replace.h
#make changes and save it
$./configure
$make

3. start marionette client
#replace <server-ip> with the IP address of the machine
$./bin/marionette_client --server_ip <server-ip> --client_ip 127.0.0.1 --client_port 8079 --format dummy&

Test: run the below command and test if it it able to download the content
$curl --socks5 127.0.0.1:8079 -o /dev/null https://www.wikipedia.com/
