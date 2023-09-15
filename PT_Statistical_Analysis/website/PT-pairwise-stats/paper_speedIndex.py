import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import copy
import os

#TODO

y_axis_var = input("enter eval criteria: SpeedIndex (milli-seconds) Median Mean: ")

pt_names = [  'Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']


tranco_list = open("websiteList/tranco_bas_krdo.csv", 'r').read().split('\n')[1:1001]
tranco_list = [x[:-1] for x in tranco_list]

all_websites = tranco_list
# all_websites.extend(blocked_list)

# create db
# db can easily be converted to a DataFrame, if needed
# contains multiple iterations (rw{})
db = {}

# for location in loc_list:
for pt in range(14):
	db[pt] = {}


	#calculate num of lines in a file and store in count
	# for result_type in ["tranco-500", "blocked-200"]:
	for result_type in ["tranco"]:
		try:
			with open(r"pt-results/speed_index/result_web_combine/n-trf-tr{0}.txt".format(pt), 'r') as fp:
				for count, line in enumerate(fp):
					pass
		except Exception as e:
			print(f"PT: {pt} not in this location, skipping...")
			continue

		# open files
		fd = {}
		camo_ke_nakhre = 6 if pt != 8 else 3
		for it in range(1,camo_ke_nakhre): ##############################################################
			try:
				fd["rw{0}".format(it)] = open(r"pt-results/speed_index/result_web_combine/n-trf-tr{0}.txt".format(pt), 'r')
			except Exception as e:
				print(f"Can not access file: {e}")
				exit()

		# main loop
		for y in range(1,camo_ke_nakhre):
			# input(f"PROCEED WITH {location} {pt_names[pt]} ITERATION {y} ?")
			#for multiple result its
			try:
				tmpx = fd["rw{0}".format(y)].read()
			except:
				continue	
			tmp = tmpx.split()

			for i in range((count+1)//2):
				try:
					if float(tmp[7*i + 4]) > 0: #################################
						db[pt][str(tmp[7*i])] = float(tmp[7*i + 4]) if y_axis_var == "Median" else float(tmp[7*i + 6])
					# websites.append(str(tmp[12*i +1]))
					# dl_size.append(int(tmp[12*i + 3]))
					# dl_speed.append(float(tmp[12*i + 5]))
					# tcp_c.append(float(tmp[12*i + 7]))
					# #print(tmp[12*i + 9])
					# ttfb.append(float(tmp[12*i + 9]))
					# total_time.append(float(tmp[12*i + 12]))
				except Exception as e:
					# print(f"Error:: {e}\n in {str((tmp[12*i + 3]))} for website {str(tmp[12*i +1])}")
					pass


print("DATABASE COMPLETE!")
# print("now we preen the database for websites with results less than threshold")

# thresh = int(input("minimum results? : "))

for pt in range(14):
	# for website in db[pt].copy():
	# 	if len(db[pt][website]) < thresh:
	# 		print(f"deleted {website} from {pt_names[pt]} result : count was {len(db[pt][website])}")
	# 		del db[pt][website]
	if not bool(db[pt]):
		del db[pt]

# print("\n\nPREENING DONE!")
# print(f"taking averages of results and creating result csvs in root folder. please check pt-results/csvs/speedindex")

# #averages taken, structure now db {pt { website = val}}
# for pt in db:
# 	for website in db[pt]:
# 		db[pt][website] = sum(db[pt][website]) / len(db[pt][website])

#writing to files
os.system(f"mkdir -p pt-results/csvs/speedindex")
for pt in db:
	f = open(f"pt-results/csvs/speedindex/{pt_names[pt]}_{y_axis_var}.csv", 'w')
	f.write("Websites,Metric\n")
	for website in db[pt]:
		f.write(website+','+str(db[pt][website])+'\n')
	f.close()

#calculating intersection
master_weblist = []
for pt in db:
	if pt == 2 or pt == 6:
		continue
	master_weblist.extend(db[pt])

intersection_set = set()

for website in master_weblist:
	if master_weblist.count(website) == len(db)-2:
		intersection_set.add(website)

# print(len(intersection_set))
# input()
# print(intersection_set)
# exit()

#now we have the final intersection list
f = open(f"pt-results/csvs/speedindex/Intersection_{y_axis_var}.csv", 'w')
f.write("Websites")
for pt in db:
	if pt == 2 or pt == 6:
		continue
	f.write(f",{pt_names[pt]}")
f.write('\n')
for website in intersection_set:
	f.write(website)
	for pt in db:
		if pt == 2 or pt == 6:
			continue
		f.write(f',{str(db[pt][website])}')
	f.write('\n')
f.close()

print("Intersection CSV made and saved in same folder.")


#############################################################################

#now we have the final intersection list
os.system(f'mkdir -p pt-results/csvs/pairwise/speedindex')

for pt1 in db:
	for pt2 in db:
		if (pt1 == pt2) or not(pt1 < pt2):
			continue
		master_weblist = []
		master_weblist.extend(db[pt1])
		master_weblist.extend(db[pt2])

		intersection_set = set()
		for website in master_weblist:
			if master_weblist.count(website) == 2:
				intersection_set.add(website)

		f = open(f"pt-results/csvs/pairwise/speedindex/Intersection_{pt_names[pt1]}-{pt_names[pt2]}_{y_axis_var}.csv", 'w')
		f.write("Websites")
		for pt in [pt1,pt2]:
			f.write(f",{pt_names[pt]}")
		f.write('\n')
		for website in intersection_set:
			f.write(website)
			for pt in [pt1,pt2]:
				f.write(f',{str(db[pt][website])}')
			f.write('\n')
		f.close()

print(f"pairwise csvs made in pt-results/csvs/pairwise/speedindex/ folder.")
