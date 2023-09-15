import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import copy
import os

#TODO
'''
choose one location
combine sites of both tranco and blocked in 1 dictionary with strcuture:
{"webite" : [results..., be it 2-3-4-5 whatever]}

this is for each PT separately
now you preen the dictionary for websites with <3 results
take the average of all the remaining results and store in this format:
{"website" : average result}
(may need to combine all types of results like TTFB, total_time etc)
store this dictionary in one csv and save

stop here for now
''' 

loc_list = [  'fra-blr', 'fra-lon','fra-tor','nyc-blr','nyc-lon','nyc-tor','sgp-blr','sgp-lon','sgp-tor', 'Tor-only-blr2', 'Tor-only-lon2', 'Tor-only-tor2' ]
print(loc_list)
location = input("location in server-client format: ")

# result_type = input("choose option: tranco-500 - blocked-200: ")
y_axis_var = input("enter eval criteria: Total_Time - Download_Speed - TTFB - TCP_connect: ")

pt_names = [  'Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']


blocked_list = open("/home/nsl400/autoScript/websiteList/url-lists/1000-websites.csv", 'r').read().split('\n')[:-1]
blocked_list = [x[:-1] for x in blocked_list]

tranco_list = open("/home/nsl400/autoScript/websiteList/tranco/tranco_bas_krdo.csv", 'r').read().split('\n')[1:1001]
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
	# for result_type in ["tranco-500", "blocked-200"]:
	for result_type in ["tranco-500"]:
		try:
			with open(r"/home/nsl400/pt-results/overall_result3/{0}/{1}/result_web1/n-trf-tr{2}.txt".format(location, result_type, pt), 'r') as fp:
				for count, line in enumerate(fp):
					pass
		except Exception as e:
			print(f"PT: {pt} not in this location, skipping...")
			continue

		# open files
		fd = {}
		camo_ke_nakhre = 6 if pt != 8 else 3
		for it in range(1,camo_ke_nakhre):
			try:
				fd["rw{0}".format(it)] = open(r"/home/nsl400/pt-results/overall_result3/{2}/{3}/result_web{0}/n-trf-tr{1}.txt".format(it, pt, location, result_type), 'r')
			except Exception as e:
				print(f"Can not access file: {e}")
				exit()

		websites = []
		dl_size = []
		dl_speed = []
		tcp_c = []
		ttfb = []
		total_time = []

		# main loop
		for y in range(1,camo_ke_nakhre):
			# input(f"PROCEED WITH {location} {pt_names[pt]} ITERATION {y} ?")
			#for multiple result its
			try:
				tmpx = fd["rw{0}".format(y)].read()
			except:
				continue	
			tmp = tmpx.split()
			websites.clear()
			dl_size.clear()
			dl_speed.clear()
			tcp_c.clear()
			ttfb.clear()
			total_time.clear()
			for i in range((count+1)//2):
				try:
					if 1 < float(tmp[12*i + 12]) < 57:
						db[pt][str(tmp[12*i +1])].append(float(tmp[12*i + 12]) if y_axis_var == "Total_Time" else float(tmp[12*i + 9]) if y_axis_var == "TTFB" else float(tmp[12*i + 5])) #default is dl_speed
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
print("now we preen the database for websites with results less than threshold")

thresh = int(input("minimum results? : "))

for pt in range(14):
	for website in db[pt].copy():
		if len(db[pt][website]) < thresh:
			# print(f"deleted {website} from {pt_names[pt]} result : count was {len(db[pt][website])}")
			del db[pt][website]
	if not bool(db[pt]):
		del db[pt]

print("\n\nPREENING DONE!")
print(f"taking averages of remaining results and creating result csvs in root folder. please check pt-results/csvs/{location}")


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

#writing to files
# os.system(f"mkdir -p /home/nsl400/pt-results/csvs/{location}")
# for pt_t in union_db:
# 	f = open(f"/home/nsl400/pt-results/csvs/{location}/{pt_names[pt]}_{y_axis_var}.csv", 'w')
# 	f.write("Websites,AvgMetric\n")
# 	for website in db[pt]:
# 		f.write(website+','+str(db[pt][website])+'\n')
# 	f.close()

# #calculating intersection
# master_weblist = []
# for pt in db:
# 	master_weblist.extend(db[pt])

# intersection_set = set()

# for website in master_weblist:
# 	if master_weblist.count(website) == len(db):
# 		intersection_set.add(website)

# # print(len(intersection_set))
# # input()
# # print(intersection_set)
# # exit()

# #now we have the final intersection list
# f = open(f"/home/nsl400/pt-results/csvs/{location}/Intersection_{y_axis_var}.csv", 'w')
# f.write("Websites")
# for pt in db:
# 	f.write(f",{pt_names[pt]}")
# f.write('\n')
# for website in intersection_set:
# 	f.write(website)
# 	for pt in db:
# 		f.write(f',{str(db[pt][website])}')
# 	f.write('\n')
# f.close()

# print("Intersection CSV made and saved in same folder.")

#############################################################################

#now we have the final intersection list
os.system(f'mkdir -p /home/nsl400/pt-results/csvs/pairwise-by-pt-types/{location}')

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

		f = open(f"/home/nsl400/pt-results/csvs/pairwise-by-pt-types/{location}/Intersection_{pt_t1}-{pt_t2}_{y_axis_var}.csv", 'w')
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

print(f"pairwise csvs made in /home/nsl400/pt-results/csvs/pairwise-by-pt-types/{location}/ folder.")

# print(len(intersection_set))
# input()
# print(intersection_set)
# exit()