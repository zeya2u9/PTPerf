At this point, raw data files for each type of experiment (Curl, Selenium, File-download and Speed-Index) have been generated. And in _PTPerf/PT_Measurements/file-downlaod/F1_, there are scripts to generate CSV files for PTs download times. We will use these CSVs to genertae statistical results.

- Apply statitical tests

Generate statistical results for Pairwise PTs
---------------------------------------------
- for getting pairwise stats for all experiments run the following script
$python3 pt_pairwise_file.py

