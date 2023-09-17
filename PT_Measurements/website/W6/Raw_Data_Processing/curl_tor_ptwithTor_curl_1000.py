import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy
import os
import time


#ISSUES
'''
- some PT files not present 0 1 6 7 8 10 12
'''


def shape(lst):
    length = len(lst)
    shp = tuple(shape(sub) if isinstance(sub, list) else 0 for sub in lst)
    if any(x != 0 for x in shp):
        return length, shp
    else:
        return length

zero_copy = [0]*14

flag = 1
# loc_list = [  'obfs4', 'marionette', 'shadowsocks', 'stegotorus', 'cloak', 'dnstt', 'psiphon', 'webTunnel']
loc_list = [  'obfs4',  'marionette', 'shadowsocks', 'stegotorus', 'cloak', 'dnstt', 'psiphon', 'webTunnel']
loc_list_i = [1,2, 3, 4,5, 9,11, 13]
pt_names = [  'Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']


result_type = 'tranco-500'
# y_axis_var = input("enter eval criteria: Download_Size - Download_Speed - Total_Time - TTFB - Connect : ")
y_axis_var = 'Total_Time'
pt_name = input("enter pt name to be evaluated: obfs4, marionette, shadowsocks, stegotorus, cloak, dnstt, psiphon, webTunnel: ")


avg_name_list = []
result = []

##############saving download times in a single csv file#####################
tor_obfs4 = pd.DataFrame(columns=['Time_tor', 'Time_obfs4'])


