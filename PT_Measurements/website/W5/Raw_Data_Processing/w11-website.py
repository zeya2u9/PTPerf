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
loc_list = [  'browsertime' ]
pt_names = [  'Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']


result_type = 'tranco'
y_axis_var = input("enter eval criteria: SpeedIndex (milli-seconds) Median Mean: ")


avg_name_list = []
result = []

for locx in loc_list:
    location = locx
    avg_name = 'avg_t_for_pts_'+location
    avg_name_list.append(avg_name)
    #calculate num of lines in a file and store in count
    try:
        with open(r"~/browsertime/tranco/result_web_combine/n-trf-tr3.txt", 'r') as fp:
            for count, line in enumerate(fp):
                pass
    except Exception as e:
        print(f"Error:: {e}")

    # exit(0)
    # open files
    fd = {}
    for i in range(1):
        fd["rw{0}".format(i)] = {}

    for x in range(1):
        for y in range(0, 14):
            try:
                fd["rw{0}".format(x)]["f{0}".format(y)] = open(r"~/browsertime/tranco/result_web_combine/n-trf-tr{0}.txt".format(y), 'r')
            except Exception as e:
                print(f"Can not access file: {e}")
                pass

    websites = []
    median = []
    mean = []

    # create db
    # db can easily be converted to a DataFrame, if needed
    # contains multiple iterations (rw{})
    db = {}
    for i in range(1):
        db["rw{}".format(i)] = {}

    # main loop
    for y in range(1):
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
            median.clear()
            mean.clear()

            # print(f"-----------------------------------------------------------x: {x} y:{y}")
            for i in range((count+1)//2):
                try:
                    websites.append(str(tmp[7*i]))
                    median.append(float(tmp[7*i + 4]))
                    mean.append(float(tmp[7*i + 6]))
                    # print(f"{str(tmp[7*i])} - median:{str(tmp[7*i + 4])} - mean:{str(tmp[7*i + 6])}")
                except Exception as e:
                    pass
            db["rw{}".format(y)]["db{}".format(x)] = {"Website":copy.deepcopy(websites),"Median":copy.deepcopy(median),"Mean":copy.deepcopy(mean)}

    avg_name = []
    for i in range(14):
        avg_name.append([])

    print(len(db))

    for x in range(0,14):
        print(x,"---------------------------------------")
        # print(len(db["rw0"]["db{0}".format(x)][y_axis_var]))
        try:   
            print(len(db["rw0"]["db{0}".format(x)][y_axis_var])) 
            for z in range(len(db["rw0"]["db{}".format(x)][y_axis_var])):
                avgsum = 0
                avgdiv = 0
                for y in range(1):
                    try:
                        if db["rw{}".format(y)]["db{}".format(x)]["Median"][z] > 0:
                            avgsum += db["rw{}".format(y)]["db{}".format(x)][y_axis_var][z]
                            avgdiv += 1
                    except:
                        pass
                if avgdiv == 0: #it removes the outliers reaching to 60 sec in the image
                    avg_name[x].append(0)
                else:
                    avg = ( avgsum/avgdiv ) * 0.001
                    avg_name[x].append(avg)
        except Exception as e:
            print(f"Error: {e}")
            pass

    if result_type == "Total_Time":
        for i in range(14):
            avg_name[i] = [j for j in avg_name[i] if ((j > 1) and (j!=0))] # only valid for total time, remove this for TTFB
    else:
        for i in range(14):
            avg_name[i] = [j for j in avg_name[i] if ((j!=0))]
            print(len(avg_name[i]))
            # exit(0)
    # print(avg_name)
    # t =[avg_name]
    # for i in range(11):
    #     if len(avg_name[i]) == 0:
    #         avg_name[i] = zero_copy
    print(shape(avg_name))
    print(avg_name)
    result.append(avg_name)

    medians = {}
    for i in range(14):
        medians["{}".format(pt_names[i])] = np.median(avg_name[i])

    medians_df = pd.DataFrame(medians, index = [0])
    # print(medians_df)
    # ch = input("Continue? 1/0: ")
    # if ch == '0':
    #     break

pt_names = [  'Tor-only', 'Obfs4', 'Marionette', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']

print(shape(result))
print(len(result[0][1]))

temp = pd.DataFrame(columns=['Time'],  index=[i for i in range(1,1001)])
# temp.columns = [str(i) for i in range(500)]

path = '~/CSVs/'
# avg_t_for_pts = []
all_pts = []
for i in range(0,14):
    
    #create a folder for this PT
    # os.system(f"mkdir {path}{pt_names[i]}")

    avg_t_for_pts = []
    for j in range(len(result)):
        copy_ = result[j][i]
        
        if len(result[j][i]) == 0:
            avg_t_for_pts.append( zero_copy )
        else:
            avg_t_for_pts.append(result[j][i])
        all_pts.append(avg_t_for_pts)

        ##copy data to temp and save
        temp = pd.DataFrame(columns=['Time'],  index=[i for i in range(1,1001)])
        if len(copy_)>0:
            print(shape(copy_))
            for k in range(len(copy_)):
                temp.iloc[k][0] = copy_[k]
            temp.to_csv(f"{path}/{pt_names[i]}.csv")
    
    print(len(avg_t_for_pts))
    print(shape(avg_t_for_pts))

    # list_ = [[avg_t_for_pts[0], avg_t_for_pts[1], avg_t_for_pts[2], avg_t_for_pts[3], avg_t_for_pts[4], avg_t_for_pts[5], avg_t_for_pts[6], avg_t_for_pts[7], avg_t_for_pts[8], avg_t_for_pts[9], avg_t_for_pts[10], avg_t_for_pts[11]]
    # plt.boxplot([avg_t_for_pts[0], avg_t_for_pts[1], avg_t_for_pts[2], avg_t_for_pts[3], avg_t_for_pts[4], avg_t_for_pts[5], avg_t_for_pts[6], avg_t_for_pts[7], avg_t_for_pts[8], avg_t_for_pts[9], avg_t_for_pts[10], avg_t_for_pts[11]])
    # plt.xticks([i for i in range(len(avg_t_for_pts))], loc_list[0:len(avg_t_for_pts)])

print(all_pts[0][0])
plt.boxplot([all_pts[0][0], all_pts[1][0], all_pts[2][0], all_pts[3][0], all_pts[4][0], all_pts[5][0], all_pts[6][0], all_pts[7][0], all_pts[8][0], all_pts[9][0], all_pts[10][0], all_pts[11][0], all_pts[12][0], all_pts[13][0]])

# plt.boxplot([avg_t_for_pts[0], avg_t_for_pts[1], avg_t_for_pts[2], avg_t_for_pts[3], avg_t_for_pts[4], avg_t_for_pts[5], avg_t_for_pts[6], avg_t_for_pts[7], avg_t_for_pts[8], avg_t_for_pts[9], avg_t_for_pts[10], avg_t_for_pts[11], avg_t_for_pts[12], avg_t_for_pts[13]])
#plt.boxplot( [avg_t_for_pts[0]] )
pt_names = [  'Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek','Camoufler', 'Dnstt', 'Massbrowser', 'Psiphon', 'Conjure', 'WebTunnel']
# pt_names_new = ['meek', 'psiphon', 'conjure']
plt.xticks( [1,2,3,4,5,6,7,8,9,10,11,12,13,14], pt_names)
plt.xlabel(f"PT-{pt_names[i]}")
plt.ylabel(y_axis_var)
plt.title(result_type)
plt.show()
