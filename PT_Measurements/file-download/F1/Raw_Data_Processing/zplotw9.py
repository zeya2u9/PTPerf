import os
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan
import statistics

base_dir = '~/F1/'
individual_dir = ['Snowflake', 'Snowflake-jan2023']
data = {}

os.chdir(base_dir)
for idir in individual_dir:
        os.chdir(idir)
        data[idir] = []
        for file in os.listdir():
            file_data = read_csv(file)
            data[idir].extend(file_data['Time'].to_list())
        data[idir] = list(filter(lambda x: isnan(x) == False, data[idir]))
        os.chdir('../')

new_data = {}
new_data['Pre-September'] = data['Snowflake']
new_data['Post-September'] = data['Snowflake-jan2023']


labels, values = new_data.keys(), new_data.values()
#print(values[1])

flierprops = dict(marker='x', markersize=2)#, markeredgecolor='b')
medianprops = dict(color="black",linewidth=1.5)
whiskerprops = dict(linewidth=1.5)
capprops = {'linewidth': '1.5'}

plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.size'] = 5
plt.rcParams['ytick.major.width'] = 2
plt.rcParams['xtick.minor.size'] = 5
plt.rcParams['xtick.minor.width'] = 1
plt.rcParams['ytick.minor.size'] = 3
plt.rcParams['ytick.minor.width'] = 1
#plt.rcParams["figure.figsize"] = (6,4)
boxprops = dict(linewidth=1.5)
box_plot = plt.boxplot(values, patch_artist=True, flierprops=flierprops, medianprops = medianprops, \
    boxprops = boxprops, whiskerprops = whiskerprops, capprops = capprops) #, showfliers=False)
plt.xticks(range(1, len(labels) + 1), labels, fontsize=13, weight = 'bold')
plt.yticks(weight = 'bold', fontsize=13)
# for median in box_plot['medians']:
#     median.set_color('black')
#     median.set_width('2')
print(box_plot['boxes'])
count = 0
colors = ['orange', 'violet']
for patch, color in zip(box_plot['boxes'], colors):
    # patch.set_edgecolor('black')
    patch.set_color(color)
    patch.set_edgecolor('black')
plt.yscale('log')
#plt.xlabel('Snowflake Performance', fontsize='x-large', fontweight='bold')
#plt.tick_params(axis='y', which='minor')
plt.grid(axis = 'y', color = 'grey', linestyle = '--', linewidth = 1)
plt.ylabel('Download time (s)', fontsize='x-large', fontweight='bold')
plt.tight_layout()
plt.savefig(f'{base_dir}/w9', dpi = 600)
# plt.show()


