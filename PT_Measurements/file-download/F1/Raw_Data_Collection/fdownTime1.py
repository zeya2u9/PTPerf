import os 
import time
import pandas as pd

#Tor - 0
paths_0 = ''
pathc_0 = 'tor -f /etc/tor/torrc-basic &'

#obfs4 - 1
#obfs4 server side
paths_1 = '' 
pathc_1 = 'tor -f /etc/tor/obfs4_torrc &' #'./pt_c.sh'

#shadowsocks - 3
#server-side
paths_3 = "sshpass -p <server-pass> ssh root@<server-ip>  '/usr/bin/ss-server -c /etc/shadowsocks-libev/config.json &'" #server proxy listens at tcp port 8388
#client-side
pathc_3 = 'tor -f /etc/tor/torrc-shadow & /usr/bin/ss-local -c /etc/shadowsocks-libev/config.json &' #client-proxy listens at tcp port 1080

#marionette - 2
#server-side
paths_2 = "sshpass -p <server-pass> ssh root@<server-ip> './marionette/start2.sh'"
#client-side
pathc_2 = './pt_mar.sh'

#stegotorus - 4
#server-side
paths_4 = "sshpass -p <server-pass> ssh root@<server-ip> './stegotorus/startn.sh'"
#client-side
pathc_4 = 'cd /root/stegotorus/; ./stegotorus --log-min-severity=debug --timestamp-logs chop client --passphrase "correct passphrase" --trace-packets --disable-retransmit 127.0.0.1:5001 nosteg_rr <server-ip>:5000 &'

#Cloak - 5
#server-side
paths_5 = "sshpass -p <server-pass> ssh root@<server-ip> 'cd /root/Cloak/ && { tor -f /etc/tor/torrc-basic & build/ck-server -c ckserver.json; } &'"
#client-side
pathc_5 = "cd /root/Cloak/ && build/ck-client -c ckclient.json -s <server-ip> &"

#Snowflake - 6
paths_6 = ''
pathc_6 = 'tor -f /etc/tor/snowflake_client_torrc &'

#Meek - 7
paths_7 = ''  #server-side
pathc_7 = 'cd /root/meek/meek-client/; tor -f /etc/tor/meek_torrc &' #client-side

#Camoufler - 8
paths_8 = 'cd /root/file_download_tg_socks-main/; ./start_camo.sh'
pathc_8 = 'echo Done'

#Dnstt - 9
paths_9 = 'echo "Done"'
pathc_9 = './start_9.sh'

#Psiphon - 11
paths_11 = ''
pathc_11 = './start_11.sh'


#conjure -12
paths_12 = ''
pathc_12 = 'tor -f /etc/tor/torrc &'

#webtunnel - 13
paths_13 = "sshpass -p <server-pass> ssh root@<server-ip>  'systemctl restart webTunnel.service &'"
pathc_13 = 'cd /root/webtunnel/main/client/; tor -f /etc/tor/torrc-webtunnel &'


#--------------------server commands for PTs--------------------------------
server = [ paths_0, paths_1, paths_2, paths_3,  paths_4, paths_5, paths_6, paths_7, paths_8, paths_9, paths_11, paths_12, paths_13]

#--------------------server commands for PTs--------------------------------
client = [ pathc_0, pathc_1, pathc_2, pathc_3, pathc_4, pathc_5, pathc_6, pathc_7, pathc_8, pathc_9, pathc_11, pathc_12,  pathc_13]

