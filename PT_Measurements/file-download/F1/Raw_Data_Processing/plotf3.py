import os
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan
import csv
import numpy as np
from matplotlib.ticker import FormatStrFormatter

base_dir = '~/F1'
data = {}
labels = ['Tor', 'Obfs4', 'Marionette', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Meek', 'Camoufler', 'Snowflake', 'Dnstt', \
    'Psiphon', 'Conjure', 'WebTunnel']
download_status = ['complete', 'partial', 'failed']

os.chdir(base_dir)

file_data = read_csv('Final_download_count.csv')
# print(file_data['Tor'])
# a = file_data['Tor']
# print(int(a[0][1]), a[0][4], a[0][7])
data['complete'] = []
data['partial'] = []
data['failed'] = []

for label in labels:
    comp = 0.0
    partial = 0.0
    fail = 0.0
    for element in file_data[label]:
        comp = comp + int(element[1])
        partial = partial + int(element[4])
        fail = fail + int(element[7])
    if label == 'Camoufler':
        comp = comp/50
        partial = partial/50
        fail = fail/50
    else:
        comp = comp/25
        partial = partial/25
        fail = fail/25
    data['complete'].append(comp)
    data['partial'].append(partial)
    data['failed'].append(fail)

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
plt.rcParams["figure.figsize"] = (6,3.5)
plt.xticks(fontsize=10, weight = 'bold')
plt.yticks( weight = 'bold', fontsize=10)
#labels = [i for i in range(len(labels))]
print(labels)


plt.xticks(range(1, len(labels) + 1), labels, rotation = 35, fontsize=10, weight = 'bold')
fig, ax = plt.subplots()
ax.bar(labels, data['complete'], 0.4, hatch = '///', label = 'complete')
ax.bar(labels, data['partial'], 0.4, hatch = '.', label = 'partial', bottom = data['complete'])
ax.bar(labels, data['failed'], 0.4, hatch = 'xx', label = 'failed', bottom = np.array(data['complete']) + np.array(data['partial']))
ax.set_xticklabels(labels, fontsize = 10, weight = 'bold')
ax.set_yticklabels(ax.get_yticks(), weight='bold')
plt.setp(ax.xaxis.get_majorticklabels(), rotation=45 ) 
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))

plt.ylabel('Fraction of downloads', fontsize='large', fontweight='bold')
plt.tight_layout()
plt.legend()
plt.savefig('f3', dpi=600)
plt.show()
