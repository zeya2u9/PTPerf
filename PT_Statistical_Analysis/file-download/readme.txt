After completion of the measurements, raw data files for each type of experiment (Curl, Selenium, File-download, and Speed-Index) are automatically generated. 
In _PTPerf/PT_Measurements/file-downlaod/F1_, there are scripts to generate CSV files for PTs download times (obtained from these raw files).
Use these CSVs to generate statistical results.
Apply statistical tests
Generate statistical results for Pairwise PTs.
---------------------------------------------
For getting pairwise stats for all experiments, run the following script
   $python3 pt_pairwise_file.py

