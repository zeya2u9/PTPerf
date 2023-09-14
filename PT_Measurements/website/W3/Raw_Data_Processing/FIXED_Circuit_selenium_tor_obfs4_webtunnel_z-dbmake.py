import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy
import os
import time



def shape(lst):
    length = len(lst)
    shp = tuple(shape(sub) if isinstance(sub, list) else 0 for sub in lst)
    if any(x != 0 for x in shp):
        return length, shp
    else:
        return length

zero_copy = [0]*14

flag = 1
loc_list = [  'loc1']
pt_names = [  'Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']


result_type = 'tranco'  #input("choose option: tranco-500 - blocked-200: ")
y_axis_var = 'Total_Time'  #input("enter eval criteria: Download_Size - Download_Speed - Total_Time : ")


avg_name_list = []
result = []

##############saving download times in a single csv file#####################
column_names = ['Time_tor', 'circuitCount_tor', 'Time_Obfs4','circuitCount_Obfs4', 'Time_WebTunnel', 'circuitCount_webTunnel']
column_index = {0: ['Time_tor','circuitCount_tor'], 1:['Time_Obfs4', 'circuitCount_Obfs4'] , 13:['Time_WebTunnel', 'circuitCount_webTunnel'] }
tor_obfs4 = pd.DataFrame(columns=column_names)
print("Dataframe created")

for locx in loc_list:
    location = locx
    avg_name = 'avg_t_for_pts_'+location
    avg_name_list.append(avg_name)
    #calculate num of lines in a file and store in count
    try:
        with open(r"~/{0}/{1}/result_web1/n-trf-tr0.txt".format(location, result_type), 'r') as fp:
            for count, line in enumerate(fp):
                # print("first read all good")
                # fp.close()
                pass
    except Exception as e:
        with open(r"~/{0}/{1}/result_web1/n-trf-tr1.txt".format(location, result_type), 'r') as fp:
            for count, line in enumerate(fp):
                # print("read issue 2")
                # fp.close()
                pass

    # open files
    # print(count)
    # time.sleep(10)
    fd = {}
    for i in range(1,501):
        fd["rw{0}".format(i)] = {}

    for x in range(1,501):
        for y in range(0, 14):
            try:
                fd["rw{0}".format(x)]["f{0}".format(y)] = open(r"~/{2}/{3}/result_web{0}/n-trf-tr{1}.txt".format(x, y, location, result_type), 'r')
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
    for i in range(1,501):
        db["rw{}".format(i)] = {}

    # main loop
    # print("This is count:", count)
    #create dataframe to store values
    # data_x = pd.DataFrame(columns=['Tor','Tor_circuit_count','Obfs4','Obfs4_circuit_count'])

    entry = 0
    for y in range(1,501):
        #for multiple result its

        for x in range(14):
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
                    
                    if x in [0, 1, 13]:
                        index_v = f"{(y-1)*5+i}"
                        tor_obfs4.at[index_v, f"{list(column_index[x])[0]}"] = float(tmp[11*i + 7])
                        tor_obfs4.at[index_v, f"{list(column_index[x])[1]}"] = float(tmp[11*i + 10])
                        entry = entry + 1


                    # tor_obfs4.loc[csv_c[x], c] = float(tmp[11*i + 7])
                    # circuitCount.append(int(tmp[11*i + 10]))
                    # tor_obfs4.loc[csv_c[x], c+1] = float(tmp[11*i + 10])
                    # csv_c[x] = csv_c[x] + 1

                    # print(f"Checking circuitCount: {int(tmp[11*i + 10])}")
                    #print(f"total_time: {str(tmp[8*i +7])} Y(folder):{y}  X(pt):{x}\n")
                    dl_speed.append(float(dl_size[-1]/total_time[-1]))
                except Exception as e:
                    pass
                
            fd["rw{0}".format(y)]["f{0}".format(x)].close()    
            db["rw{}".format(y)]["db{0}".format(x)] = {"Website":copy.deepcopy(websites),"Download_Size":copy.deepcopy(dl_size),"Download_Speed":copy.deepcopy(dl_speed), "Total_Time":copy.deepcopy(total_time), "circuitCount":copy.deepcopy(circuitCount)}
            
    tor_obfs4.to_csv(f"tor_obfs4_webTunnel_2500_count_sep2.csv", index=False)
    # print(db)
    print(len(tor_obfs4))

    print(int(entry/3))

    ###make pairwise csv
    pairwise = {0:'Tor-Obfs4', 1:'Tor-WebTunnel', 13:'Obfs4-WebTunnel'}
    for i in [0,1,13]:
        for k in [0, 1 ,13]:
            if i == k or i>k:
                continue
            data = pd.DataFrame(columns=[f"{pt_names[i]}", f"{pt_names[k]}"])
            data_index = 0
            for j in range(int(entry/3)):
                if tor_obfs4.at[f"{j}", f"{list(column_index[i])[1]}"] == 1 and tor_obfs4.at[f"{j}", f"{list(column_index[k])[1]}"] == 1:  #check circuit count ==1
                    if (tor_obfs4.at[f"{j}", f"{list(column_index[i])[0]}"]) < 120 and (tor_obfs4.at[f"{j}", f"{list(column_index[k])[0]}"]) < 120:                    
                        tt = f"{data_index}"
                        data.at[tt, f"{pt_names[i]}"] = tor_obfs4.at[f"{j}", f"{list(column_index[i])[0]}"] 
                        data.at[tt, f"{pt_names[k]}"] = tor_obfs4.at[f"{j}", f"{list(column_index[k])[0]}"] 
                        data_index = data_index + 1
            

            data.to_csv(f"~/pairwise/{pt_names[i]}-{pt_names[k]}.csv", index=False)

    ##########for pairwise in all three circuits csv
    for i in [0,1,13]:
        for k in [0, 1 ,13]:
            if i == k or i>k:
                continue
            data = pd.DataFrame(columns=[f"{pt_names[i]}", f"{pt_names[k]}"])
            data_index = 0
            for j in range(int(entry/3)):
                if tor_obfs4.at[f"{j}", "circuitCount_tor"] <= 2 and (tor_obfs4.at[f"{j}", "circuitCount_Obfs4"] <= 2 and tor_obfs4.at[f"{j}", "circuitCount_webTunnel"] <= 2) :  #check circuit count ==1
                    if (tor_obfs4.at[f"{j}", "Time_tor"]) < 120 and ( (tor_obfs4.at[f"{j}", "Time_Obfs4"]) < 120 and (tor_obfs4.at[f"{j}", "Time_WebTunnel"]) < 120 ):                    
                        tt = f"{data_index}"
                        data.at[tt, f"{pt_names[i]}"] = tor_obfs4.at[f"{j}", f"{list(column_index[i])[0]}"] 
                        data.at[tt, f"{pt_names[k]}"] = tor_obfs4.at[f"{j}", f"{list(column_index[k])[0]}"] 
                        data_index = data_index + 1
            

            data.to_csv(f"~/pairwis_same_circuit_in_all_three/{pt_names[i]}-{pt_names[k]}.csv", index=False)



    exit(1)
