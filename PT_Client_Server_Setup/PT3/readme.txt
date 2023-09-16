Shadowsocks server setup
------------------------

0. clone shadowsocks repository
$git clone https://github.com/shadowsocks/shadowsocks-libev.git
$cd shadowsocks-libev

1. add dependencies and build from source
$sudo apt-get install --no-install-recommends gettext build-essential autoconf libtool libpcre3-dev asciidoc xmlto libev-dev libc-ares-dev automake libmbedtls-dev libsodium-dev pkg-config
$./autogen.sh && ./configure && make
$sudo make install

It will add ss-local and ss-server binaries in /usr/local/bin/ folder of your machine

2. make a directory inside /etc with shadowsocks-libev name
$mkdir /etc/shadowsocks-libev

3. copy config.json file from server-setup folder to above folder
$cp config.json /etc/shadowsocks-libev/
 - replace <server-ip> with the IP address of your machine

4. start shadowsocks server using ss-server binary
$/usr/local/bin/ss-server -c /etc/shadowsocks-libev/config.json 

Now, the shadowsocks server is listening at port 8388 for client connections.



Shadowsocks client setup
-----------------------

0. clone shadowsocks repository
$git clone https://github.com/shadowsocks/shadowsocks-libev.git
$cd shadowsocks-libev

1. add dependencies and build from source
$sudo apt-get install --no-install-recommends gettext build-essential autoconf libtool libpcre3-dev asciidoc xmlto libev-dev li>
$./autogen.sh && ./configure && make
$sudo make install

It will add ss-local and ss-server binaries in /usr/local/bin/ folder of your machine

2. make a directory inside /etc with shadowsocks-libev name
$mkdir /etc/shadowsocks-libev

3. copy config.json from client-setup folder to /etc/shadowsocks-libev/ folder in your machine
   - replace <server-ip> with the IP of your shadowsocks server

4. start shadowsocks client
$/usr/local/bin/ss-local -c /etc/shadowsocks-libev/config.json
#client has connected to the server and is listening on 1080 port for local requests

5. copy torrc-shadow from client-setup folder to your machine and start the tor process. It will proxy all tor data to port 1080
$tor -f <path-to-torrc-shadow>
 

Test: to test if it is working, download any website using curl 
$curl --socks5 127.0.0.1:9050 -o /dev/null https://www.wikipedia.com/

NOTE:  The above steps are not the only way to set up shadowsocks. One can also follow different steps provided at https://github.com/shadowsocks  