for locx in loc_list:
    location = locx
    avg_name = 'avg_t_for_pts_'+location
    avg_name_list.append(avg_name)
    ind = [0, loc_list_i[loc_list.index(location)]]
    #calculate num of lines in a file and store in count
    try:
        with open(r"/home/nsl300/Documents/curl_Tor_PTwithTor_same_circuit_tranco-1000/{0}/result_web1/n-trf-tr0.txt".format(location), 'r') as fp:
            for count, line in enumerate(fp):
                # print("first read all good")
                pass
    except Exception as e:
        print('-------------------------------------here--------------------------------------')
        with open(r"/home/nsl300/Documents/curl_Tor_PTwithTor_same_circuit_tranco-1000/{0}/result_web1/n-trf-tr1.txt".format(location), 'r') as fp:
            for count, line in enumerate(fp):
                print("read issue 2")
                pass


    # open files
    fd = {}
    for i in range(1,6):
        fd["rw{0}".format(i)] = {}

    for x in range(1,6):
        for y in range(0, 2):
            try:
                fd["rw{0}".format(x)]["f{0}".format(y)] = open(r"/home/nsl300/Documents/curl_Tor_PTwithTor_same_circuit_tranco-1000/{2}/result_web{0}/n-trf-tr{1}.txt".format(x, ind[y], location), 'r')
            except Exception as e:
                print("reading issue")

                pass


    websites = []
    dl_size = []
    dl_speed = []
    total_time = []
    tcp_c = []
    ttfb = []
    circuitCount = []
    # create db
    # db can easily be converted to a DataFrame, if needed
    # contains multiple iterations (rw{})
    db = {}
    for i in range(1,6):
        db["rw{}".format(i)] = {}

    # main loop
    # print("This is count:", count)
    csv_c = [0,0]
    for y in range(1,6):  #for multiple result its
        for x in range(0,2):
            try:
                tmpx = fd["rw{0}".format(y)]["f{0}".format(x)].read()
            except:
                continue
            tmp = tmpx.split()
            websites.clear()
            dl_size.clear()
            dl_speed.clear()
            total_time.clear()
            tcp_c.clear()
            ttfb.clear()
            circuitCount.clear()
            for i in range(((count)//2) + 1):
                try:
                    websites.append(str(tmp[15*i]))
                    dl_size.append(int(tmp[15*i + 2]))
                    dl_speed.append(float(tmp[15*i + 4]))
                    tcp_c.append(float(tmp[15*i + 6]))
                    ttfb.append(float(tmp[15*i + 8]))
                    total_time.append(float(tmp[15*i + 11]))
                    circuitCount.append(float(tmp[15*i + 14]))
                except Exception as e:
                    pass
                                
            db["rw{}".format(y)]["db{0}".format(x)] = {"Website":copy.deepcopy(websites),"Download_Size":copy.deepcopy(dl_size),"Download_Speed":copy.deepcopy(dl_speed), 
            "Total_Time":copy.deepcopy(total_time), "Connect":copy.deepcopy(tcp_c), "TTFB":copy.deepcopy(ttfb), "Circuit_Count":copy.deepcopy(circuitCount)}

    ####save dataFrame to csv
    # tor_obfs4.to_csv(f"/home/nsl300/Documents/selenium_tor_obfs4_same_circuit_2500/tor_obfs4_2500.csv")
    # print(db)
    # exit(1)

    avg_name = []
    for i in range(2):
        avg_name.append([])

    for x in range(0,2):
        try:    
            for z in range(len(db["rw1"]["db{}".format(x)][y_axis_var])):
                avgsum = 0
                avgdiv = 0
                for y in range(1,6):
                    try:
                        #check for two anomalies: 1. download time should be less than 60 sec || 2. dl_size > 0
                        flag1 = (db["rw{}".format(y)]["db{}".format(0)]["Total_Time"][z] < 60 and db["rw{}".format(y)]["db{}".format(0)]["Download_Size"][z] > 0 and db["rw{}".format(y)]["db{}".format(0)]["Total_Time"][z] > 1)
                        flag2 = (db["rw{}".format(y)]["db{}".format(1)]["Total_Time"][z] < 60 and db["rw{}".format(y)]["db{}".format(1)]["Download_Size"][z] > 0 and db["rw{}".format(y)]["db{}".format(1)]["Total_Time"][z] > 1)
                        flag3 = ((db["rw{}".format(y)]["db{}".format(0)]["Circuit_Count"][z] == 1) and (db["rw{}".format(y)]["db{}".format(1)]["Circuit_Count"][z] == 1))
                        if ((flag1 and flag2) and flag3):
                            avgsum += db["rw{}".format(y)]["db{}".format(x)][y_axis_var][z]
                            avgdiv += 1
                    except:
                        pass
                if avgdiv == 0: #it removes the outliers reaching to 60 sec in the image
                    avg_name[x].append(0)
                else:
                    avg = avgsum/avgdiv
                    avg_name[x].append(avg)
        except Exception as e:
            print(f"Error: {e}")
            pass


    #some value-checks for now, since here it does not make any sense
    if y_axis_var == "Total_Time":
        for i in range(2):
            avg_name[i] = [j for j in avg_name[i] if (j!=0)] # only valid for total time, remove this for TTFB
    # else:
    #     for i in range(2):
    #         avg_name[i] = [j for j in avg_name[i] if ((j!=0))]
    print(f"---------------------------------------------for {locx} :-------------------------------------------------------------- ")
    # print(avg_name)
    # input()
    # t =[avg_name]
    # for i in range(11):
    #     if len(avg_name[i]) == 0:
    #         avg_name[i] = zero_copy
    print(shape(avg_name))
    result.append(avg_name)

    medians = {}
    for i in range(2):
        medians["{}".format(pt_names[i])] = np.median(avg_name[i])

    medians_df = pd.DataFrame(medians, index = [0])

# pt_names = [  'Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure']

# print(shape(result))
# print(len(result[0][1]))

temp = pd.DataFrame(columns=['Tor', pt_name],  index=[i for i in range(1,1001)])
# temp.columns = [str(i) for i in range(500)]
# print(result)

# path = '/home/nsl300/Documents/scripts/graphs/all_pt_location-wise_datPoints_5/'
path = '/home/nsl300/Documents/curl_Tor_PTwithTor_same_circuit_tranco-1000/dataPoints/'
#create a folder for this PT
os.system(f"mkdir {path}{pt_name} -p")
# for i in range(0,2):
    
#     avg_t_for_pts = []
#     for j in range(len(result)):
#         copy_ = result[j][i]
        
#         if len(result[j][i]) == 0:
#             avg_t_for_pts.append( zero_copy )
#         else:
#             avg_t_for_pts.append(result[j][i])
        
#         ##copy data to temp and save
#         if len(copy_)>0:
#             print(shape(copy_))
#             for k in range(len(copy_)):
#                 temp.iloc[k][0] = copy_[k]
#             temp.to_csv(f"{path}{pt_name}/{loc_list[j]}.csv")
            
    
#     print(len(avg_t_for_pts))
#     print(shape(avg_t_for_pts))
print(len(result))
print(shape(result))


for i in range(0,2):
    
    avg_t_for_pts = []
    ind = loc_list.index(pt_name)
    print(f"\nindex: {ind}\n")
    copy_ = result[ ind ][i]
    
    # if len(result[j][i]) == 0:
    #     avg_t_for_pts.append( zero_copy )
    # else:
    #     avg_t_for_pts.append(result[j][i])
    
    ##copy data to temp and save
    if len(copy_)>0:
        print(shape(copy_))
        for k in range(len(copy_)):
            temp.iloc[k][i] = copy_[k]
        
            
temp.to_csv(f"{path}{pt_name}/{pt_name}.csv")    
    # print(len(avg_t_for_pts))
    # print(shape(avg_t_for_pts))

# list_ = [[avg_t_for_pts[0], avg_t_for_pts[1]]
# # print(avg_t_for_pts[0])
# plt.boxplot([ avg_t_for_pts[0], avg_t_for_pts[1] ])
# # plt.xticks([i for i in range(len(avg_t_for_pts))], loc_list[0:len(avg_t_for_pts)])
# plt.xticks( [1,2], ['Tor',pt_name])
# plt.xlabel("Tor and PT")
# plt.ylabel(y_axis_var)
# plt.title(result_type)
# plt.show()

