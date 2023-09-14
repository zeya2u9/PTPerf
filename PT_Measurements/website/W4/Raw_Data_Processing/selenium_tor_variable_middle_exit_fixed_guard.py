import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy
import os
import time
from scipy.interpolate import interp1d


def shape(lst):
	length = len(lst)
	shp = tuple(shape(sub) if isinstance(sub, list) else 0 for sub in lst)
	if any(x != 0 for x in shp):
		return length, shp
	else:
		return length

zero_copy = [0]*14

flag = 1
loc_list = [  'circuitx']
pt_names = [  'M1-E1', 'M2-E2', 'M3-E3', 'M4-E4']


result_type = input("choose option: tranco - blocked: ")
y_axis_var = input("enter eval criteria: Download_Size - Download_Speed - Total_Time : ")


avg_name_list = []
result = []

##############saving download times in a single csv file#####################
tor_data = pd.DataFrame(columns=['M1','C1','M2','C2','M3','C3','M4','C4'])
print("Dataframe created")

for locx in loc_list:
	location = locx
	avg_name = 'avg_t_for_pts_'+location
	avg_name_list.append(avg_name)
	#calculate num of lines in a file and store in count
	try:
		with open(r"~/selenium_tor_fixed_guard_diff_pairs_of_middle_exit/{0}/{1}/result_web1/n-trf-tr0.txt".format(location, result_type), 'r') as fp:
			for count, line in enumerate(fp):
				# print("first read all good")
				pass
	except Exception as e:
		with open(r"~/selenium_tor_fixed_guard_diff_pairs_of_middle_exit/{0}/{1}/result_web1/n-trf-tr1.txt".format(location, result_type), 'r') as fp:
			for count, line in enumerate(fp):
				# print("read issue 2")
				pass

	# open files
	# print(count)
	# time.sleep(10)
	fd = {}
	for i in range(1,3):
		fd["rw{0}".format(i)] = {}

	for x in range(1,3):
		for y in range(0, 4):
			try:
				fd["rw{0}".format(x)]["f{0}".format(y)] = open(r"~/selenium_tor_fixed_guard_diff_pairs_of_middle_exit/{2}/{3}/result_web{0}/n-trf-tr{1}.txt".format(x, y, location, result_type), 'r')
			except Exception as e:
				pass

	websites = []
	dl_size = []
	dl_speed = []
	total_time = []
	circuitCount = []
	# create db
	# db can easily be converted to a DataFrame, if needed
	# contains multiple iterations (rw{})
	db = {}
	for i in range(1,3):
		db["rw{}".format(i)] = {}

	# main loop
	# print("This is count:", count)
	csv_c = [0,0,0,0,0,0,0,0] #,0,0,0,0,0,0,0,0,0,0,0,0]
	for y in range(1,3):
		#for multiple result its
		for x in range(4):
			if x in [1,2,3,4]:
				c = 3*x + 1
			else:
				c = x
			try:
				tmpx = fd["rw{0}".format(y)]["f{0}".format(x)].read()
			except:
				continue
			tmp = tmpx.split()
			websites.clear()
			dl_size.clear()
			dl_speed.clear()
			total_time.clear()
			circuitCount.clear()
			for i in range(((count)//2) + 1):
				try:
					websites.append(str(tmp[11*i]))
					# print(f"Website: {str(tmp[8*i +1])} Y(folder):{y}  X(pt):{x}\n")
					dl_size.append(int(tmp[11*i + 4]))
					total_time.append(float(tmp[11*i + 7]))
					tor_data.loc[csv_c[x], c] = float(tmp[11*i + 7])
					circuitCount.append(int(tmp[11*i + 10]))
					tor_data.loc[csv_c[x], c+1] = float(tmp[11*i + 10])
					csv_c[x] = csv_c[x] + 1
					# print(f"Checking circuitCount: {int(tmp[11*i + 10])}")
					#print(f"total_time: {str(tmp[8*i +7])} Y(folder):{y}  X(pt):{x}\n")
					dl_speed.append(float(dl_size[-1]/total_time[-1]))
				except Exception as e:
					pass
				
				
			db["rw{}".format(y)]["db{0}".format(x)] = {"Website":copy.deepcopy(websites),"Download_Size":copy.deepcopy(dl_size),"Download_Speed":copy.deepcopy(dl_speed), "Total_Time":copy.deepcopy(total_time), "circuitCount":copy.deepcopy(circuitCount)}

	###save dataFrame to csv
	tor_data.to_csv("tor_guard_diff_middle_exit_pairs.csv")
	print(db)
	#exit(1)

	avg_name = []
	for i in range(4):
		avg_name.append([])

	# print(f"{y_axis_var}")
	# exit(1)
	for x in range(4):
		try:    
			for z in range(len(db["rw1"]["db{}".format(x)][y_axis_var])):
				avgsum = 0
				avgdiv = 0
				for y in range(1,3):
					try:
						#if (db["rw{}".format(y)]["db{}".format(x)]["Total_Time"][z] > 31 or db["rw{}".format(y)]["db{}".format(x)]["Total_Time"][z] < 30) and db["rw{}".format(y)]["db{}".format(x)]["Total_Time"][z] < 120:
						#removing failed downloads (120 sec) and circuitCount > 1 in tor/webTunnel
						#hard-coded format(0) since we do not want to include downloads with more than one circuit count in either Tor or Obfs4
						exp_and = ( (db["rw{}".format(y)]["db{}".format(0)]["circuitCount"][z] == 1) and (db["rw{}".format(y)]["db{}".format(1)]["circuitCount"][z] == 1) and (db["rw{}".format(y)]["db{}".format(2)]["circuitCount"][z] == 1) and (db["rw{}".format(y)]["db{}".format(3)]["circuitCount"][z] == 1)) # and (db["rw{}".format(y)]["db{}".format(4)]["circuitCount"][z] == 1) and (db["rw{}".format(y)]["db{}".format(5)]["circuitCount"][z] == 1) and (db["rw{}".format(y)]["db{}".format(6)]["circuitCount"][z] == 1) and (db["rw{}".format(y)]["db{}".format(7)]["circuitCount"][z] == 1) and (db["rw{}".format(y)]["db{}".format(8)]["circuitCount"][z] == 1) and (db["rw{}".format(y)]["db{}".format(9)]["circuitCount"][z] == 1) )
						#removing downloads with size 0 even if th circuitCount is 1
						exp_and_size = ( (db["rw{}".format(y)]["db{}".format(0)]["Download_Size"][z] > 0) and (db["rw{}".format(y)]["db{}".format(1)]["Download_Size"][z] > 0) and (db["rw{}".format(y)]["db{}".format(2)]["Download_Size"][z] > 0) and (db["rw{}".format(y)]["db{}".format(3)]["Download_Size"][z] > 0)) # and (db["rw{}".format(y)]["db{}".format(4)]["Download_Size"][z] > 0) and (db["rw{}".format(y)]["db{}".format(5)]["Download_Size"][z] > 0) and (db["rw{}".format(y)]["db{}".format(6)]["Download_Size"][z] > 0) and (db["rw{}".format(y)]["db{}".format(7)]["Download_Size"][z] > 0) and (db["rw{}".format(y)]["db{}".format(8)]["Download_Size"][z] > 0) and (db["rw{}".format(y)]["db{}".format(9)]["Download_Size"][z] > 0) )
						exp_and_30 = ( (31 < db["rw{}".format(y)]["db{}".format(0)]["Total_Time"][z] or db["rw{}".format(y)]["db{}".format(0)]["Total_Time"][z] < 30) and 
							(31 < db["rw{}".format(y)]["db{}".format(1)]["Total_Time"][z] or db["rw{}".format(y)]["db{}".format(1)]["Total_Time"][z] < 30) and 
							(31 < db["rw{}".format(y)]["db{}".format(2)]["Total_Time"][z] or db["rw{}".format(y)]["db{}".format(2)]["Total_Time"][z] < 30) and 
							(31 < db["rw{}".format(y)]["db{}".format(3)]["Total_Time"][z] or db["rw{}".format(y)]["db{}".format(3)]["Total_Time"][z] < 30))
						exp_and_120 = (db["rw{}".format(y)]["db{}".format(0)]["Total_Time"][z] < 120) and (db["rw{}".format(y)]["db{}".format(0)]["Total_Time"][z] < 120) and (db["rw{}".format(y)]["db{}".format(2)]["Total_Time"][z] < 120) and (db["rw{}".format(y)]["db{}".format(3)]["Total_Time"][z] < 120) 
						
						fin_exp = exp_and and exp_and_size and exp_and_30 and exp_and_120
						# db["rw{}".format(y)]["db{}".format(x)]["Total_Time"][z] < 120 and 
						if (fin_exp == 1): 
						# and ((db["rw{}".format(y)]["db{}".format(0)]["circuitCount"][z] == 1) and (db["rw{}".format(y)]["db{}".format(1)]["circuitCount"][z] == 1)):                        
							print(db["rw{}".format(y)]["db{}".format(x)][y_axis_var][z])
							avgsum += db["rw{}".format(y)]["db{}".format(x)][y_axis_var][z]
							avgdiv += 1
					except:
						pass
				if avgdiv == 0: #it removes the outliers reaching to 60 sec in the image
					avg_name[x].append(0)
					# print(avg_name[x])
				else:
					avg = avgsum/avgdiv
					avg_name[x].append(avg)
		except Exception as e:
			print(f"Error: {e}")
			pass

	if result_type == "Total_Time":
		for i in range(4):
			avg_name[i] = [j for j in avg_name[i] if ((j > 1) and (j!=0))] # only valid for total time, remove this for TTFB
	else:
		for i in range(4):
			avg_name[i] = [j for j in avg_name[i] if ((j!=0))]
	# print(avg_name)
	# t =[avg_name]
	# for i in range(11):
	#     if len(avg_name[i]) == 0:
	#         avg_name[i] = zero_copy
	# print(shape(avg_name))
	result.append(avg_name)

	medians = {}
	for i in range(4):
		medians["{}".format(pt_names[i])] = np.median(avg_name[i])

	medians_df = pd.DataFrame(medians, index = [0])

temp = pd.DataFrame(columns=['M1-E1', 'M2-E2', 'M3-E3', 'M4-E4'],  index=[i for i in range(1,1001)])
print(len(result))

path = '/root/'
temp_list = [[0]*1]*4  #change 1 to 5 for 5 rounds
for i in range(4):
	

	avg_t_for_pts = []
	for j in range(len(result)):
		copy_ = result[j][i]
		
		if len(result[j][i]) == 0:
			avg_t_for_pts.append( zero_copy )
		else:
			avg_t_for_pts.append(result[j][i])
		
		##copy data to temp and save
		if len(copy_)>0:
			# print(shape(copy_))
			for k in range(len(copy_)):
				temp.iloc[k][0] = copy_[k]
	temp_list[i] = avg_t_for_pts[0]

#saving in a csv
for i in range(4):
	copy_ = temp_list[i]
	for k in range(len(copy_)):
		temp.iloc[k][i] = copy_[k]
temp.to_csv(f"{path}tor.csv")

ll = len(temp_list[0])-5
print(f"Size of temp_list: {ll}")
##standard deviation
for i in range(3):
	dev = np.std([temp_list[i][0:ll],temp_list[i+1][0:ll]])
	print(f"Std_dev between Gurad-{i+1} and Guard-{i+2}:: {dev}")


'''#################cdf
# NUM_COLORS = 20

# cm = plt.get_cmap('gist_rainbow')
clrs = ['violet','pink','cyan','yellow','black','magenta','yellow','red','green','blue']

# print()
for i in range(4):
	print(f"for middle-exit-node: {i+1}")
	x1, y1 = sorted(temp_list[i]), np.arange(len(temp_list[i])) / len(temp_list[i])
	cubic_interpolation_model = interp1d(x1, y1, kind = "cubic")
	plt.xlabel("Download Time in seconds")
	plt.ylabel("%tage fraction")
	plt.plot(x1, y1, label=f"M{i+1}-E{i+1}",color = clrs[i])
	plt.legend()
	# fig.set_color(cm(i//3*3.0/NUM_COLORS))
	# plt.show()
	# x2, y2 = sorted(temp_list[1]), np.arange(len(temp_list[1])) / len(temp_list[1])

# plt.plot(x1, y1)
# plt.plot(x2, y2)
plt.xscale('log')
plt.show()
'''
