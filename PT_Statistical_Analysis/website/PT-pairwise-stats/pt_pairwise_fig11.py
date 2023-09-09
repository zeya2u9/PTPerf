import os
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan
import csv
import matplotlib.font_manager as font_manager

import scipy.stats as st
import numpy as np

import pandas as pd

base_dir =  input("Enter absolute path to speed-index time between pairs of PTs")
data = {}
os.chdir(base_dir)
pt_pairs = os.listdir(base_dir)

pt_names = ['Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']
pts = len(pt_names)


##########function to calculate 95% CI
def ci_func(g1,g2):
    diff1 = [ i-j for i,j in zip( g1, g2 ) ]
    values = st.norm.interval(confidence=0.95, loc=np.mean( diff1 ), scale=st.sem(diff1) ) 
    return values

#create dataframe to store values
data = pd.DataFrame(columns=['Pt_Pair','CI_start', 'CI_end', 't-value' ,'p-value','Mean_diff','PT1_mean', 'PT1_std', 'PT2_mean', 'PT2_std','Degree_of_Freedom'])

count = 0
for pt in pt_pairs:
    pt_data = pd.read_csv(pt)
    # print(pt_data.columns[1:3])
    a = [k for k in pt_data.iloc[:,1]]
    b = [k for k in pt_data.iloc[:,2]]
    index_v = f"{pt[13:-11]}"   #for speedindex
    print(index_v)
    
    data.at[index_v, 'Pt_Pair'] = index_v
    
    #Mean and std deviation of each pt 
    data.at[index_v, 'PT1_mean'] = np.mean(a)
    data.at[index_v, 'PT1_std'] = np.std(a)
    data.at[index_v, 'PT2_mean'] = np.mean(b)
    data.at[index_v, 'PT2_std'] = np.std(b)
    
    # calculate CI
    ci_value1, ci_value2 = ci_func(a, b)
    # print(ci_value1, ci_value2)
    data.at[index_v, 'CI_start'] = ci_value1
    data.at[index_v, 'CI_end'] = ci_value2         

    # calculate t-test
    t_test_value1, t_test_value2 = st.ttest_rel(a,b)
    data.at[index_v, 't-value'] = t_test_value1
    data.at[index_v, 'p-value'] = t_test_value2
    
    # add mean_diff, Degree of freedom
    diff_t = [p-q for p,q in zip(a,b)]
    data.at[index_v, 'Mean_diff'] = np.mean(diff_t)
    data.at[index_v, 'Degree_of_Freedom'] = len(a) - 1
    
    
    count = count + 1
    # exit(0)
print(count)

path = input("Enter absolute path to save test-results")
data.to_csv(f"{path}/fig_11.csv", index=False)
