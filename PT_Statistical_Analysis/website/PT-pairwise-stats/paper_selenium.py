import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import copy
import os

#TODO

# loc_list = [  'fra-blr', 'fra-lon','fra-tor','nyc-blr','nyc-lon','nyc-tor','sgp-blr','sgp-lon','sgp-tor', 'Tor-only-blr2', 'Tor-only-lon2', 'Tor-only-tor2' ]
# print(loc_list)
# location = input("location in server-client format: ")

# result_type = input("choose option: tranco-500 - blocked-200: ")
# y_axis_var = input("enter eval criteria: Total_Time - Download_Speed - TTFB - TCP_connect: ")
y_axis_var = "Total_Time"

pt_names = [  'Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']


blocked_list = open("websiteList/1000-websites.csv", 'r').read().split('\n')[:-1]
blocked_list = [x[:-1] for x in blocked_list]

tranco_list = open("websiteList/tranco_bas_krdo.csv", 'r').read().split('\n')[1:1001]
tranco_list = [x[:-1] for x in tranco_list]

all_websites = tranco_list
all_websites.extend(blocked_list)

# create db
# db can easily be converted to a DataFrame, if needed
# contains multiple iterations (rw{})
db = {}

# for location in loc_list:
for pt in range(14):
	db[pt] = {}
	for website in all_websites:
		db[pt][website] = []

	#calculate num of lines in a file and store in count
	# for result_type in ["tranco-500"]:
	for result_type in ["web_all", "blocked-all"]:
	# for result_type in ["web_all"]:
		try:
			with open(r"pt-results/selenium_results/selenium_overall_result1000/{0}/result_web1/n-trf-tr{1}.txt".format(result_type, pt), 'r') as fp:
				for count, line in enumerate(fp):
					pass
		except Exception as e:
			print(f"PT: {pt} not in this experiment, skipping...")
			continue

		# open files
		fd = {}
		# psiphon_ke_nakhre = 6 if (pt != 11 and result_type != "blocked-all") else 5
		for it in range(1,6):
			try:
				fd["rw{0}".format(it)] = open(r"pt-results/selenium_results/selenium_overall_result1000/{2}/result_web{0}/n-trf-tr{1}.txt".format(it, pt,  result_type), 'r')
			except Exception as e:
				print(f"Can not access file: {e}")
				exit()

		websites = []
		dl_size = []
		# dl_speed = []
		# tcp_c = []
		# ttfb = []
		total_time = []

		# main loop
		for y in range(1,6):
			# input(f"PROCEED WITH {location} {pt_names[pt]} ITERATION {y} ?")
			#for multiple result its
			try:
				tmpx = fd["rw{0}".format(y)].read()
			except:
				continue	
			tmp = tmpx.split()
			websites.clear()
			dl_size.clear()
			# dl_speed.clear()
			# tcp_c.clear()
			# ttfb.clear()
			total_time.clear()
			for i in range((count)//2):
				try:
					#if (db["rw{}".format(y)]["db{}".format(x)]["Total_Time"][z] > 31 or db["rw{}".format(y)]["db{}".format(x)]["Total_Time"][z] < 30) and db["rw{}".format(y)]["db{}".format(x)]["Total_Time"][z] < 120:
					if (float(tmp[8*i + 7]) > 31 or float(tmp[8*i + 7]) < 30) and (float(tmp[8*i + 7]) < 120) and (float(tmp[8*i + 7]) > 1):
						db[pt][str(tmp[8*i])].append(float(tmp[8*i + 7]))

				except Exception as e:
					pass

print("DATABASE COMPLETE!")
print("now we preen the database for websites with results less than threshold")

# input()
# print(db)
# exit()

thresh = int(input("minimum results? : "))

for pt in range(14):
	for website in db[pt].copy():
		if len(db[pt][website]) < thresh:
			# print(f"deleted {website} from {pt_names[pt]} result : count was {len(db[pt][website])}")
			del db[pt][website]
	if not bool(db[pt]):
		del db[pt]

print("\n\nPREENING DONE!")
print(f"taking averages of remaining results and creating result csvs in root folder. please check pt-results/csvs/selenium/")

#averages taken, structure now db {pt { website = val}}
for pt in db:
	for website in db[pt]:
		db[pt][website] = sum(db[pt][website]) / len(db[pt][website])

#writing to files
os.system(f"mkdir -p pt-results/csvs/selenium")
for pt in db:
	f = open(f"pt-results/csvs/selenium/{pt_names[pt]}_{y_axis_var}.csv", 'w')
	f.write("Websites,AvgMetric\n")
	for website in db[pt]:
		f.write(website+','+str(db[pt][website])+'\n')
	f.close()

#calculating intersection
master_weblist = []
for pt in db:
	if pt == 2:
		continue
	master_weblist.extend(db[pt])

intersection_set = set()

for website in master_weblist:
	if master_weblist.count(website) == len(db)-1:
		intersection_set.add(website)

# print(len(intersection_set))
# input()
# print(intersection_set)
# exit()

#now we have the final intersection list
f = open(f"pt-results/csvs/selenium/Intersection_{y_axis_var}_wo_M.csv", 'w')
f.write("Websites")
for pt in db:
	if pt == 2:
		continue
	f.write(f",{pt_names[pt]}")
f.write('\n')
for website in intersection_set:
	f.write(website)
	for pt in db:
		if pt == 2:
			continue
		f.write(f',{str(db[pt][website])}')
	f.write('\n')
f.close()

print("Intersection CSV made and saved in same folder.")

#############################################################################

#now we have the final intersection list
os.system(f'mkdir -p pt-results/csvs/pairwise/selenium')

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

		f = open(f"pt-results/csvs/pairwise/selenium/Intersection_{pt_names[pt1]}-{pt_names[pt2]}_{y_axis_var}.csv", 'w')
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

print(f"pairwise csvs made in pt-results/csvs/pairwise/selenium/ folder.")

# print(len(intersection_set))
# input()
# print(intersection_set)
# exit()
