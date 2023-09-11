Tor client setup
----------------

1. Build tor-0.4.7.13 (or any latest version) from its source [https://github.com/torproject/tor/releases/tag/tor-0.4.7.13]
Steps -  
$wget https://github.com/torproject/tor/archive/refs/tags/tor-0.4.7.13.tar.gz  
$tar -xvzf https://github.com/torproject/tor/archive/refs/tags/tor-0.4.7.13.tar.gz  
$cd tor-0.4.7.13  
$autoreconf -fi  
$./configure --disable-asciidoc  
$sudo make  
$sudo make install  

2. copy the torrc provided in this folder to your machine OR use default torrc provided by Tor

3. Start Tor process 
$tor -f <path-to-torrc>

4. Example to download a website using tor
$curl --socks5 127.0.0.1:9050 <website-url> -o <output-file>
