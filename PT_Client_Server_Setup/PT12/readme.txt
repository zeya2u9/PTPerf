Conjure Client setup
-----------------

0. Clone conjure repository
$git clone https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/conjure.git
$cd conjure

1. Install the necessary dependencies 
   i. setup latest Go version by following the steps mentioned at https://go.dev/doc/install
   ii. install libczmq library 
      $apt-get install libczmq-dev

2. Build Go module for conjure client
   $cd client
   $go build

3. copy torrc given in client_setup folder to your machine
  - replace <path-to-conjure-module> with its absolute path 

4. start conjure client
$tor -f <path-to-torrc>


