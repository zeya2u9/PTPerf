After completion of the measurements, raw data files for each type of experiment (Curl, Selenium, File-download, and Speed-Index) are automatically generated.
We will use these raw files to generate CSVs for applying statistical tests between pairs of PTs and their categories.

Generate CSVs for Pairwise PTs
------------------------------
- copy scripts to your folder
  - each script ending with a figure number corresponds to a figure present in the paper.
  - each script ending with the type of experiment name corresponds to the method of measurement done.

- for getting pairwise CSVs for curl experiment run the following scripts and change the path to the folder where raw data is present 

for curl
$python3 paper_curl.py

for selenium 
$python3 paper_selenium.py

and for speedindex
$python3 paper_speedIndex.py

- Apply statitical tests

Generate statistical results for Pairwise PTs
---------------------------------------------
- for getting pairwise stats for all experiments run the following script
$python3 pt_pairwise_fig2a.py
$python3 pt_pairwise_fig2b.py
$python3 pt_pairwise_fig11.py


