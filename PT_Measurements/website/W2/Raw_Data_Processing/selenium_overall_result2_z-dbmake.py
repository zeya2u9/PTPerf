import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy
import os

#create the graph
fig = plt.figure()

location = input("location in server-client format: ")
result_type = input("choose option: tranco - blocked: ")
y_axis_var = input("enter eval criteria: Total_Time - Download_Speed : ")
zero_copy = [0]*1000
result = []

#calculate num of lines in a file and store in count
try:
    with open(r"selenium_overall_result1000/{0}/{1}/result_web1/n-trf-tr0.txt".format(location, result_type), 'r') as fp:
        for count, line in enumerate(fp):
            pass
except Exception as e:
    try:
        with open(r"selenium_overall_result1000/{0}/{1}/result_web1/n-trf-tr1.txt".format(location, result_type), 'r') as fp:
            for count, line in enumerate(fp):
                pass
    except Exception as e:
        try:
            with open(r"selenium_overall_result1000/{0}/{1}/result_web1/n-trf-tr3.txt".format(location, result_type), 'r') as fp:
                for count, line in enumerate(fp):
                    pass
        except Exception as e:
            try:
                with open(r"selenium_overall_result1000/{0}/{1}/result_web1/n-trf-tr4.txt".format(location, result_type), 'r') as fp:
                    for count, line in enumerate(fp):
                        pass
            except Exception as e:
                try:
                    with open(r"selenium_overall_result1000/{0}/{1}/result_web1/n-trf-tr5.txt".format(location, result_type), 'r') as fp:
                        for count, line in enumerate(fp):
                            pass
                except Exception as e:
                    try:
                        with open(r"selenium_overall_result1000/{0}/{1}/result_web1/n-trf-tr7.txt".format(location, result_type), 'r') as fp:
                            for count, line in enumerate(fp):
                                pass
                    except Exception as e:
                        with open(r"selenium_overall_result1000/{0}/{1}/result_web1/n-trf-tr13.txt".format(location, result_type), 'r') as fp:
                            for count, line in enumerate(fp):
                                pass

# open files
fd = {}
for i in range(1,6):
    fd["rw{0}".format(i)] = {}

for x in range(1,6):
    for y in range(0, 14):
        try:
            fd["rw{0}".format(x)]["f{0}".format(y)] = open(r"selenium_overall_result1000/{2}/{3}/result_web{0}/n-trf-tr{1}.txt".format(x, y, location, result_type), 'r')
        except Exception as e:
            print(f"Can not access file: {e}")

websites = []
dl_size = []
dl_speed = []
total_time = []
# create db
# db can easily be converted to a DataFrame, if needed
# contains multiple iterations (rw{})
db = {}
for i in range(1,6):
    db["rw{}".format(i)] = {}

# main loop
for y in range(1,6):
    #for multiple result its
    for x in range(0,14):
        # if x in [8]:
            # continue
        try:
            tmpx = fd["rw{0}".format(y)]["f{0}".format(x)].read()
        except:
            continue
        tmp = tmpx.split()
        websites.clear()
        dl_size.clear()
        dl_speed.clear()
        total_time.clear()
        for i in range((count)//2):
            try:
                websites.append(str(tmp[8*i]))
                # print(f"Website: {str(tmp[8*i +1])} Y(folder):{y}  X(pt):{x}\n")
                dl_size.append(int(tmp[8*i + 4]))
                total_time.append(float(tmp[8*i + 7]))
                # print(f"total_time: {str(tmp[8*i +7])} Y(folder):{y}  X(pt):{x}\n")
                dl_speed.append(float(dl_size[-1]/total_time[-1]))
            except Exception as e:
                pass
            
            
        db["rw{}".format(y)]["db{0}".format(x)] = {"Website":copy.deepcopy(websites),"Download_Size":copy.deepcopy(dl_size),"Download_Speed":copy.deepcopy(dl_speed), "Total_Time":copy.deepcopy(total_time)}


avg_t_for_pts = []
for i in range(14):
    avg_t_for_pts.append([])

for x in range(0,14): #for each pt
    try:    
        for z in range(len(db["rw1"]["db{}".format(x)][y_axis_var])): #for each website
            avgsum = 0
            avgdiv = 0
            for y in range(1,6):  #in each folder
                try:
                    if (db["rw{}".format(y)]["db{}".format(x)]["Total_Time"][z] > 31 or db["rw{}".format(y)]["db{}".format(x)]["Total_Time"][z] < 30) and db["rw{}".format(y)]["db{}".format(x)]["Total_Time"][z] < 120:
                        avgsum += db["rw{}".format(y)]["db{}".format(x)][y_axis_var][z]
                        avgdiv += 1
                except:
                    pass
            if avgdiv == 0: #it removes the outliers reaching to 60 sec in the image
                avg_t_for_pts[x].append(0)
            else:
                avg = avgsum/avgdiv
                avg_t_for_pts[x].append(avg)
    except Exception as e:
        print(f"Error: {e}")

for i in range(14):
    avg_t_for_pts[i] = [j for j in avg_t_for_pts[i] if ((j > 1) and (j!=0))]
result.append(avg_t_for_pts)


# if result_type == "Total_Time":
pt_names = [  'Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']
path = 'website/W2/'
temp = pd.DataFrame(columns=['Time'],  index=[i for i in range(1,1001)])
for i in range(0,14):
    
    #create a folder for this PT
    # os.system(f"mkdir {path}{pt_names[i]}")

    # avg_t_for_pts = []
    temp = pd.DataFrame(columns=['Time'],  index=[i for i in range(1,1001)])
    for j in range(len(result)):
        copy_ = result[j][i]
        
        # if len(result[j][i]) == 0:
        #     avg_t_for_pts.append( zero_copy )
        # else:
        #     avg_t_for_pts.append(result[j][i])
        
        ##copy data to temp and save
        if len(copy_)>0:
            # print(shape(copy_))
            for k in range(len(copy_)):
                temp.iloc[k][0] = copy_[k]
            temp.to_csv(f"{path}{pt_names[i]}.csv")
    


# os.system(f"mkdir {path}Massbrowser")
# for k in range(len(copy_)):
    # temp.iloc[k][0] = copy_[k]
# temp.to_csv(f"{path}Massbrowser/sfo.csv")



plt.boxplot([avg_t_for_pts[0], avg_t_for_pts[1], avg_t_for_pts[2], avg_t_for_pts[3], avg_t_for_pts[4], avg_t_for_pts[5], avg_t_for_pts[6], avg_t_for_pts[7], avg_t_for_pts[8], avg_t_for_pts[9], avg_t_for_pts[10], avg_t_for_pts[11], avg_t_for_pts[12], avg_t_for_pts[13]])
pt_names = [  'Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], pt_names)
plt.xlabel(f"Tor & diff. Pluggable Transports - loc:{location}")
plt.ylabel(y_axis_var)
plt.title(result_type)
plt.show()
medians = {}
for i in range(14):
    medians["{}".format(pt_names[i])] = np.median(avg_t_for_pts[i])

medians_df = pd.DataFrame(medians, index = [0])
print(medians_df)
