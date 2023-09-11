Obfs4 server setup
------------------

0. Clone obfs4 repository
$git clone https://github.com/Yawning/obfs4.git
$cd obfs4

1. satisfy dependencies --> setup latest go version by following steps in https://go.dev/doc/install

2. Build go module for obfs4 client; it will make a obfs4proxy module in obfs4/obfs4proxy/ folder
$go build -o obfs4proxy/obfs4proxy ./obfs4proxy


3. copy torrc given in server_setup folder to your machine
  - replace <path-to-obfs4proxy-module> with its absolute path
  - replace <ip-of-the-machine> with your machine's IP-adddress

4. Start obfs4 bridge
$tor -f <path-to-torrc>

Hint:If it bootstarps to 100%, that means its working.

In case you do not want to setup your own bridge, use tor-provided Obfs4 bridgeline in your client-torrc- 
obfs4 193.11.166.194:27015 2D82C2E354D531A68469ADF7F878FA6060C6BACA cert=4TLQPJrTSaDffMK7Nbao6LC7G9OW/NHkUwIdjLSS3KYf0Nv4/nQiiI8dY2TcsQx01NniOg iat-mode=0


Obfs4 client setup
------------------

0. Clone obfs4 repository
$git clone https://github.com/Yawning/obfs4.git
$cd obfs4

1. satisfy dependencies --> setup latest Go version by following steps in https://go.dev/doc/install

2. Build go module for obfs4 client
$go build -o obfs4proxy/obfs4proxy ./obfs4proxy

3. copy torrc given in client_setup folder
  - replace <path-to-obfs4proxy-module> with its absolute path
  - EITHER copy bridgeline from obfs4/datadir/pt_state/obfs4_bridgeline.txt from your obfs4-server (bridge) machine; then paste the copied line to client side torrc <bridge-line>. OR use Tor provided obfs4 bridge line e.g., "obfs4 193.11.166.194:27015 2D82C2E354D531A68469ADF7F878FA6060C6BACA cert=4TLQPJrTSaDffMK7Nbao6LC7G9OW/NHkUwIdjLSS3KYf0Nv4/nQiiI8dY2TcsQx01NniOg iat-mode=0"

4. start Obfs4 client
$tor -f <path-to-torrc>



Side Note1:we used obfs4 before it became lyrebird by Tor Project (https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/lyrebird).
Side Note2: You can also setup obfs4 client and server by following the steps present in the readme of obfs4 repository instead of following above steps  
Obfs4 - https://github.com/Yawning/obfs4.git

