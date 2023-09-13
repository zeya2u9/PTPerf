import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy
import os


def shape(lst):
    length = len(lst)
    shp = tuple(shape(sub) if isinstance(sub, list) else 0 for sub in lst)
    if any(x != 0 for x in shp):
        return length, shp
    else:
        return length

zero_copy = [0]*1000

flag = 1
loc_list = [  'fra-blr', 'fra-lon','fra-tor','nyc-blr','nyc-lon','nyc-tor','sgp-blr','sgp-lon','sgp-tor' ]
pt_names = [  'Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']


result_type = input("choose option: tranco - blocked: ")
y_axis_var = input("enter eval criteria: Total_Time - Download_Speed - TTFB - TCP_connect: ")


avg_name_list = []
result = []

for locx in loc_list:
    location = locx
    avg_name = 'avg_t_for_pts_'+location
    avg_name_list.append(avg_name)
    #calculate num of lines in a file and store in count
    try:
        with open(r"overall_result3/{0}/{1}/result_web1/n-trf-tr2.txt".format(location, result_type), 'r') as fp:
            for count, line in enumerate(fp):
                pass
    except Exception as e:
        with open(r"overall_result3/{0}/{1}/result_web1/n-trf-tr0.txt".format(location, result_type), 'r') as fp:
            for count, line in enumerate(fp):
                pass

    # open files
    fd = {}
    for i in range(1,6):
        fd["rw{0}".format(i)] = {}

    for x in range(1,6):
        for y in range(0, 14):
            try:
                fd["rw{0}".format(x)]["f{0}".format(y)] = open(r"overall_result3/{2}/{3}/result_web{0}/n-trf-tr{1}.txt".format(x, y, location, result_type), 'r')
            except Exception as e:
                # print(f"Can not access file: {e}")
                pass

    websites = []
    dl_size = []
    dl_speed = []
    tcp_c = []
    ttfb = []
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
            tcp_c.clear()
            ttfb.clear()
            total_time.clear()
            # print(f"-----------------------------------------------------------x: {x} y:{y}")
            for i in range((count+1)//2):
                websites.append(str(tmp[12*i +1]))
                dl_size.append(int(tmp[12*i + 3]))
                dl_speed.append(float(tmp[12*i + 5]))
                tcp_c.append(float(tmp[12*i + 7]))
                ttfb.append(float(tmp[12*i + 9]))
                
                total_time.append(float(tmp[12*i + 12]))
            db["rw{}".format(y)]["db{0}".format(x)] = {"Website":copy.deepcopy(websites),"Download_Size":copy.deepcopy(dl_size),"Download_Speed":copy.deepcopy(dl_speed),"TCP_connect":copy.deepcopy(tcp_c),"TTFB":copy.deepcopy(ttfb),"Total_Time":copy.deepcopy(total_time)}

    avg_name = []
    for i in range(14):
        avg_name.append([])

    for x in range(0,14):
        try:    
            for z in range(len(db["rw1"]["db{}".format(x)][y_axis_var])):
                avgsum = 0
                avgdiv = 0
                for y in range(1,6):
                    try:
                        if 1 < db["rw{}".format(y)]["db{}".format(x)]["Total_Time"][z] < 57:
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
            # print(f"Error: {e}")
            pass

    if result_type == "Total_Time":
        for i in range(14):
            avg_name[i] = [j for j in avg_name[i] if ((j > 1) and (j!=0))] # only valid for total time, remove this for TTFB
    else:
        for i in range(14):
            avg_name[i] = [j for j in avg_name[i] if ((j!=0))]
    # print(avg_name)
    # t =[avg_name]
    # for i in range(11):
    #     if len(avg_name[i]) == 0:
    #         avg_name[i] = zero_copy
    print(shape(avg_name))
    result.append(avg_name)

    medians = {}
    for i in range(14):
        medians["{}".format(pt_names[i])] = np.median(avg_name[i])

    medians_df = pd.DataFrame(medians, index = [0])
    # print(medians_df)
    # ch = input("Continue? 1/0: ")
    # if ch == '0':
    #     break

pt_names = [  'Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']

print(shape(result))
print(len(result[0][1]))

temp = pd.DataFrame(columns=['Time'],  index=[i for i in range(1,1001)])
# temp.columns = [str(i) for i in range(500)]

path = '/home/nsl300/Documents/1_Final_results/W-Website/W1/'
for i in range(0,14):
    
    #create a folder for this PT
    os.system(f"mkdir {path}{pt_names[i]}")

    avg_t_for_pts = []
    temp = pd.DataFrame(columns=['Time'],  index=[i for i in range(1,1001)])
    for j in range(len(result)):
        copy_ = result[j][i]
        
        if len(result[j][i]) == 0:
            avg_t_for_pts.append( zero_copy )
        else:
            avg_t_for_pts.append(result[j][i])
        
        ##copy data to temp and save
        if len(copy_)>0:
            print(shape(copy_))
            for k in range(len(copy_)):
                temp.iloc[k][0] = copy_[k]
            temp.to_csv(f"{path}{pt_names[i]}/{loc_list[j]}.csv")
    
    print(len(avg_t_for_pts))
    print(shape(avg_t_for_pts))
    

    plt.boxplot([avg_t_for_pts[0], avg_t_for_pts[1], avg_t_for_pts[2], avg_t_for_pts[3], avg_t_for_pts[4], avg_t_for_pts[5], avg_t_for_pts[6], avg_t_for_pts[7], avg_t_for_pts[8], avg_t_for_pts[9], avg_t_for_pts[10], avg_t_for_pts[11]])
    plt.xticks( [1,2,3,4,5,6,7,8,9,10,11,12], loc_list)
    plt.xlabel(f"PT-{pt_names[i]}")
    plt.ylabel(y_axis_var)
    plt.title(result_type)
    plt.show()
