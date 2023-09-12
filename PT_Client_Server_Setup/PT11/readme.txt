Psiphon Server Setup
--------------------

0. Clone psiphon repository
$git clone https://github.com/Psiphon-Labs/psiphon-tunnel-core-binaries.git
$cd psiphon-tunnel-core-binaries

1. generate server configuration data
$cd psiphond 
$./psiphond -ipaddress <server-ip> -protocol OSSH:9999 generate

 - it creates a server-entry.dat file, it will be used at client side

3. start psiphon server
$cd psiphond/
$./psiphond run


Psiphon Client Setup
--------------------

0. Clone psiphon repository
$git clone https://github.com/Psiphon-Labs/psiphon-tunnel-core-binaries.git
$cd psiphon-tunnel-core-binaries

1. copy the client.config file from client-setup folder to your machine 
   - replace <server-entry> with the contents of server-entry.dat (present at the server side) to the TargetServerEntry field.

2. copy torrc-psiphon from client-setup folder to your machine

3. start psiphon client and tor process 
$cd linux/
$./psiphon-tunnel-core-x86_64  -config ./client.config &
$tor -f <path-to-torrc-psiphon>
#tor will proxy all its data to the psiphon client process listening at port 1080

Test: run below command and see it it able to download the content
$curl --socks5 127.0.0.1:9050 -o /dev/null https://www.wikipedia.com/
