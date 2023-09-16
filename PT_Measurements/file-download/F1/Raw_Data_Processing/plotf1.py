import os
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan
import csv
import matplotlib.font_manager as font_manager

base_dir = '~/F1'
data = {}
labels = []

os.chdir(base_dir)

file_data = read_csv('all_pts.csv')
# print(file_data)
labels.extend(file_data['Name'])
data['5mb'] = []
data['10mb'] = []
data['20mb'] = []
data['50mb'] = []
data['100mb'] = []
data['5mb'].extend(file_data['5mb'].to_list())
data['10mb'].extend(file_data['10mb'].to_list())
data['20mb'].extend(file_data['20mb'].to_list())
data['50mb'].extend(file_data['50mb'].to_list())
data['100mb'].extend(file_data['100mb'].to_list())

print(data)

plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.size'] = 5
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['xtick.minor.size'] = 5
plt.rcParams['xtick.minor.width'] = 1
plt.rcParams['ytick.minor.size'] = 3
plt.rcParams['ytick.minor.width'] = 1
#plt.rcParams["figure.figsize"] = (7,4)
# plt.xticks(fontsize=10, weight = 'bold')
# plt.yticks(weight = 'bold', fontsize=10)
#labels = [i for i in range(len(labels))]
print(labels)

fig, ax = plt.subplots()
ax.plot(labels, data['5mb'], label = '5 MB', linestyle='dashed', marker='o')
ax.plot(labels, data['10mb'], label = '10 MB', linestyle='dashed', marker='o')
ax.plot(labels, data['20mb'], label = '20 MB', linestyle='dashed', marker='o')
ax.plot(labels, data['50mb'], label = '50 MB', linestyle='dashed', marker='o')
ax.plot(labels, data['100mb'], label = '100 MB', linestyle='dashed', marker='o')
ax.set_xticklabels(labels, fontsize = 13, weight = 'bold', ha='right')
ax.set_yticklabels(ax.get_yticks(), weight='bold', fontsize = 13)
handles, labels = ax.get_legend_handles_labels()
font = font_manager.FontProperties(weight='bold')
ax.legend(handles[::-1], labels[::-1], prop=font)
ax.set_ylim(5,2000)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, fontsize = 13) 


plt.yscale('log')
plt.grid(color = 'grey', linestyle = '--', linewidth = 1)
# plt.grid(which = 'minor', color = 'grey', linestyle = '--', linewidth = 0.5)
# plt.grid(which = 'major', color = 'grey', linestyle = '--', linewidth = 0.5)
#plt.xlabel('Download time difference(s)', fontsize='large', fontweight='bold')
plt.ylabel('Download time (s)', fontsize='x-large', fontweight='bold')
plt.tight_layout()
#plt.legend(fontsize = 10)
plt.savefig('../../f1', dpi=600)
plt.show()
