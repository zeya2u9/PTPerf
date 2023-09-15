PT categories:
"proxy-layer" : [6,7,11,12], 
"tunneling" : [8,9,13], 
"mimicry" : [2,4,5], 
"fully-encrypted" : [1,3], 
"tor" : [0]


At this point, raw data files for each type of experiment (Curl, Selenium, File-download and Speed-Index) have been generated. We will use those raw files to generate CSVs for applying statistical tests between pairs of PTs and their categories.

Generate CSVs for PT Categorywise measurements
----------------------------------------------
- copy scripts to your folder
  - each script ending with a figure number corresponds to a figure present in the paper.
  - each script ending with the type of experiment name corresponds to the method of measurement done.

- for getting pairwise results for PT categories for curl experiment run the following script and change the path to the folder where raw data is present -
$python3 typewiseunion_curl.py

- similarly for selenium and speedindex
$python3 typewiseunion_selenium.py
$python3 typewiseunion_speedIndex.py


- Apply statitical tests

Generate statistical results over above genertaed CSVs 
------------------------------------------------------ 
- for getting PT categorywise stats run the following script 
$python3 pt_pairwise_fig2a_category.py
$python3 pt_pairwise_fig2b_category.py
$python3 pt_pairwise_fig11_category.py


