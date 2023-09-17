import os
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan
import statistics
import numpy as np

base_dir = '~/W3'

data = {}

os.chdir(base_dir)
file_data = read_csv('tor_obfs4_2500_count_for_histogram.csv', encoding='utf-7')
data['Tor'] = []
data['Tor'].extend(file_data['Torobfs4'].to_list())
data['Tor'] = list(filter(lambda x: isnan(x) == False, data['Tor']))
# data['obfs4'] = []
# data['obfs4'].extend(file_data['Time+AF8-obfs4'].to_list())
# data['obfs4'] = list(filter(lambda x: isnan(x) == False, data['obfs4']))

file_data = read_csv('tor_webTunnel_2500_count_for_histogram.csv', encoding='utf-7')
# data['Tor1'] = []
# data['Tor1'].extend(file_data['Time+AF8-tor'].to_list())
# data['Tor1'] = list(filter(lambda x: isnan(x) == False, data['Tor1']))
data['WebTunnel'] = []
data['WebTunnel'].extend(file_data['TorWebTunnel'].to_list())
data['WebTunnel'] = list(filter(lambda x: isnan(x) == False, data['WebTunnel']))

plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.size'] = 5
plt.rcParams['ytick.major.width'] = 2
plt.rcParams["figure.figsize"] = (5,4)
plt.xticks(fontsize=13, weight = 'bold')
plt.yticks(weight = 'bold', fontsize=13)

count, bins_count = np.histogram(data['Tor'], bins = [i for i in range(0,50)])# bins=[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
pdf = count / sum(count)
cdf = np.cumsum(pdf)
plt.plot(bins_count[1:], cdf, label="obfs4", linewidth = 2.5, color = 'magenta')
count, bins_count = np.histogram(data['WebTunnel'],bins = [i for i in range(0,50)]) #bins=[0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
pdf = count / sum(count)
cdf = np.cumsum(pdf)
plt.plot(bins_count[1:], cdf, label="WebTunnel", linewidth = 2.5, color = 'royalblue')

plt.grid(color = 'grey', linestyle = '--', linewidth = 1)
plt.xlabel('Download time difference (s)', fontsize='x-large', fontweight='bold')
plt.ylabel('Fraction of values', fontsize='x-large', fontweight='bold')
plt.tight_layout()
plt.legend(loc='lower right', fontsize=15)
plt.savefig('../../w4', dpi = 600)
plt.show()

