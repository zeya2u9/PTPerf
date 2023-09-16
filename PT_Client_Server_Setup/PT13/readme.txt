WebTunnel Server Setup
----------------------

0. Clone webTunnel repository and build it
$git clone https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/webtunnel.git
$cd webtunnel/main/server
$go mod init server
$go mod tidy
$go build

-It will create a Go module named "server".

-copy the server module from server-setup folder to /var/lib/torwebtunnel folder
$mkdir /var/lib/torwebtunnel
$cp server /var/lib/torwebtunnel/webtunnel

-copy the torrc from server-setup folder to /var/lib/torwebtunnel folder
  - replace <url-of-nginx-server> with the webiste url that will be hosted in the next few steps using nginx 

-copy webTunnel.service file from server-setup folder to /etc/systemd/system/ [this step is run webTunnel as a service in the background]

1. website setup and hosting steps using nginx

-install nginx
$apt-get install nginx-full -y
$systemctl stop nginx

$apt-get install socat -y
$curl https://get.acme.sh | sh -s email=<provide-your-email-id>
#change SERVER_ADDRESS with the ip of current machine
#if your IP is a.b.c.d, then set SERVER_ADDRESS = a-b-c-d 
$~/.acme.sh/acme.sh --set-default-ca --server letsencrypt --issue --standalone --domain $SERVER_ADDRESS.sslip.io
#copy fullchain certificate from above produced path to /etc/nginx/ssl/
$mkdir /etc/nginx/ssl/
$cp /root/.acme.sh/$SERVER_ADDRESS.sslip.io_ecc/$SERVER_ADDRESS.sslip.io.key /etc/nginx/ssl/key.key
$cp /root/.acme.sh/$SERVER_ADDRESS.sslip.io_ecc/fullchain.cer /etc/nginx/ssl/fullchain.cer

-copy nginx.conf file from server-setup folder to the below folder
$cd /etc/nginx/

-copy default_server file from server-setup folder and copy it to the below folder
$mkdir /etc/nginx/sites-enabled -p
$cd /etc/nginx/sites-enabled/
$rm default
 - replace <ip-of-this-machine> with the IP of your machine in the default_server file

2. Start nginx and webtunnel service

$systemctl daemon-reload
$systemctl start nginx.service
$systemctl status nginx.service
--check if <https://$SERVER_ADDRESS.sslip.io> is accessible in browser; it will confirm the website setup part

$systemctl start webTunnel.service
$systemctl status webTunnel.service
#instead of running a webTunnel service, one can also run the below line to start the webtunnel server
$tor -f /var/lib/torwebtunnel/torrc



WebTunnel Client Setup
----------------------

0. Clone webTunnel repository
$git clone https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/webtunnel.git
$cd webtunnel

1. satisfy dependencies
   - setup latest Go version by following the steps in https://go.dev/doc/install

2. Build Go module for webTunnel client
$cd main/client
$go build

3. copy torrc from client_setup folder to your machine
   - replace <path-to-webtunnel-module> with its absolute path
   - replace <ip-of-webTunnel-server> with the IP address of your webTunnel server 
   - replace <url-of-website-hosted-at-server-side> with the url of the website hosted at webTunnel server side  

4. start webTunnel client
$tor -f <path-to-torrc>

NOTE: The above steps are not the only way to set up webtunnel. One can also follow the steps provided on https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/webtunnel
