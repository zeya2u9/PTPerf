import os
import matplotlib
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan
import csv

base_dir = 'C:/Users/piyus/Documents/1_Final_results/F-File/F2'
#individual_dir = ['tranco-1000']
data = {}
# labels = ['Tor', 'obfs4', 'Marionette', 'Shadowsocks', 'Stegotaurus', 'Cloak', 'Snowflake', 'Meek', 'Camoufler', 'dnstt', \
#     'Psiphon', 'Conjure', 'Webtunnel']
labels = []

os.chdir(base_dir)

file_data = read_csv('selenium_file_download_times.csv')
#print(file_data)
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
#plt.rcParams["figure.figsize"] = (7,4)
plt.rcParams['xtick.minor.size'] = 5
plt.rcParams['xtick.minor.width'] = 1
plt.rcParams['ytick.minor.size'] = 3
plt.rcParams['ytick.minor.width'] = 1
plt.xticks(fontsize=10, weight = 'bold')
plt.yticks(weight = 'bold', fontsize=10)

# plt.plot(labels, data['5mb'], label = '5 MB', linestyle='dashed', marker='o')
# plt.plot(labels, data['10mb'], label = '10 MB', linestyle='dashed', marker='o')
# plt.plot(labels, data['20mb'], label = '20 MB', linestyle='dashed', marker='o')
# plt.plot(labels, data['50mb'], label = '50 MB', linestyle='dashed', marker='o')
# #plt.plot(labels, data['100mb'], label = '100 MB', linestyle='dashed', marker='o')
# plt.xticks(range(1, len(labels) + 1), labels, rotation = 35)
# #plt.title("Tor + WebTunnel Histogram")
# # plt.xlabel('Time bins (in seconds)')
# # plt.ylabel('Number of occurences')

#plt.xticks(range(1, len(labels) + 1), labels, rotation = 35, fontsize=10, weight = 'bold')
fig, ax = plt.subplots()
ax.plot(labels, data['5mb'], label = '5 MB', linestyle='dashed', marker='o')
ax.plot(labels, data['10mb'], label = '10 MB', linestyle='dashed', marker='o')
ax.plot(labels, data['20mb'], label = '20 MB', linestyle='dashed', marker='o')
ax.plot(labels, data['50mb'], label = '50 MB', linestyle='dashed', marker='o')
ax.plot(labels, data['100mb'], label = '100 MB', linestyle='dashed', marker='o')
ax.set_xticklabels(labels, fontsize = 13, weight = 'bold')
# ax.set_yticks([1, 10, 100, 1000])
# ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

ax.set_ylim(5,2000)
ax.set_yticklabels(ax.get_yticks(), weight='bold', fontsize = 13)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45 ) 

plt.yscale('log')
plt.grid(color = 'grey', linestyle = '--', linewidth = 1)
#plt.xlabel('Download time difference(s)', fontsize='large', fontweight='bold')
#plt.ylabel('Download time (s)', fontsize='x-large', fontweight='bold')
plt.tight_layout()
#plt.legend()
plt.savefig('../../f2', dpi=600)
plt.show()
