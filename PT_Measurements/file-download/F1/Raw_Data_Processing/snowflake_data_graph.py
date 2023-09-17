import os
from pandas import *
from matplotlib import pyplot as plt
import json
from math import nan, isnan
import statistics
import numpy as np
import matplotlib.dates as mdates
import datetime

base_dir = 'F1/Raw_Data_Processing/'
data = {}

os.chdir(base_dir)
file_data = read_csv('userstats-bridge-transport-multi.csv')
data['date'] = []
data['date'].extend(file_data['date'].to_list())
#data['date'] = to_datetime(data['date'], format = '%Y-%m-%d')
#data['date'] = list(filter(lambda x: isnan(x) == False, data['date']))
data['users'] = []
data['users'].extend((file_data['users']*(file_data['num_instances']/file_data['coverage'])).to_list())
#data['users'] = list(filter(lambda x: isnan(x) == False, data['users']))



plt.rcParams["axes.linewidth"] = 1.5
plt.rcParams['xtick.major.size'] = 5
plt.rcParams['xtick.major.width'] = 2
plt.rcParams['ytick.major.size'] = 5
plt.rcParams['ytick.major.width'] = 2
#plt.rcParams["figure.figsize"] = (5,4)
# x_vals = [data['date'][0], data['date'][50]]
# dates = matplotlib.dates.date2num(x_vals)
datelist = [data['date'][i] for i in range(0, len(data['date'])+1, 30)]
print(datelist)
converted_dates = [datetime.datetime.strptime(i,'%Y-%m-%d').date() for i in datelist]
#converted_dates = list(map(datetime.datetime.strptime, datelist, len(datelist)*['%Y-%m-%d']))
print(converted_dates)
x_axis = converted_dates
myfmt = mdates.DateFormatter('%d-%b-%Y')
plt.gca().xaxis.set_major_formatter(myfmt)

p = plt.plot(data['date'], data['users'], linewidth = 2.5, color = 'crimson')
plt.xticks([i for i in range(0, len(data['date'])+1, 30)], x_axis, rotation = 25, fontsize=12, \
    weight = 'bold', ha = 'center')#, rotation_mode='anchor')
plt.yticks(weight = 'bold', fontsize=12)
# plt.gcf().autofmt_xdate()



plt.grid(color = 'grey', linestyle = '--', linewidth = 0.5)
# plt.xlabel('Time', fontsize='x-large', fontweight='bold')
plt.ylabel('Average simultaneous users', fontsize='x-large', fontweight='bold')
plt.tight_layout()
#plt.legend(loc='lower right', fontsize=15)
plt.savefig('../../sf1', dpi = 600)
plt.show()

