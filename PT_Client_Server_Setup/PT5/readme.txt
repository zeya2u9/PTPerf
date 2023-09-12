Cloak server setup
------------------

0. Clone Cloak respository
$git clone https://github.com/cbeuw/Cloak.git
$cd Cloak

1. satisfy dependencies --> setup latest go version by following steps in https://go.dev/doc/install

2. build cloak 
$go get ./...
$make

it will generate ck-client and ck-server binaries in build folder

3. generate public,private key pair and uid using below command
$build/ck-server -key
$build/ck-server -uid

Note:store the public key to share with clients

4. copy torrc-basic and ckserver.json from server-setup folder to your machine
 - replace <key> and <uid> in ckserver.json file with the respective values of key and uid genertaed in step-3

5. start tor and Cloack server
$tor -f <path-torrc-basic> 
$build/ck-server -c ckserver.json;


Cloak client setup
------------------

0. Clone Cloak respository
$git clone https://github.com/cbeuw/Cloak.git
$cd Cloak

1. satisfy dependencies --> setup latest go version by following steps in https://go.dev/doc/install

2. build cloak
$go get ./...
$make

it will generate ck-client and ck-server binaries in build folder

3. copy ckclient.json file from client-setup folder to your machine
 - replace <pub> and <uid> with the public key and uid of Cloak server

4. start Cloak client (replace <server-ip> with the IP address of cloak server)
$build/ck-client -c ckclient.json -s <server-ip>

Test: run below command and see it it able to download the content
$curl --socks5 127.0.0.1:1984 -o /dev/null https://www.wikipedia.com/

