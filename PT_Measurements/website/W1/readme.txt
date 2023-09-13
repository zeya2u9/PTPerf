Curl-based experiments
----------------------

There are two folders -
1. Raw_Data_Collection: 
   - It contains scripts to start the measurement process for each PT. We have followed a common nomenclature for file names and folder names for storing the measurement results. 
   - File-name format: n-trf-tr<pt-number>.txt; for example n-trf-tr0.txt represents results for Tor-only.  
   - Folder structure: Throughout the measurement at one location we repeat each website download five times, thsu there are five folders. 
	<[server_location]-[client_location]>
		blocked
			result_web1 -> n-trf-tr0.txt, n-trf-tr1.txt, ...... , n-trf-tr13.txt
			result_web2 -> n-trf-tr0.txt, n-trf-tr1.txt, ...... , n-trf-tr13.txt
			result_web3 -> n-trf-tr0.txt, n-trf-tr1.txt, ...... , n-trf-tr13.txt
			result_web4 -> n-trf-tr0.txt, n-trf-tr1.txt, ...... , n-trf-tr13.txt
			result_web5 -> n-trf-tr0.txt, n-trf-tr1.txt, ...... , n-trf-tr13.txt
		tranco
                        result_web1 -> n-trf-tr0.txt, n-trf-tr1.txt, ...... , n-trf-tr13.txt
                        result_web2 -> n-trf-tr0.txt, n-trf-tr1.txt, ...... , n-trf-tr13.txt
                        result_web3 -> n-trf-tr0.txt, n-trf-tr1.txt, ...... , n-trf-tr13.txt
                        result_web4 -> n-trf-tr0.txt, n-trf-tr1.txt, ...... , n-trf-tr13.txt
                        result_web5 -> n-trf-tr0.txt, n-trf-tr1.txt, ...... , n-trf-tr13.txt
     server_location = {fra,nyc,sgp}
     client_location = {blr,lon,tor} 
   - Each file contains measurements in the following format -
	......
	https://www.youtube.com/
	Size_of_downloaded_file: xx Download_speed_Bps: xx.xx Connect: xx.xx TTFB: xx.xx Total time: xx.xx
        https://www.facebook.com/
        Size_of_downloaded_file: xx Download_speed_Bps: xx.xx Connect: xx.xx TTFB: xx.xx Total time: xx.xx
	.......
   - starting the measurements -
	- copy all files from this folder
	- replace <server-pass>, <server-ip> with PT server's password and IP addresses in curlTime.py, kill_<0-13>.sh, start_<x>.sh files
	- copy websiteList folder to your machine; it contains tranco and blocked list
	- select <website_tr20>(tranco) or <website_url>(blocked) in the code's innermost loop  
	- make sure all paths to tranco list and blocked list are correct in curlTime.py
	- start the measurement (MOT) - 
	$python3 curlTime1.py  //for tranco-1000
	- once above is excuted successfully; change the type of website (<website_tr20>(tranco) or <website_url>(blocked)) to start measurement
	$python3 curlTime1.py  //for blocked-1000
   - Repeat above steps at each location you want to perform the measurement and save results.

2. Raw_Data_Processing: it contains scripts which will process the raw data obtained from step-1
   - To apply processing scripts over the raw data strictly follow above folder and file structure 
   	-  run w-website.py file to generate csv files for each PT
	$python3 w-website.py  //select proper options to proceed

   - To make graphs out of the processed data, put tranco results in tranco-1000 folder and blocked results in blocked-1000 folder
	- run plot 



Follow some comm

