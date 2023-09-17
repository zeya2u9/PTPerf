import os
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan
import statistics

base_dir = '~/W1'
individual_dir = ['tranco-1000']
pts_to_consider = ['Meek', 'Snowflake', 'Obfs4']
proxy_based = ['Meek',  'Psiphon', 'Conjure', 'Snowflake']
tunelling_based = ['Camoufler', 'Dnstt',  'WebTunnel']
mimicry = ['Marionete', 'Stegotorus', 'Cloak']
fully_encrypted = ['Shadowsocks', 'Obfs4']
data = {}

os.chdir(base_dir)
for idir in individual_dir:
    os.chdir(idir)
    for dir in pts_to_consider:
        os.chdir(dir)
        for file in os.listdir():
            data[dir+str(file)] = []
            print(dir+str(file))
            file_data = read_csv(file)
            data[dir+str(file)].extend(file_data['Time'].to_list())
            data[dir+str(file)] = list(filter(lambda x: isnan(x) == False, data[dir+str(file)]))
        os.chdir('../')
    os.chdir('../')

with open('data_dict.json', 'w') as f:
    json.dump(data, f)

plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.size'] = 5
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['xtick.minor.size'] = 5
plt.rcParams['xtick.minor.width'] = 1
plt.rcParams['ytick.minor.size'] = 3
plt.rcParams['ytick.minor.width'] = 1
plt.rcParams["figure.figsize"] = (7,4)
plt.xticks(fontsize=10, weight = 'bold')
plt.yticks(weight = 'bold', fontsize=10)

new_data = {}
new_data['BLR'] = {'Meek': data['Meekfra-blr.csv'], 'Snowflake' : data['Snowflakefra-blr.csv'], 'Obfs4' : data['Obfs4fra-blr.csv']}
new_data['LON'] = {'Meek': data['Meekfra-lon.csv'], 'Snowflake' : data['Snowflakefra-lon.csv'], 'Obfs4' : data['Obfs4fra-lon.csv']}
new_data['TORO'] = {'Meek': data['Meekfra-tor.csv'], 'Snowflake' : data['Snowflakefra-tor.csv'], 'Obfs4' : data['Obfs4fra-tor.csv']}

# print(new_data)

fig, axes = plt.subplots(ncols=3, sharey=True)
fig.subplots_adjust(wspace=0)
flierprops = dict(marker='x', markersize=1.5)#, markeredgecolor='b')
medianprops = dict(color="black",linewidth=1.25)
whiskerprops = dict(linewidth=1.25)
capprops = {'linewidth': '1.25'}
boxprops = dict(linewidth=1.25)
#boxprops = {dict(linewidth=1.5)}
# colors = ['lightgreen', 'lightblue', 'lightpink']

for ax, name in zip(axes, ['BLR', 'LON', 'TORO']):
    bplot = ax.boxplot([new_data[name][item] for item in ['Meek', 'Snowflake', 'Obfs4']], flierprops=flierprops, medianprops = medianprops, \
    boxprops = boxprops, whiskerprops = whiskerprops, capprops = capprops, patch_artist=True)
    #ax.set_xticklabels(['Meek', 'Snowflake', 'Obfs4'], rotation=10, xlabel=name)
    #ax.set(xticklabels=['Meek', 'Snowflake', 'Obfs4'], xlabel=name)
    ax.set_xticklabels(['Meek', 'Snowflake', 'Obfs4'], rotation = 20, fontsize = 12, weight = 'bold')
    ax.set_yticklabels([i for i in range(0,61,10)], fontsize = 12, weight = 'bold')
    ax.set_xlabel(name, fontsize = 12, weight = 'bold')
    ax.set_ylabel('Download Time (s)', fontsize = 13, weight = 'bold')
    #ax.set_facecolor('lightgreen')
    colors = ['lightgreen', 'lightgrey', 'violet']
    for patch, color in zip(bplot['boxes'], colors):
        # patch.set_edgecolor('black')
        patch.set_color(color)
        patch.set_edgecolor('black')
    ax.set_ylim(1,100)
    ax.grid(axis = 'y', color = 'grey', linestyle = '--', linewidth = 1)
# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axes.flat:
    ax.label_outer()

count = 0
plt.yscale('log')
fig.tight_layout()
fig.show()
fig.savefig('L1', dpi=600)

