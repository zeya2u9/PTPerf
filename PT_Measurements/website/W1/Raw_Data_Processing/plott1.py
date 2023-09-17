import os
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan
import statistics
import numpy as np

base_dir = '~/W1'
individual_dir = ['tranco-1000']
proxy_based = ['Meek',  'Psiphon', 'Conjure', 'Snowflake']
tunelling_based = ['Camoufler', 'Dnstt',  'WebTunnel']
mimicry = ['Marionete', 'Stegotorus', 'Cloak']
fully_encrypted = ['Shadowsocks', 'Obfs4']
data = {}

os.chdir(base_dir)
for idir in individual_dir:
    os.chdir(idir)
    for dir in os.listdir():
        data[dir] = []
        os.chdir(dir)
        for file in os.listdir():
            file_data = read_csv(file)
            data[dir].extend(file_data['Time'].to_list())
        data[dir] = list(filter(lambda x: isnan(x) == False, data[dir]))
        os.chdir('../')
    os.chdir('../')

with open('data_dict.json', 'w') as f:
    json.dump(data, f)

  
plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.size'] = 5
plt.rcParams['ytick.major.width'] = 2
plt.rcParams["figure.figsize"] = (7,4)
plt.xticks(fontsize=13, weight = 'bold')
plt.yticks(weight = 'bold', fontsize=13)

markers = ['o', 'v', '^', '<', 'd', 'X', '>', 's', 'p', 'P', '*', 'x', '+']
colors = ['blue', 'y', 'orange', 'forestgreen', 'm', 'r', 'slategrey', 'olive', 'teal', 'purple', 'brown', 'hotpink', 'k']

for pt, mark, clr in zip(data, markers, colors):
    count, bins_count = np.histogram(data[pt], bins=[i for i in range(0,41)])
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf, label=pt, linestyle='dotted', marker=mark, color = clr, markersize = 5)
plt.xlabel('Time (in seconds)')
plt.ylabel('Fraction of websites')

plt.grid(color = 'grey', linestyle = '--', linewidth = 1)
plt.xlabel('Time (s)', fontsize='x-large', fontweight='bold')
plt.ylabel('Fraction of values', fontsize='x-large', fontweight='bold')
plt.tight_layout()
plt.legend()
plt.savefig('t1', dpi=600)
plt.show()
