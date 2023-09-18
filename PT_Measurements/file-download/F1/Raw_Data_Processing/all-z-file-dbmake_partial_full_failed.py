import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy
import math


flag = 1
loc_list = [  'fra-blr', 'fra-lon','fra-tor','nyc-blr','nyc-lon','nyc-tor','sgp-blr','sgp-lon','sgp-tor', 'Tor-only-blr2', 'Tor-only-lon2', 'Tor-only-tor2' ]

for locx in loc_list:
    location = locx
    y_axis_var = "Total_Time"

    #calculate num of lines in a file and store in count
    try:
        with open(r"~/{0}/file-download/result_file1/new_pt9.txt".format(location), 'r') as fp:
            for count, line in enumerate(fp):
                pass
    except Exception as e:
        with open(r"~/{0}/file-download/result_file1/new_pt0.txt".format(location), 'r') as fp:
            for count, line in enumerate(fp):
                pass
    # open files
    fd = {}
    for i in range(1,3):
        fd["rw{0}".format(i)] = {}

    for x in range(1,3):
        for y in range(0, 12):
            try:
                fd["rw{0}".format(x)]["f{0}".format(y)] = open(r"~/{0}/file-download/result_file{1}/new_pt{2}.txt".format(location, x, y), 'r')
            except Exception as e:
                print(f"Error: {e}")

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
    for i in range(1,3):
        db["rw{}".format(i)] = {}

    '''
    creating list with original download size
    '''
    ogdl = [5242880, 10485760, 20971520, 52428800, 104857600]
    '''
    creating dictionary with structure:
    {
        "folder-file": [counts of not downloading file properly indexed in order]
    }
    '''
    ptfail = {}
    byptfail = {}
    pt_failures = {}

    # for i in range(11):
    #     pt_failures["pt{0}".format(i)] = [[0]*3]*5 
    # print(pt_failures)
    # # quit()
    # input()

    temp = []
    for i in range(12):
        temp = []
        for j in range(5):
            temp2 = []
            for k in range(3):
                temp2.append(0)
            temp.append(temp2)
        pt_failures["pt{0}".format(i)] = copy.deepcopy(temp)
    # print(pt_failures)
    # quit()
        # for each PT, a list that contains partial, full or not downloaded data for each of the 5 file sizes
        # [complete, partial, 0]

    # main loop
    for y in range(1,3):
        #for multiple result its
        for x in range(0,12):
            try:
                tmpx = fd["rw{0}".format(y)]["f{0}".format(x)].read()
            except Exception as e:
                continue
            tmp = tmpx.split()
            websites.clear()
            dl_size.clear()
            dl_speed.clear()
            tcp_c.clear()
            ttfb.clear()
            total_time.clear()
            for i in range((count+1)//2):
                # print(y,x,i)
                # print(f"Tmp is:  [ {tmp} ]")
                
                if x == 8 or (len(tmp)-1)/10 == 5:
                    
                    websites.append(str(tmp[10*i +1]))

                    if int(tmp[10*i + 3]) == 0:
                        pt_failures["pt{0}".format(x)][i][2] += 1
                    elif 0 < int(tmp[10*i + 3]) < ogdl[i]:
                        pt_failures["pt{0}".format(x)][i][1] += 1
                    else:
                        pt_failures["pt{0}".format(x)][i][0] += 1

                    if int(tmp[10*i + 3]) < ogdl[i]:
                        if "rw{0}-f{1}".format(y,x) not in ptfail:
                            ptfail["rw{0}-f{1}".format(y,x)] = [0]*5
                            if "f{}".format(x) not in byptfail:
                                byptfail["f{}".format(x)] = [0]*5
                        ptfail["rw{0}-f{1}".format(y,x)][i] += 1
                        byptfail["f{}".format(x)][i] += 1 

                    dl_size.append(int(tmp[10*i + 3]))
                    dl_speed.append(0) # changing this to 0 because not recorded
                    tcp_c.append(float(tmp[10*i + 5]))
                    #print(tmp[12*i + 9])
                    ttfb.append(float(tmp[10*i + 7]))
                    
                    total_time.append(float(tmp[10*i + 10]))
                else:
                    print(f"Current value of x:: {x}")
                    try:
                        websites.append(str(tmp[12*i +1]))
                    except:
                        print(f'loc{locx} rs{y} pt{x}')
                        exit(-1)

                    if int(tmp[12*i + 3]) == 0:
                        pt_failures["pt{0}".format(x)][i][2] += 1
                    elif 0 < int(tmp[12*i + 3]) < ogdl[i]:
                        pt_failures["pt{0}".format(x)][i][1] += 1
                    else:
                        pt_failures["pt{0}".format(x)][i][0] += 1

                    if int(tmp[12*i + 3]) < ogdl[i]:
                        if "rw{0}-f{1}".format(y,x) not in ptfail:
                            ptfail["rw{0}-f{1}".format(y,x)] = [0]*5
                            if "f{}".format(x) not in byptfail:
                                byptfail["f{}".format(x)] = [0]*5
                        ptfail["rw{0}-f{1}".format(y,x)][i] += 1
                        byptfail["f{}".format(x)][i] += 1 

                    dl_size.append(int(tmp[12*i + 3]))
                    dl_speed.append(float(tmp[12*i + 5]))
                    tcp_c.append(float(tmp[12*i + 7]))
                    #print(tmp[12*i + 9])
                    ttfb.append(float(tmp[12*i + 9]))
                    
                    total_time.append(float(tmp[12*i + 12]))
                      # print(pt_failures)
                    # print(y,x,i)
                    # input()
            db["rw{}".format(y)]["db{0}".format(x)] = {"Website":copy.deepcopy(websites),"Download_Size":copy.deepcopy(dl_size),"Download_Speed":copy.deepcopy(dl_speed),"TCP_connect":copy.deepcopy(tcp_c),"TTFB":copy.deepcopy(ttfb),"Total_Time":copy.deepcopy(total_time)}

    # calculating averages from db and storing in new avg_db
    #print(db)
    #jnsdkfjn

    #avg_t_for_pts = [[0]*len((db["rw1"]["db1"]["Total_Time"]))]*9
    avg_t_for_pts = []
    for i in range(12):
        avg_t_for_pts.append([])
    #print(len(avg_t_for_pts), len(avg_t_for_pts[0]))
    for x in range(0,12):
        try:
            len_ = len(db["rw1"]["db{}".format(x)][y_axis_var])
        except Exception as e:
            continue
        for z in range(len_):
            avgsum = 0
            avgdiv = 0
            for y in range(1,3):

                try:
                    if db["rw{}".format(y)]["db{}".format(x)]["Download_Size"][z] > 0:  #it removes the problem of unnecessary addition of avgdiv irrespective of its successful download
                        avgsum += db["rw{}".format(y)]["db{}".format(x)][y_axis_var][z]
                        avgdiv += 1
                except Exception as e:
                    print(f"Can not access file: {e}")
            #    print( db["rw{}".format(y)]["db{}".format(x)]["Total_Time"][z])
    #        print(x,z, avgsum, avgdiv)
            
            if avgdiv == 0: #it removes the outliers reaching to 60 sec in the image
                avg_t_for_pts[x-1].append(0)
            else:
                avg = avgsum/avgdiv
                avg_t_for_pts[x-1].append(avg)
            
            #avg_t_for_pts[x-1][z] = avgsum/avgdiv
     #       print(avg_t_for_pts[x-1][z])

    # print(len(avg_t_for_pts),"=======================================")

    for i in range(12):
        # print(avg_t_for_pts[i])
        # print("\n\n", len(avg_t_for_pts[i]), "\n\n\n\n")
        # # avg_t_for_pts[i] = list(filter((0).__ne__, avg_t_for_pts[i]))
        avg_t_for_pts[i] = [j for j in avg_t_for_pts[i] if (j != 0)]


    #----------------------------------------------------------------------
    '''
    creating dictionary with structure:
    {
        "folder-file": [counts of not downloading file properly indexed in order]
    }
    '''
    # ptfail = {}
    ptfail_df = pd.DataFrame(ptfail)
    byptfail_df = pd.DataFrame(byptfail)
    print(ptfail_df)
    print(byptfail_df)


    plot_array = [avg_t_for_pts[0], avg_t_for_pts[1], avg_t_for_pts[2], avg_t_for_pts[3], avg_t_for_pts[4], avg_t_for_pts[5], avg_t_for_pts[6], avg_t_for_pts[7], avg_t_for_pts[8], avg_t_for_pts[9], avg_t_for_pts[10]]
    # plt.boxplot(plot_array)
    pt_names = [  'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek', 'Camoufler', 'Dnstt', 'Tor-only', 'Psiphon']

    medians = {}
    for i in range(len(plot_array)):
        medians["{}".format(pt_names[i])] = np.median(plot_array[i])

    medians_df = pd.DataFrame(medians, index = [0])
    print(medians_df)

    ##calculating average time for each [5mb, 10mb, 20mb, 50mb, 100mb] files for each pt
    print(f"Average time for each\n [5mb, 10mb, 20mb, 50mb, 100mb]\n")
    for i in range(12):
        try:
            print(avg_t_for_pts[i][0], avg_t_for_pts[i][4])
        except Exception as e:
            pass

    print("\n\n\n\n\n\n\n")
    print("for each PT, a list that contains partial, full or not downloaded data for each of the 5 file sizes \n\n[complete, partial, 0]\n\n")

    # print(pd.DataFrame(pt_failures))
    a = pd.DataFrame(pt_failures)

    if flag==1:
        a_cp = pd.DataFrame(pt_failures)
        flag = 0
    else:
        for i in range(12): #columns
            for j in range(5): #rows
                a_cp.iloc[j,i][0] += a.iloc[j,i][0]
                a_cp.iloc[j,i][1] += a.iloc[j,i][1]
                a_cp.iloc[j,i][2] += a.iloc[j,i][2]

    #############################
    # Merge all
    #############################

    # print(a.columns)
    
                
    print(a_cp)
    # ch = input("Continue? 1/0: ")
    # if ch == '0':
    #     break

a_cp.to_csv('Final_download_count-.csv')

########################stacked bar plot
# temp = pd.DataFrame(columns=[])


files = ['5MB', '10MB', '20MB', '50MB', '100MB']
for i in range(5):
    x = ['Tor', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek', 'Camoufler', 'Dnstt', 'Psiphon']
    x_ =[7, 1, 6, 9, 3, 2, 11, 4, 5, 8, 0] #added 11 to skip massbrowser
    #print()
    y1 = np.array([ (a_cp.iloc[i,j][0] ) /(a_cp.iloc[i,j][0] + a_cp.iloc[i,j][1] + a_cp.iloc[i,j][2]) for j in x_])
    y2 = np.array([ (a_cp.iloc[i,j][1] ) /(a_cp.iloc[i,j][0] + a_cp.iloc[i,j][1] + a_cp.iloc[i,j][2]) for j in x_])
    y3 = np.array([ (a_cp.iloc[i,j][2] ) /(a_cp.iloc[i,j][0] + a_cp.iloc[i,j][1] + a_cp.iloc[i,j][2]) for j in x_])
    print('----------------------------------------------------------')
    print(':: ', y1)
    print(':: ', y2)
    print(':: ', y3)
    print('----------------------------------------------------------')

    import seaborn as sns
    sns.set_style("white")

    # print(f"X: {x}\nY1:{y1}\nY2: {y2}\nY3: {y3}")
    low = 0
    high = 1
    plt.ylim([(low-0.01*(high-low)), (high+0.1)])

    x_ =[7, 1, 6, 9, 3, 2, 10, 4, 5, 8, 0]
    x = [x[k] for k in x_]
    print(x)
    plt.bar(x, y1, width=0.5, align='center', color='b', fill=True, hatch='xx')
    plt.bar(x, y2, width=0.5, align='center', bottom=y1, color='r', fill=True, hatch='..')
    plt.bar(x, y3, width=0.5, align='center', bottom=y1+y2, color='black', fill=True, hatch='++')
    # plt.xlabel("Pluggable Transports & Tor", fontsize=18)
    plt.xticks(fontsize=22, rotation= 45, weight = 'bold', fontname = "Times New Roman")
    plt.ylabel("Fraction of Downloads", fontsize=22, weight = 'bold')
    plt.yticks( fontsize=18, weight = 'bold')
    plt.legend(["Complete", "Partial", "Zero"], prop = {'size':20}, loc='upper right', ncol = 3)#bbox_to_anchor=(1, 1), loc=1, borderaxespad=0)
    plt.title(f"Downloads For {files[i]}-file", fontsize=22, weight = 'bold')
    plt.show()

