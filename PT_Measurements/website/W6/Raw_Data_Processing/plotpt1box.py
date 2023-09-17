import os
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan
import numpy as np

base_dir = '~/W6/'
proxy_based = ['Meek',  'Psiphon', 'Conjure', 'Snowflake']
tunelling_based = ['Dnstt',  'WebTunnel']
mimicry = ['Marionete', 'Stegotorus', 'Cloak']
fully_encrypted = ['Shadowsocks', 'Obfs4']
data = {}

os.chdir(base_dir)
for idir in individual_dir:
    os.chdir(idir)
    for file in os.listdir():
            filename = file.split('.')[0]
            file_data = read_csv(file)
            data[filename] = []
            data[filename].extend(file_data[filename+'-tor'].to_list())
            data[filename] = list(filter(lambda x: isnan(x) == False, data[filename]))
            data[filename] = list(filter(lambda x: x > -20, data[filename]))
    os.chdir('../')


labels, values = data.keys(), data.values()
#labels, values = new_data.keys(), new_data.values()
flierprops = dict(marker='x', markersize=2)#, markeredgecolor='b')
medianprops = dict(color="black",linewidth=1.5)
whiskerprops = dict(linewidth=1.5)
capprops = {'linewidth': '1.5'}

plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.size'] = 5
plt.rcParams['ytick.major.width'] = 2
#plt.rcParams["figure.figsize"] = (10,4)
boxprops = dict(linewidth=1.5)
box_plot = plt.boxplot(values, patch_artist=True, flierprops=flierprops, medianprops = medianprops, \
    boxprops = boxprops, whiskerprops = whiskerprops, capprops = capprops) #, showfliers=False)
# box_plot = plt.violinplot(values)
plt.xticks(range(1, len(labels) + 1), labels, rotation = 25, fontsize=13, weight = 'bold')
plt.yticks(weight = 'bold', fontsize=13)

for patch in box_plot['boxes']:
    patch.set_color('lightgrey')
    patch.set_edgecolor('black')

plt.grid(axis = 'y', color = 'grey', linestyle = '--', linewidth = 1)
plt.ylabel('Time difference (s)', fontsize='x-large', fontweight='bold')
plt.tight_layout()
plt.savefig('pt1-box', dpi=600)
plt.show()

