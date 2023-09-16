Cloak server setup
------------------

0. Clone Cloak repository
$git clone https://github.com/cbeuw/Cloak.git
$cd Cloak

1. satisfy dependencies --> setup latest go version by following the steps in https://go.dev/doc/install

2. build cloak 
$go get ./...
$make

It will generate ck-client and ck-server binaries in the build folder.

3. generate public-private key pair and uid using the below command
$build/ck-server -key
$build/ck-server -uid

Note: store the public key to share with clients

4. copy torrc-basic and ckserver.json from server-setup folder to your machine
 - replace <key> and <uid> in ckserver.json file with the respective values of key and uid generated in step-3

5. start tor and Cloack server
$tor -f <path-torrc-basic> 
$build/ck-server -c ckserver.json;


Cloak client setup
------------------

0. Clone Cloak repository
$git clone https://github.com/cbeuw/Cloak.git
$cd Cloak

1. satisfy dependencies --> setup latest go version by following the steps in https://go.dev/doc/install

2. build cloak
$go get ./...
$make

It will generate ck-client and ck-server binaries in the build folder.

3. copy ckclient.json file from client-setup folder to your machine
 - replace <pub> and <uid> with the public key and uid of cloak server

4. start Cloak client (replace <server-ip> with the IP address of cloak server)
$build/ck-client -c ckclient.json -s <server-ip>

Test: run the below command and test if it it able to download the content
$curl --socks5 127.0.0.1:1984 -o /dev/null https://www.wikipedia.com/

