dnstt Nameserver Records Setup
------------------------------

// buy a domain (on namecheap, porkbun, etc.)
// add your dnstt server's IP as a custom nameserver for a subdomain of your domain, say t.<domain>.xyz (keep a short subdomain like 't' or 'a') and add an NS record for that subdomain (for example ns1.<domain>.xyz) and an A record for this NS record. This A record will have the IP of your dnstt server.

// (for more hints follow, see https://www.bamsoftware.com/software/dnstt/)

General Instructions
--------------------

- git clone https://www.bamsoftware.com/git/dnstt.git
// (on both the client and server side)
- cd ./dnstt/dnstt-<client/server>

- go build (both sides)

Server Setup
------------

- ./dnstt-server -gen-key -privkey-file server.key -pubkey-file server.pub
- scp ./server.pub <client-user>@<client-ip>:/path/to/dnstt-client/

- sudo iptables -I INPUT -p udp --dport 5300 -j ACCEPT
- sudo iptables -t nat -I PREROUTING -i eth0 -p udp --dport 53 -j REDIRECT --to-ports 5300

- vim /etc/tor/torrc
// uncomment #ORPort 9001 and save
- tor -f /etc/tor/torrc
- ./dnstt-server -udp :5300 -privkey-file server.key t.ptransports.xyz 127.0.0.1:9001

Client Setup
------------

- vim /etc/tor/torrc
// uncomment - SocksPort 9050
// add line - UseBridges 1
// add line - Bridge 127.0.0.1:7000
// save and exit 
- ./dnstt-client -doh https://doh.opendns.com/dns-query -pubkey-file server.pub t.ptransports.xyz 127.0.0.1:7000
- tor -f /etc/tor/torrc
- curl --proxy socks5://127.0.0.1:9050/ https://ifconfig.me/

Running dnstt
-------------
// For convenience, there are two scripts (for client and server, respectively) to execute the starting commands automatically; these scripts are in the server_setup and client_setup folders
// Please add the appropriate details in these scripts before trying to run them.

---------------------------------------------------------------------------------------------
