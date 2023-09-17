import os
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan
import statistics

base_dir = '~/W1'
individual_dir = ['tranco-1000']#,'blocked-1000']
# labels = ['Tor', 'obfs4', 'Marionette', 'Shadowsocks', 'Stegotaurus', 'Cloak', 'Snowflake', 'Meek', 'Camoufler', 'dnstt', \
#     'Psiphon', 'Conjure', 'Webtunnel']
# proxy_based = ['Meek', 'Snowflake', 'Conjure', 'Massbrowser', 'Psiphon']
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

new_data = {}
for item in proxy_based:
    new_data[item] = data[item]
for item in tunelling_based:
    new_data[item] = data[item]
for item in mimicry:
    new_data[item] = data[item]
for item in fully_encrypted:
    new_data[item] = data[item]
new_data['Tor-only'] = data['Tor-only']

labels, values = new_data.keys(), new_data.values()
flierprops = dict(marker='x', markersize=2)#, markeredgecolor='b')
medianprops = dict(color="black",linewidth=1.5)
whiskerprops = dict(linewidth=1.5)
capprops = {'linewidth': '1.5'}

plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.size'] = 5
plt.rcParams['ytick.major.width'] = 2
plt.rcParams["figure.figsize"] = (10,4.5)
boxprops = dict(linewidth=1.5)
box_plot = plt.boxplot(values, patch_artist=True, flierprops=flierprops, medianprops = medianprops, \
    boxprops = boxprops, whiskerprops = whiskerprops, capprops = capprops) #, showfliers=False)
plt.xticks(range(1, len(labels) + 1), labels, rotation = 35, fontsize=13, weight = 'bold')
plt.yticks(weight = 'bold', fontsize=13)
# for median in box_plot['medians']:
#     median.set_color('black')
#     median.set_width('2')
print(box_plot['boxes'])
count = 0
for patch in box_plot['boxes']:
    # patch.set_edgecolor('black')
    if count <=3:
        patch.set_color('lightgreen')
    if count >3 and count <=6:
        patch.set_color('lightblue')
    if count >6 and count <=9:
        patch.set_color('lightpink')
    if count >9 and count <=11:
        patch.set_color('violet')
    if count >11:
        patch.set_color('orange')
    count = count + 1
    patch.set_edgecolor('black')

## for plotting median values
for medline in box_plot['medians']:
    linedata = medline.get_ydata()
    median = linedata[0]
    print(median)

#plt.yscale('log')
#plt.xlabel('PTs')
#plt.tick_params(axis='y', which='minor')
plt.grid(axis = 'y', color = 'grey', linestyle = '--', linewidth = 1)
plt.ylabel('Download time (s)', fontsize='x-large', fontweight='bold')
plt.legend([box_plot["boxes"][0], box_plot["boxes"][4], box_plot["boxes"][7], box_plot["boxes"][10]], \
    ['Proxy-layer', 'Tunnelling', 'Mimicry', 'Fully-encrypted'], loc='upper right', fontsize=15)
plt.tight_layout()
# plt.savefig('../../w1', dpi=600)
plt.show()
