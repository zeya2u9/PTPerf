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
	# for result_type in ["web_all", "blocked-all"]:
	for result_type in ["web_all"]:
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


#HERE HAVE TO ADD PT TYPE OVERALL AVERAGE
pt_types = {"proxy-layer" : [6,7,11,12], "tunneling" : [8,9,13], "mimicry" : [2,4,5], "fully-encrypted" : [1,3], "tor" : [0]}
union_db = {}

# here we have made a union db that will have results of all same type pts in one collection (kind of like all same type pts are one pt, so results are combined)
for pt_t in pt_types:
	union_db[pt_t] = {}
	for pt in pt_types[pt_t]:
		if pt not in db:
			continue
		for website in db[pt]:
			union_db[pt_t].setdefault(website, []).extend(db[pt][website])
			# union_db[pt_t][website] = ((union_db[pt_t][website] * len(union_db[pt_t][website])) + sum(db[pt][website])) / (len(db[pt][website]) + len(union_db[pt_t][website]))
			#hotchpotch, ignore (bask in the glory of)


#averages taken, structure now db {pt { website = val}}
for pt_t in union_db:
	for website in union_db[pt_t]:
		union_db[pt_t][website] = sum(union_db[pt_t][website]) / len(union_db[pt_t][website])



#now we have the final intersection list
os.system(f'mkdir -p pt-results/csvs/selenium-pairwise-by-pt-types/')

for pt_t1 in union_db:
	for pt_t2 in union_db:
		if (pt_t1 == pt_t2) or not(pt_t1 < pt_t2):
			continue
		master_weblist = []
		master_weblist.extend(union_db[pt_t1])
		master_weblist.extend(union_db[pt_t2])

		intersection_set = set()
		for website in master_weblist:
			if master_weblist.count(website) == 2:
				intersection_set.add(website)

		f = open(f"pt-results/csvs/selenium-pairwise-by-pt-types/Intersection_{pt_t1}-{pt_t2}_{y_axis_var}.csv", 'w')
		f.write("Websites")
		for pt_t in [pt_t1,pt_t2]:
			f.write(f",{pt_t}")
		f.write('\n')
		for website in intersection_set:
			f.write(website)
			for pt_t in [pt_t1,pt_t2]:
				f.write(f',{str(union_db[pt_t][website])}')
			f.write('\n')
		f.close()

print(f"pairwise csvs made in pt-results/csvs/selenium-pairwise-by-pt-types/ folder.")

# #############################################################################

