This version of Camoufler requires five telegram IM accounts (i.e., five physical sims for authentication and getting OTPs while creating API tokens).

Camoufler Initial Setup(CIS)
----------------------
0. generate API-ID and API-HASH for five IM accounts using the below link
  https://my.telegram.org/auth
  
1. Note down usernames for each IM account; it will be used in different scripts to receive messages. 
 we will refer to each API-ID, API-HASH, and username like this -
  API-ID1, HASH-ID1, username1
  API-ID2, HASH-ID2, username2
  API-ID3, HASH-ID3, username3
  API-ID4, HASH-ID4, username4
  API-ID5, HASH-ID5, username5

Camoufler Server Setup(CSS)
----------------------

0. copy the complete "file_download_tg_socks_main" folder present in server-setup to your machine

1. replace API-ID, API-HASH, and usernames with the values obtained in CIS-0
  - make sure to perform the replacement carefully in every file of the folder; 
    for example in client_listener/mod_client_listener.py file replace <API-ID1>, <API-HASH1> and <username2> with values obtained in CIS-1

Note: Nothing needs to be done on the server anymore; the client will automatically issue commands to start different processes on the server using sshpass utility

Camoufler Client Setup(CCS)
----------------------

0. copy the complete "file_download_tg_socks_main" folder present in client-setup to your machine
$cd file_download_tg_socks_main

1. replace API-ID, API-HASH, and usernames with the values obtained in CIS-0
  - make sure to perform the replacement carefully in every file of the folder;
    for example in client_listener/mod_client_listener.py file replace <API-ID1>, <API-HASH1> and <username2> with values obtained in CIS-1

2. open start_camo.sh file 
  - replace <server-ip> and <server-pass> with the IP address and password of camoufler server machine
  - make sure that the path to all files in the shell file is correct

3. start client and server process using the shell script present in the folder
$./start_camo.sh

Test: Run the below command to test if it it able to download the content
$curl --socks5 127.0.0.1:9050 -o /dev/null https://www.wikipedia.com/
