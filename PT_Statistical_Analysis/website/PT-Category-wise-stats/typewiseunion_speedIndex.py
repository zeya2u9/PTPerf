import pandas as pd
# import matplotlib.pyplot as plt
import numpy as np
import copy
import os

#TODO

# result_type = input("choose option: tranco-500 - blocked-200: ")
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
	# for result_type in ["tranco", "blocked"]:
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
						# db[pt][str(tmp[7*i])] = float(tmp[7*i + 4]) if y_axis_var == "Median" else float(tmp[7*i + 6])
						db[pt][str(tmp[7*i])] = (float(tmp[7*i + 4])*0.001) if y_axis_var == "Median" else (float(tmp[7*i + 6])*0.001)
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

#HERE HAVE TO ADD PT TYPE OVERALL AVERAGE
pt_types = {"proxy-layer" : [6,7,11,12], "tunneling" : [8,9,13], "mimicry" : [2,4,5], "fully-encrypted" : [1,3], "tor" : [0]}
union_db = {}

# here we have made a union db that will have results of all same type pts in one collection (kind of like all same type pts are one pt, so results are combined)
for pt_t in pt_types:
	union_db[pt_t] = {}
	counter = 0
	for pt in pt_types[pt_t]:
		if pt not in db:
			continue
		counter+=1
		for website in db[pt]:
			# union_db[pt_t].setdefault(website, 0).extend(db[pt][website])
			union_db[pt_t].setdefault(website, 0)
			union_db[pt_t][website] = ((union_db[pt_t][website]*(counter-1)) + db[pt][website]) / counter
			# union_db[pt_t].setdefault(website, 0) = ((union_db[pt_t].setdefault(website, 0)*(counter-1)) + db[pt][website]) / counter
			# union_db[pt_t][website] = ((union_db[pt_t][website] * len(union_db[pt_t][website])) + sum(db[pt][website])) / (len(db[pt][website]) + len(union_db[pt_t][website]))
			#hotchpotch, ignore (bask in the glory of)


# #averages taken, structure now db {pt { website = val}}
# for pt_t in union_db:
# 	for website in union_db[pt_t]:
# 		union_db[pt_t][website] = sum(union_db[pt_t][website]) / len(union_db[pt_t][website])



#now we have the final intersection list
os.system(f'mkdir -p pt-results/csvs/si-pairwise-by-pt-types/')

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

		f = open(f"pt-results/csvs/si-pairwise-by-pt-types/Intersection_{pt_t1}-{pt_t2}_{y_axis_var}.csv", 'w')
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

print(f"pairwise csvs made in pt-results/csvs/si-pairwise-by-pt-types/ folder.")

