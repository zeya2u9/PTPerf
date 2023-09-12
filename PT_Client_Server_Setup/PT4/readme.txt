Stegotorus server setup
-----------------------

0. Clone stegotorus repository
$git clone https://github.com/TheTorProject/stegotorus.git
$cd stegotorus

1. add dependencies anf build from source
$sudo apt-get install build-essential git automake autoconf pkg-config libssl-dev libevent-dev libcurl4-openssl-dev libyaml-cpp-dev zlib1g-dev libboost-dev libboost-system-dev libboost-filesystem-dev
$autoreconf -i
$ ./configure [--without-boost]
$ sudo make

2. start stegotorus server (<server-ip> : replace it with the IP of your machine)
$./stegotorus --log-min-severity=debug --timestamp-logs chop server --passphrase "correct passphrase" --trace-packets --disable-retransmit 127.0.0.1:9050 nosteg_rr <server-ip>:5000 &

3. copy torrc-basic from server-setup folder and run tor process
$tor -f /etc/tor/torrc-basic

Stegotorus client setup
-----------------------

0. Clone stegotorus repository
$git clone https://github.com/TheTorProject/stegotorus.git
$cd stegotorus

1. add dependencies anf build from source
$sudo apt-get install build-essential git automake autoconf pkg-config libssl-dev libevent-dev libcurl4-openssl-dev libyaml-cpp-dev zlib1g-dev libboost-dev libboost-system-dev libboost-filesystem-dev
$autoreconf -i
$ ./configure [--without-boost]
$ sudo make

2. start stegotorus client (<server-ip> : replace it with the IP of stegortorus server)
$./stegotorus --log-min-severity=debug --timestamp-logs chop client --passphrase "correct passphrase" --trace-packets --disable-retransmit 127.0.0.1:5001 nosteg_rr 134.122.113.191:5000

Test: run below command and see it it able to download the content
$curl --socks5 127.0.0.1:5001 -o /dev/null https://www.wikipedia.com/
