Selenium-based experiments
-------------------------

All measurements will be taken using Selenium browser.

Selenium browser automation setup details
-----------------------------------------
   - copy sel_setup.sh file and selenium_testing folder to your machine and run it
   $./sel_setup.sh

   It will automatically set up selenium on your machine. 


Raw_Data_Collection
-------------------
   - It contains scripts to start the measurement process for each PT. We have followed a common nomenclature for file names and folder names for storing the measurement results.
   - File-name format: n-trf-tr<pt-number>.txt; for example n-trf-tr0.txt represents results for Tor-only.
   - Folder structure: Throughout the measurement at one location, we repeat each website download five times; thus, there are five folders.
	selenium_overall_result1000
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
	Dl Size (Bits): x Time_Taken = xx.xx
        https://www.facebook.com/
	Dl Size (Bits): x Time_Taken = xx.xx
        .......
   - starting the measurements -
	- copy all files and folders from this directory to the machine where PTs have been setup
	- replace <server-pass>, <server-ip> with PT server's password and IP addresses in selenium_testing.py, kill_<0-13>.sh, start_<x>.sh files
	- start the measurement (MOT) - 
        $python3 ../selenium_testing/selenium_curl.py tranco  //for tranco-1000
	$python3 ../selenium_testing/selenium_curl.py blocked  //for blocked-1000
   - Repeat the above steps at each location you want to perform the measurement and save the results.


Raw_Data_Processing
-------------------
2. Raw_Data_Processing: it contains scripts that will process the raw data obtained from step-1
   - To apply processing scripts over the raw data, follow the above folder and file structure
        -  run  file to generate csv files for each PT
        $python3 selenium_overall_result2_z-dbmake.py  //select proper options on prompt to proceed

   - To make graphs out of the processed data, put tranco results in tranco-1000 folder and blocked results in the blocked-1000 folder
        - run plotw1.py
        $python3 plotw1.py  //it will the box-plots for all PTs
