import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy
import os

#create the graph
fig = plt.figure()
#ax = fig.add_axes([0,0,1,1])

#location = 'file-download'
input("location in server-client format: ")
y_axis_var = 'Total_Time'
# input("enter eval criteria: Total_Time - Download_Speed - TTFB - TCP_connect: ")


#calculate num of lines in a file and store in count
with open(r"~/{0}/file-download/result_file1/new_pt1.txt".format(location), 'r') as fp:
    for count, line in enumerate(fp):
        pass

# open files
fd = {}
for i in range(1,6):
    fd["rw{0}".format(i)] = {}

for x in range(1,6):
    for y in range(0, 14):
        try:
            fd["rw{0}".format(x)]["f{0}".format(y)] = open(r"~/{0}/file-download/result_file{0}/new_pt{1}.txt".format(location, x, y), 'r')
            print(f"Round:{x} PT:{y}")
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
for i in range(1,6):
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
csvs_dict = {}

# for i in range(11):
#     pt_failures["pt{0}".format(i)] = [[0]*3]*5 
# print(pt_failures)
# # quit()
# input()

temp = []
for i in range(14):
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

for i in range(14):
    temp = {}
    for j in range(5):      # iterations
        temp2 = []
        for k in range(5):  # file
            temp2.append(0)
        temp[f'iteration-{j}'] = temp2
    csvs_dict[f'pt-{i}'] = copy.deepcopy(temp)



# main loop
for y in range(1,6):
    #for multiple result its
    for x in range(0,14):
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
            
            if x == 10 or x == 8 :
                continue
            if x in [4,5,9]:
                print(f"Current value of x:: {x} -- NOSPEED----------")
                websites.append(str(tmp[10*i +1]))

                if int(tmp[10*i + 3]) == 0:
                    pt_failures["pt{0}".format(x)][i][2] += 1
                elif 0 < int(tmp[10*i + 3]) < ogdl[i]:
                    pt_failures["pt{0}".format(x)][i][1] += 1
                else:
                    pt_failures["pt{0}".format(x)][i][0] += 1

                ###############
                perc = 100 - (((ogdl[i] - int(tmp[10*i + 3])) / ogdl[i]) * 100)
                # y -> its
                # x -> pt
                # i -> file
                print('x y i -> ', x,y,i)
                csvs_dict[f'pt-{x}'][f'iteration-{y-1}'][i] = perc
                ###############

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
                websites.append(str(tmp[12*i +1]))

                if int(tmp[12*i + 3]) == 0:
                    pt_failures["pt{0}".format(x)][i][2] += 1
                elif 0 < int(tmp[12*i + 3]) < ogdl[i]:
                    pt_failures["pt{0}".format(x)][i][1] += 1
                else:
                    pt_failures["pt{0}".format(x)][i][0] += 1

                ###############
                perc = 100 - (((ogdl[i] - int(tmp[12*i + 3])) / ogdl[i]) * 100)
                # y -> its
                # x -> pt
                # i -> file
                print('x y i -> ', x,y,i)
                csvs_dict[f'pt-{x}'][f'iteration-{y-1}'][i] = perc
                ###############

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
# print(db)
#jnsdkfjn
# exit(0)
#avg_t_for_pts = [[0]*len((db["rw1"]["db1"]["Total_Time"]))]*9
avg_t_for_pts = []
for i in range(14):
    avg_t_for_pts.append([])
#print(len(avg_t_for_pts), len(avg_t_for_pts[0]))
for x in range(0,14):
    try:
        len_ = len(db["rw1"]["db{}".format(x)][y_axis_var])
    except Exception as e:
        continue
    for z in range(len_):
        avgsum = 0
        avgdiv = 0
        for y in range(1,6):

            try:
                if db["rw{}".format(y)]["db{}".format(x)]["Download_Size"][z] > 0:  #it removes the problem of unnecessary addition of avgdiv irrespective of its successful download
                    avgsum += db["rw{}".format(y)]["db{}".format(x)][y_axis_var][z]
                    avgdiv += 1
            except Exception as e:
                print(f"Can not access file: {e}")
        #    print( db["rw{}".format(y)]["db{}".format(x)]["Total_Time"][z])
#        print(x,z, avgsum, avgdiv)
        
        if avgdiv == 0: #it removes the outliers reaching to 60 sec in the image
            avg_t_for_pts[x].append(0)
        else:
            avg = avgsum/avgdiv
            avg_t_for_pts[x].append(avg)
        
        #avg_t_for_pts[x-1][z] = avgsum/avgdiv
 #       print(avg_t_for_pts[x-1][z])

print(len(avg_t_for_pts),"=======================================")
print(avg_t_for_pts[4])
for i in range(14):
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

#----------------------------------------------------------------------

# print(avg_t_for_pts[0])
# print(avg_t_for_pts[1])
# print(avg_t_for_pts[8])
 

#pts = c()
plot_array = [avg_t_for_pts[0], avg_t_for_pts[1], avg_t_for_pts[2], avg_t_for_pts[3], avg_t_for_pts[4], avg_t_for_pts[5], avg_t_for_pts[6], avg_t_for_pts[7], avg_t_for_pts[8], avg_t_for_pts[9], avg_t_for_pts[10], avg_t_for_pts[11], avg_t_for_pts[12], avg_t_for_pts[13]]
plt.boxplot(plot_array)
pt_names = [ 'Tor-only', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek', 'Camoufler', 'Dnstt', 'MassBrowser', 'Psiphon', 'Conjure', 'WebTunnel']
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ,13, 14], pt_names)
plt.xlabel(f"Tor & diff. Pluggable Transports Loc:{location}")
plt.ylabel(y_axis_var)
plt.title("File-Download")
# plotting
#plt.boxplot([db["db1"]['Total_Time'], db["db2"]['Total_Time'], db["db3"]['Total_Time'], db["db4"]['Total_Time'], db["db5"]['Total_Time'], db["db9"]['Total_Time']])

plt.show()

medians = {}
for i in range(len(plot_array)):
    medians["{}".format(pt_names[i])] = np.median(plot_array[i])

medians_df = pd.DataFrame(medians, index = [0])
print(medians_df)

##calculating average time for each [5mb, 10mb, 20mb, 50mb, 100mb] files for each pt
print(f"Average time for each\n [5mb, 10mb, 20mb, 50mb, 100mb]\n")
for i in range(14):
    try:
        print(avg_t_for_pts[i][0], avg_t_for_pts[i][4])
    except Exception as e:
        pass

print("\n\n\n\n\n\n\n")
print("for each PT, a list that contains partial, full or not downloaded data for each of the 5 file sizes \n\n[complete, partial, 0]\n\n")

print(pd.DataFrame(pt_failures))
a = pd.DataFrame(pt_failures)
print(a.columns)
for i in range(1,6):
    for j in range(5):
        print(f":: {a.iloc[j,i][0]}")

os.system('rm -rdf ~/F1/file_perc_csvs')
os.system('mkdir file_perc_csvs')
for i in range(14):
    df = pd.DataFrame(csvs_dict[f'pt-{i}'])
    print('\n\n', 'pt ',i,'\n')
    print(df)
    print('\n\n')
    df.to_csv(f'~/F1/file_perc_csvs/{pt_names[i]}.csv')
