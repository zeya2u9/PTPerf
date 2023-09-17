PT-isolating_performance_of_only_PTs_from_Tor
--------------------------------------------

Raw_Data_Collection
-------------------

1. This experiment requires first setting up a guard relay on a machine. 
   - For setting up a guard relay, please follow the guidelines provided by Tor Project --> https://community.torproject.org/relay/setup/guard/ 

2. copy the tor_g_me_fixed_only_curl.py file to your machine 
   - make sure to use appropriate torrc for each transport.
   - strictly follow the SocksPort and ControlPort values used in the python file
   - please change all <server-pass>, <server-ip>, <pt_number> and <guard-relay-fingerprint> with their respective values from your setup.

3. install carml using https://github.com/meejah/carml 
   It will be used to attach streams to circuits in this experiment. It is being handled in the tor_g_me_fixed_only_curl.py automatically. 

3. start the measurement
   $python3 tor_g_me_fixed_only_curl.py tranco

   It will start storing the results in the following format -
   <pt_name>
	result_web1 -> n-trf-tr0.txt  n-trf-tr<pt_number>.txt 
        result_web2 -> n-trf-tr0.txt  n-trf-tr<pt_number>.txt 
        result_web3 -> n-trf-tr0.txt  n-trf-tr<pt_number>.txt 
        result_web2 -> n-trf-tr0.txt  n-trf-tr<pt_number>.txt
        result_web3 -> n-trf-tr0.txt  n-trf-tr<pt_number>.txt


   each file will contain results in the following format:
        ......
        https://www.youtube.com/
        Size_of_downloaded_file: xx Download_speed_Bps: xx.xx Connect: xx.xx TTFB: xx.xx Total time: xx.xx circuitCount = xx
        https://www.facebook.com/
        Size_of_downloaded_file: xx Download_speed_Bps: xx.xx Connect: xx.xx TTFB: xx.xx Total time: xx.xx circuitCount = xx
        .......
   we are storing circuit count against each download so that only the measurements with circuit count one should be considered in the analysis.

 
Raw_Data_Processing
-------------------

   - To apply processing scripts over the raw data, follow the above folder and file structure
        -  run curl_tor_ptwithTor_curl_1000.py file to generate csv files for each PT
        $python3 curl_tor_ptwithTor_curl_1000.py  //select proper options on prompt to proceed (location, Total_time, TTFB, etc.)
		
   - To make graphs out of the processed data, put CSVs and plotpt1box.py in the same folder:        
	- run plotpt1box.py
        $python3 plotpt1box.py  //it will make the box-plots for all PTs (fig-9)
	


