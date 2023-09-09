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

base_dir = input("Enter absolute path to file-download csvs for each PT:: ")

data = {}
os.chdir(base_dir)
pt_pairs = os.listdir(base_dir)
print(f'Total:: {pt_pairs}')
pt_len = len(pt_pairs)

pt_names = ['Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']
pts = len(pt_names)

##########function to calculate 95% CI
def ci_func(g1,g2):
    diff1 = [ i-j for i,j in zip( g1, g2 ) ]
    values = st.t.interval(alpha=0.95, df=len(diff1)-1,loc=np.mean( diff1 ), scale=st.sem(diff1) ) 
    return values


#create dataframe to store values
data = pd.DataFrame(columns=['Pt_Pair','CI_start', 'CI_end', 't-value' ,'p-value','Mean_diff','PT1_mean', 'PT1_std', 'PT2_mean', 'PT2_std', 'Degree_of_Freedom'])

count = 0
for pt1 in range(pt_len):
    for pt2 in range(pt_len):
        if pt1 == pt2 or pt1 > pt2:
            continue
        index_v = f"{pt_pairs[pt1][:-4]+'-'+pt_pairs[pt2][:-4]}"
        data.at[index_v, 'Pt_Pair'] = index_v
        
        #load the two csv files
        csv1 = pd.read_csv(f"{pt_pairs[pt1]}")
        csv2 = pd.read_csv(f"{pt_pairs[pt2]}")
        # print(csv1, csv2)
        
        c = 0
        a = [0]*25
        b = [0]*25
        for i in range(5):
            for j in range(5):
                a[c] = csv1.iloc[i,j] 
                b[c] = csv2.iloc[i,j]   
                c = c + 1
        # print(a,b)
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
print(count)

path = input("Enter absolute path to save test-results")
data.to_csv(f"{path}/fig_5.csv", index=False)
