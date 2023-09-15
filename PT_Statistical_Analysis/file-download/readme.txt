At this point, raw data files for each type of experiment (Curl, Selenium, File-download and Speed-Index) have been generated. We will use those raw files to generate CSVs for applying statistical tests between pairs of PTs and their categories.
Also we have csv files conatining results for each file download corresponding to ecah PT. We will use these CSVs to genertae statistical results.

- Apply statitical tests

Generate statistical results for Pairwise PTs
---------------------------------------------
- for getting pairwise stats for all experiments run the following script
$python3 pt_pairwise_file.py

