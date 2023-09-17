import os
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan
import csv
import matplotlib.font_manager as font_manager
import numpy as np

base_dir = '~/F1/'
individual_dir = ['file_perc_csvs']

os.chdir(base_dir)

data = {}


for idir in individual_dir:
    os.chdir(idir)
    for file in os.listdir():
        #file_data = read_csv(file)
        filename = file.split('.')[0]
        print(filename)
        file_data = read_csv(file)
        if filename not in data:
            data[filename] = []
        data[filename].extend(file_data['iteration-0'].to_list())
        data[filename].extend(file_data['iteration-1'].to_list())
        data[filename].extend(file_data['iteration-2'].to_list())
        data[filename].extend(file_data['iteration-3'].to_list())
        data[filename].extend(file_data['iteration-4'].to_list())
        data[filename] = list(filter(lambda x: isnan(x) == False, data[filename]))
        #data[filename] = list(filter(lambda x: x < 100, data[filename]))
    os.chdir('../')

#print(data)

plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.size'] = 5
plt.rcParams['ytick.major.width'] = 2
plt.rcParams["figure.figsize"] = (5,4)
plt.xticks(fontsize=13, weight = 'bold')
plt.yticks(weight = 'bold', fontsize=13)

# count, bins_count = np.histogram(data[filename], bins = [i for i in range(0,100)])
# pdf = count / sum(count)
# cdf = np.cumsum(pdf)
# plt.plot(bins_count[1:], cdf, label="obfs4", linewidth = 2.5, color = 'magenta')
markers = ['o', 'v', '^', '<', 'd', 'X', '>', 's', 'p', 'P', '*', 'x', '+']
colors = ['blue', 'y', 'orange', 'forestgreen', 'm', 'r', 'slategrey', 'olive', 'teal', 'purple', 'brown', 'hotpink', 'k']

for pt, mark, clr in zip(['Meek', 'Dnstt', 'Snowflake'], markers, colors):
    count, bins_count = np.histogram(data[pt], bins = [i for i in range(0,101)])
    pdf = count / sum(count)
    cdf = np.cumsum(pdf)
    plt.plot(bins_count[1:], cdf, label=pt, linewidth = 2.5)#, linestyle='dotted', marker=mark, color = clr, markersize = 5)

print(data['Dnstt'])
plt.grid(color = 'grey', linestyle = '--', linewidth = 1)
plt.xlabel('File Download percentage', fontsize='x-large', fontweight='bold')
plt.ylabel('Fraction of attempts', fontsize='x-large', fontweight='bold')
plt.tight_layout()
plt.legend(loc='upper left', fontsize=15)
plt.savefig('f1-file-perc', dpi = 600)
plt.show()
