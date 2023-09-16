File-download based experiments
------------------------------

There are two folders:
1. Raw_Data_Collection:
   - It contains scripts to start the measurement process for each PT. We have followed a common nomenclature for file names and folder names for storing the measurement results.
   - File-name format: new_pt<pt-number>.txt; for example new_pt0.txt represents results for Tor-only.
   - Folder structure: Throughout the measurement at one location, we repeat each website download five times; thus, there are five folders.
        <[server_location]-[client_location]>
		file-download
			result_file1 -> new_pt0.txt, new_pt1.txt, ....... , new_pt13.txt 
			result_file2 -> new_pt0.txt, new_pt1.txt, ....... , new_pt13.txt 
                        ....
			....
			....
     Apart from the names of the files and folders, file format and location variation are all the same as in curl-based 
     experiments.
   - starting the measurements -
        - copy all files from this folder
        - replace <server-pass>, <server-ip> with PT server's password and IP addresses in fdownTime.py, kill_<0-13>.sh, 
           start_<x>.sh files
        - change the url for different file sizes in fDwonload.csv (we hosted our own server to store these files)
	- start the measurement (MOT) -
        $python3 fdownTime.py  
   - Repeat the above steps at each location you want to perform the measurement and save the results.

2. Raw_Data_Processing: it contains scripts that will process the raw data obtained from step 1
   - To apply processing scripts over the raw data, follow the above folder and file structure
        - run z-file-dbmake.py to get the average download time for each PT
         $python3 z-file-dbmake.py 
	     -- From the results of the above scripts, make a single CSV file containing average download times for all file 
                sizes [5,10,20,50,100MB] for each PT.
		- let's assume the name of the CSV is all_pts.csv
		- keep the format of all_pts.csv like below (the first row denotes file sizes, and first column denotes PT 
                  names)
			Name , 5mb, 10mb, 20mb, 50mb, 100mb
			Tor 
			Obfs4
			...
			...
	The above script will also print the number of failures in downloads by all PTs.
  
   - To make graphs out of the processed data (all_pts.csv), run plotf1.py script
	$python3 plotf1.py  //it will make a point graph for all PTs download times

