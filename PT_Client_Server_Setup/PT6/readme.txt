Snowflake Client setup
-----------------

0. Clone snowflake repository
$git clone https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/snowflake.git
$cd snowflake

1. Install the required dependencies --> setup latest Go version by following the steps at https://go.dev/doc/install

2. Build Go module for snowflake client
$cd client
$go build

3. copy torrc given in client_setup folder to your machine
  - replace <path-to-snowflake-module> with its absolute path 

4. Start snowflake client
$tor -f <path-to-torrc>


Note: The provided torrc uses one of the Tor-provided snowflake bridgeline; one can replace the snowflake bridge details with any other Tor-provided bridge 
