# PTPerf
IMC'23 Artifacts

This repo contains the setup details, source code for starting different pluggable transports (PTs), measurement scripts, and statistical analysis scripts. For more details about our IMC 2023 paper, please see <PTPerf-link>.

Repository Structure
--------------------

There are three major directories  
_PT_Client_Server_Setup_  
As the name suggests, it contains individual folders containing deployment details for a PT client and server.  

_PT_Measurements_   
It contains all the scripts to start a measurement campaign once you have deployed your PT clients and servers. These measurements include website access using curl utility, selenium-based browser automation, and fixing the complete Tor circuits (for nuanced analysis). Overall, each measurement directory contains two sub-directories as follows -  
First, _Raw_Data_Collection_ contains automation scripts to start the measurement and storing of the data.  
Second, _Raw_Data_Processing_ contains analysis scripts over the raw data.  

_PT_Statistical_Analysis_  
We applied a paired t-test to the measurement results, e.g., the download times of a pair of PTs. This repository contains scripts first to arrange the raw data such that a t-test can be applied. Next, there are scripts to apply the t-test and store results.  

