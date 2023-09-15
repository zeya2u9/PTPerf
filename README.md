# PTPerf
IMC'23 Artifacts

This repo hosts the setup details, necessary source code for starting different pluggable transports(PT, measurement scripts and statistical analysis scripts. For more details about our IMC 2023 paper, please see <PTPerf-link>.

Repository Structure
--------------------

There are three major directories  
_PT_Client_Server_Setup_  
As the name suggests, it contains individual folders containing deployment details for a PT client and server.  

_PT_Measurements_   
It contains all the scripts to start a measurement campaign once you have deployed your PT clients and servers. These measurements span from website access using curl utility or selenium based browser automation. It also includes fixing the complete Tor circuits for digging deeper into some measurements. Overall in each measurement directory, it contains two sub-directories as follows -  
First, _Raw_Data_Collection_ contains automation scripts to start the measurement and storing the data.  
Second, _Raw_Data_Processing_ contains analysis scripts over the raw data.  

_PT_Statistical_Analysis_  
We applied paired t-test over the measurement results. T-tests can be applied over two PTs results as well as over two categories of PTs results. This repository contains scripts to first arrange the raw data in the form where t-test can be applied. And then there are scripts to apply the t-test and store results properly.  

