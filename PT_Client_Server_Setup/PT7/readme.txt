Meek Client setup
-----------------

0. Clone meek repository
$git clone https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/meek.git
$cd meek

1. Install the necessary dependencies --> setup latest Go version by following the steps at https://go.dev/doc/install

2. Build Go module for meek client
$cd meek-client
$go build

3. copy torrc given in client_setup folder to your machine
  - replace <path-to-meek-module> with its absolute path 

4. start meek client
$tor -f <path-to-torrc>


Note: The provided meek-torrc uses one of the Tor-provided meek bridgeline; one can replace the meek bridge details with any other Tor-provided bridge 
