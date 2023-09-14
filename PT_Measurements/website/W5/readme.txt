Speed-index using browser-time
------------------------------

Setup browsertime
-----------------
   - copy the browsertime_install.sh from this folder and run it
   $./browsertime_install.sh
	
   It will automatically setup browsertime on your machine.

Raw_Data_Collection
-------------------
   - follow the same nomenclature of files and folders for storing results of website downloads for each PT as explained in PT_Measurement/W2/readme.txt

   - starting the measurements -
        - copy all files and folders from this directory to the machine where PTs have been setup
        - replace <server-pass>, <server-ip> with PT server's password and IP addresses in browsertime_lover.py, kill_<0-13>.sh, start_<x>.sh files
        - start the measurement (MOT) -
        $python3 browsertime_lover.py tranco  //for tranco-1000
        $python3 browsertime_lover.py blocked  //for blocked-1000
   - Repeat above steps at each location you want to perform the measurement and save results.

Raw_Data_Processing
-------------------
2. Raw_Data_Processing: it contains scripts which will process the raw data obtained from step-1
   - To apply processing scripts over the raw data follow above folder and file structure
        -  run w11-website.py file to generate csv files for each PT
        $python3 w11-website.py  //select proper options on prompt to proceed

   - To make graphs out of the processed data, put tranco results in tranco folder and blocked results in blocked folder
        - run plotw11.py
        $python3 plotw11.py  //it will the box-plots for all PTs
