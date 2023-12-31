4.2.1 complete circuit fixing experiments
-----------------------------------------

Raw_Data_Collection
-------------------

1. This experiment requires first setting up a guard relay, obfs4, and webTunnel bridges privately on a single machine. 
   - For setting up a guard relay, please follow the guidelines provided by Tor Project --> https://community.torproject.org/relay/setup/guard/ 
   - Obfs4 and WebTunnel can be set up using the setup details provided in the PT_Client_Server_Setup folder of this repository

2. copy the same_circuit_selenium_421.py file to your machine 
   - make sure to use appropriate torrc for each transport.
   - strictly follow the SocksPort and ControlPort values used in the python file

3. start the measurement
   $python3 same_circuit_selenium_421.py tranco

   It will start storing the results in the following format -
   tranco
	result_web1 -> n-trf-tr0.txt  n-trf-tr1.txt  n-trf-tr13.txt
        result_web2 -> n-trf-tr0.txt  n-trf-tr1.txt  n-trf-tr13.txt
        result_web3 -> n-trf-tr0.txt  n-trf-tr1.txt  n-trf-tr13.txt
	....
	....
	....
	result_web500 -> n-trf-tr0.txt  n-trf-tr1.txt  n-trf-tr13.txt

   each file will contain --> https://www.youtube.com/
			      Dl Size (Bits): xx Time_Taken = xx.xx circuitCount = x
   we are storing circuit count against each download so that only the measurements with circuit count one should be considered in the analysis.

 
Raw_Data_Processing
-------------------

   - To apply processing scripts over the raw data, follow the above folder and file structure
        -  run FIXED_Circuit_selenium_tor_obfs4_webtunnel_z-dbmake.py file to generate csv files for each PT
        $python3 FIXED_Circuit_selenium_tor_obfs4_webtunnel_z-dbmake.py  //select proper options on prompt to proceed

	It will generate one CSV for Tor-Obfs4-WebTunnel
		tor_obfs4_webTunnel_2500_count.csv
		
   - To make graphs out of the processed data, put tranco results in the same folder as the below script:
        
	- run plotw3.py
        $python3 plotw3.py  //it will make the box-plots for all PTs (fig-3a)
	
	- To make fig-3b in paper do some manual work on the tor_obfs4_webTunnel_2500_count.csv 
	  --> make two CSVs with following names
	      - tor_obfs4_2500_count_for_histogram.csv //it will have a column 'Torobfs4' with time-differences between Tor_time and Obfs4_time
	      - tor_webTunnel_2500_count_for_histogram.csv //it will have a column 'TorWebTunnel' with time-differences between Tor_time and WebTunnel_time 
	  - now run plotw4.py
	  $python3 plotw4.py  //it will make the CDF for time-differences between Tor-obfs4 and Tor-webTunnel (fig-3b)


