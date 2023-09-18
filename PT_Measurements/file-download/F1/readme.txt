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
		- keep the format of all_pts.csv like below (the first row denotes file sizes, and the first column denotes PT 
                  names)
			Name , 5MB, 10MB, 20MB, 50MB, 100MB
			Tor 
			Obfs4
			...
			...

	- The above script(z-file-dbmake.py) will also print the number of failures in downloads by all PTs (on the terminal).

	- run all-z-file-dbmake_partial_full_failed.py 
	$python3 all-z-file-dbmake_partial_full_failed.py //it will generate a CSV file named as Final_download_count.csv with following format  (first row contains the PT names, first column contains the file-size values)
			S.N.   ,Tor      ,  Obfs4,   .............. , WebTunnel
			5mb   ,[x, y, z] , [x, y, z] .............. , [x, y, z]
			10mb  ,[x, y, z] , [x, y, z] .............. , [x, y, z]
			20mb  ,[x, y, z] , [x, y, z] .............. , [x, y, z]
			50mb  ,[x, y, z] , [x, y, z] .............. , [x, y, z]
			100mb ,[x, y, z] , [x, y, z] .............. , [x, y, z]
		[x, y, z] --> x denotes the count of complete downloads, y denotes the count of partial downloads, z denotes the count of failed downloads

	- run file_perc_d-file-dbmake.py to get the percentage of file-download for all pts (for all file-sizes in each round)
	$python3 file_perc_d-file-dbmake.py // it will generate separate CSV files for each PT in file_perc_csvs/ folder
	

   - To make graphs out of the processed data follow below lines
	
	- run plotf1.py using all-pts.csv
	$python3 plotf1.py  //it will make a point graph for all PTs download times (fig-5)

	- run plotf3.py using Final_download_count.csv
	$python3 plotf3.py //it will make a stacked-bar graph depicting the %tage of complete/partial/failed downloads for all PTs (fig-8a)

	- run plotf1_file-perc.py using CSVs present in file_perc_csvs/
	$python3 plotf1_file-perc.py //it will make an ECDF of percentage download by meek, dnstt and snowflake. (fig-8b)