#--------------------Operation list----------------------------------------
operation_f = [ 'curl --socks5 127.0.0.1:9050 --max-time 7200 -o /dev/null -w "Size_of_downloaded_file: %{size_download} Download_speed_Bps: %{speed_download} Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" ',
		'curl --socks5 127.0.0.1:9050 --max-time 7200 -o /dev/null -w "Size_of_downloaded_file: %{size_download} Download_speed_Bps: %{speed_download} Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" ',
	        'curl --socks4a 127.0.0.1:8079 --max-time 7200 -o /dev/null -w "Size_of_downloaded_file: %{size_download} Download_speed_Bps: %{speed_download} Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" ',
		'curl --socks5 127.0.0.1:9050 --max-time 7200 -o /dev/null -w "Size_of_downloaded_file: %{size_download} Download_speed_Bps: %{speed_download} Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" ',
		'curl -x socks4://127.0.0.1:5001 --max-time 7200 -o /dev/null -w "Size_of_downloaded_file: %{size_download} Download_speed_Bps: %{speed_download} Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" ',
		'curl --socks5 127.0.0.1:1984 -o /dev/null --max-time 7200 -w "Size_of_downloaded_file: %{size_download} Download_speed_Bps: %{speed_download} Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" ',
		'curl --socks5 127.0.0.1:9050 --max-time 7200 -o /dev/null -w "Size_of_downloaded_file: %{size_download} Download_speed_Bps: %{speed_download} Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" ',
		'curl --socks5 127.0.0.1:9050 --max-time 7200 -o /dev/null -w "Size_of_downloaded_file: %{size_download} Download_speed_Bps: %{speed_download} Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" ',
		'curl -v --socks5 127.0.0.1:9011 --max-time 7200 -o /dev/null -k -w "Size_of_downloaded_file: %{size_download} Download_speed_Bps: %{speed_download} Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" ',
		'curl --proxy socks5://127.0.0.1:9050/ --max-time 7200 -o /dev/null -k -w "Size_of_downloaded_file: %{size_download} Download_speed_Bps: %{speed_download} Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" ',
		'curl --socks5 127.0.0.1:9050 --max-time 7200 -o /dev/null -w "Size_of_downloaded_file: %{size_download} Download_speed_Bps: %{speed_download} Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" ',
		'curl --socks5 127.0.0.1:9050 --max-time 7200 -o /dev/null -w "Size_of_downloaded_file: %{size_download} Download_speed_Bps: %{speed_download} Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" ',
		'curl --socks5 127.0.0.1:9050 --max-time 7200 -o /dev/null -w "Size_of_downloaded_file: %{size_download} Download_speed_Bps: %{speed_download} Connect: %{time_connect} TTFB: %{time_starttransfer} Total time: %{time_total} \n" ']

#--------------------List of files-----------------------------------------
data3 = pd.read_csv('/root/fDownload.csv')
files = data3.iloc[0:5, 1]

#-------------------kill-pt-process----------------------------------------
kill_pt = ['./kill_0.sh', './kill_1.sh', './kill_2.sh', './kill_3.sh', './kill_4.sh', './kill_5.sh', './kill_6.sh', './kill_7.sh', './kill_8.sh','./kill_9.sh', './kill_11.sh','./kill_12.sh', './kill_13.sh']

#--------------------Executing PT's-----------------------------------------
print('::Executing PTs for Curl command')
for x in range(5):
	print(f'::Iteration No: {x+1}------------------------------------------')
	op = 0
	for i,j,l in zip(server, client, kill_pt):
		print('Starting Server: ', i)
		#os.system("sshpass -p pT@123pt ssh root@134.122.113.191 " + '$i')
		os.system(i + '&')
		print('Server: Done\n')
		
		time.sleep(5)
		print('Starting Client:', j)
		os.system(j)
		print('Client: Done\n')
		
		time.sleep(6)
		if op==6:
			print('Meek takes time in bootstrapping::\n')
			time.sleep(40)
		fname = ['new_pt1.txt','new_pt2.txt','new_pt3.txt', 'new_pt4.txt', 'new_pt5.txt','new_pt6.txt','new_pt7.txt', 'new_pt8.txt', 'new_pt9.txt', 'new_pt11.txt', 'new_pt12.txt', 'new_pt13.txt']
		os.system('echo ' + str(op) + ' >> ' + fname[op])
		##Download operation
		for m in files:
			print('File:: ', m, '\nOperation:: ',operation_f[op])
			os.system('echo ' + m + ' >> ' +  fname[op])
			os.system(operation_f[op] + m + ' >> ' + fname[op])
			if op == 7:
				print('::Camoufler needs to be rebooted')
				os.system(l)
				time.sleep(2)
				os.system(i+'&')
				time.sleep(5)
		#kill this  PT
		os.system(l)
		#ch = input('Continue with next PT? y[1]/n[0]: ')
		op = op + 1
		#if ch=='0':
		#	break
	os.system(f'mkdir -p result_file{x+1}')
	os.system(f'mv new_pt*.txt result_file{x+1}/')
print('----------------------------Execution over--------------------------')
