import os
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan
import statistics

base_dir = 'W3'
data = {}

os.chdir(base_dir)
file_data = read_csv('tor_obfs4_webTunnel_2500_count.csv')
data['Tor'] = []
data['Tor'].extend(file_data['+ACI-Time+AF8-tor+ACI-'].to_list())
data['Tor'] = list(filter(lambda x: isnan(x) == False, data['Tor']))
data['obfs4'] = []
data['obfs4'].extend(file_data['+ACI-Time+AF8-Obfs4+ACI-'].to_list())
data['obfs4'] = list(filter(lambda x: isnan(x) == False, data['obfs4']))
data['WebTunnel'] = []
data['WebTunnel'].extend(file_data['+ACI-Time+AF8-WebTunnel+ACI-'].to_list())
data['WebTunnel'] = list(filter(lambda x: isnan(x) == False, data['WebTunnel']))

labels, values = data.keys(), data.values()

flierprops = dict(marker='x', markersize=2)#, markeredgecolor='b')
medianprops = dict(color="black",linewidth=1.5)
whiskerprops = dict(linewidth=1.5)
capprops = {'linewidth': '1.5'}

plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.size'] = 5
plt.rcParams['ytick.major.width'] = 2
plt.rcParams["figure.figsize"] = (5,4)
boxprops = dict(linewidth=1.5)
# box_plot = plt.violinplot(values,showmedians=True)
box_plot = plt.boxplot(values, patch_artist=True, flierprops=flierprops, medianprops = medianprops, \
    boxprops = boxprops, whiskerprops = whiskerprops, capprops = capprops) #, showfliers=False)

# box_plot = plt.boxplot(values, patch_artist=True, flierprops=flierprops, medianprops = medianprops, \
#     boxprops = boxprops, whiskerprops = whiskerprops, capprops = capprops) #, showfliers=False)

plt.xticks(range(1, len(labels) + 1), labels, fontsize=13, weight = 'bold')
plt.yticks(weight = 'bold', fontsize=13)
# for median in box_plot['medians']:
#     median.set_color('black')
#     median.set_width('2')

count = 0
colors = ['orange', 'violet', 'lightblue']
for patch, color in zip(box_plot['boxes'], colors):
# for patch, color in zip(box_plot['bodies'], colors):
    # patch.set_edgecolor('black')
    patch.set_color(color)
    patch.set_edgecolor('black')
#plt.yscale('log')
#plt.xlabel('PTs')
#plt.tick_params(axis='y', which='minor')
plt.grid(axis = 'y', color = 'grey', linestyle = '--', linewidth = 1)
plt.ylabel('Download time (s)', fontsize='x-large', fontweight='bold')
plt.tight_layout()
plt.savefig('w3', dpi=600)
plt.show()

