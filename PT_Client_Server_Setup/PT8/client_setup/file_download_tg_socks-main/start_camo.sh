#!/bin/bash

cd file_download_tg_socks-main/client_listener
python3 mod_client_listener.py &
sleep 2
python3 mod_client_listener2.py &
echo '1-2-------'
sleep 7


sshpass -p <server-pass> ssh root@<server-ip> " python3  ~/file_download_tg_socks-main/server_int.py"&
echo '4-server started'
sleep 1

sshpass -p <server-pass> ssh root@<server-ip> " python3 ~/file_download_tg_socks-main/alt_proxy_listener/alt_proxy_listener.py "&
echo '5------'
sleep 1

cd file_download_tg_socks-main/
python3 int_client.py &
sleep 2
python3 camoufler_socks.py &
sleep 2

echo '::::::::::::all-process-started:::::::::'
