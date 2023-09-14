import os
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan

base_dir = '/home/nsl300/Documents/1_Final_results/W-Website/w11'
individual_dir = ['CSVs']
# labels = ['Tor', 'obfs4', 'Marionette', 'Shadowsocks', 'Stegotaurus', 'Cloak', 'Snowflake', 'Meek', 'Camoufler', 'dnstt', \
#     'Psiphon', 'Conjure', 'Webtunnel']
# proxy_based = ['Meek', 'Snowflake', 'Conjure', 'Massbrowser', 'Psiphon']
proxy_based = ['Meek',  'Psiphon', 'Conjure', 'Snowflake']
tunelling_based = ['Dnstt',  'WebTunnel']
mimicry = ['Marionette', 'Stegotorus', 'Cloak']
fully_encrypted = ['Shadowsocks', 'Obfs4']
data = {}

os.chdir(base_dir)
for idir in individual_dir:
    os.chdir(idir)
    for file in os.listdir():
            filename = file.split('.')[0]
            file_data = read_csv(file)
            data[filename] = []
            data[filename].extend(file_data['Time'].to_list())
            data[filename] = list(filter(lambda x: isnan(x) == False, data[filename]))
    os.chdir('../')

with open('data_dict.json', 'w') as f:
    json.dump(data, f)

#labels, values = [*zip(*data.items())]  # 'transpose' items to parallel key, value lists

# or backwards compatable    
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

# new_data['Snowflake'] = data['Snowflake']
# new_data['Snowflake-100'] = data['Snowflake'][90:100]
# for i in range(101,911,100):
#     #110,201:210,301:310,401:410,501:510,601:610,701:710,801:810,901:910):
#     #print(data['Snowflake'][i:i+10])
#     new_data['Snowflake-100'].extend(data['Snowflake'][i+90:i+100])

#labels, values = data.keys(), data.values()
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
plt.xticks(range(1, len(labels) + 1), labels, rotation = 30, fontsize=13, weight = 'bold')
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
    if count >3 and count <=5:
        patch.set_color('lightblue')
    if count >5 and count <=8:
        patch.set_color('lightpink')
    if count >8 and count <=10:
        patch.set_color('violet')
    if count >10:
        patch.set_color('orange')
    count = count + 1
    patch.set_edgecolor('black')

print(labels)
for medline in box_plot['medians']:
    linedata = medline.get_ydata()
    median = linedata[0]
    print(median)


# plt.yscale('log')
#plt.xlabel('PTs')
#plt.tick_params(axis='y', which='minor')
plt.grid(axis = 'y', color = 'grey', linestyle = '--', linewidth = 1)
plt.ylabel('Speed Index (s)', fontsize='x-large', fontweight='bold')
plt.legend([box_plot["boxes"][0], box_plot["boxes"][4], box_plot["boxes"][6], box_plot["boxes"][9]], \
   ['Proxy-layer', 'Tunnelling', 'Mimicry', 'Fully-encrypted'], loc='upper right', fontsize=15)
plt.tight_layout()
plt.savefig('w11', dpi=600)
plt.show()

