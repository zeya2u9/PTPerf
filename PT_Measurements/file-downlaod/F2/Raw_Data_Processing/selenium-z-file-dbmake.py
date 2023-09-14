import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy

#create the graph
fig = plt.figure()
#ax = fig.add_axes([0,0,1,1])

location = input("location in server-client format: ")
y_axis_var = input("enter eval criteria: Total_Time - Download_Size: ")


#calculate num of lines in a file and store in count
with open(r"/homeselenium_overall_result1000/file_download/all-pts/file-download/result_file1/new_pt0.txt".format(location), 'r') as fp:
    for count, line in enumerate(fp):
        pass

# open files
fd = {}
for i in range(1,6):
    fd["rw{0}".format(i)] = {}

for x in range(1,6):
    for y in range(0, 14):
        try:
            fd["rw{0}".format(x)]["f{0}".format(y)] = open(r"selenium_overall_result1000/file_download/all-pts/file-download/result_web{1}/new_pt{2}.txt".format(location, x, y), 'r')

        except Exception as e:
            print(f"Error: {e}")

websites = []
dl_size = []
total_time = []
dl_speed = []

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
        total_time.clear()
        dl_speed.clear()
        for i in range((count+1)//2):
            # print(y,x,i)
            # print(f"Tmp is:  [ {tmp} ]")
            
            if x == 8 or x == 10 or (len(tmp)-1)/10 == 5:
                continue
            else:
                # print(f"Current value of x:: {x}")
                websites.append(str(tmp[8*i +1]))

                if int(tmp[8*i + 4]) == 0:
                    pt_failures["pt{0}".format(x)][i][2] += 1
                elif 0 < int(tmp[8*i + 4]) < ogdl[i]:
                    pt_failures["pt{0}".format(x)][i][1] += 1
                else:
                    pt_failures["pt{0}".format(x)][i][0] += 1

                if int(tmp[8*i + 4]) < ogdl[i]:
                    if "rw{0}-f{1}".format(y,x) not in ptfail:
                        ptfail["rw{0}-f{1}".format(y,x)] = [0]*5
                        if "f{}".format(x) not in byptfail:
                            byptfail["f{}".format(x)] = [0]*5
                    ptfail["rw{0}-f{1}".format(y,x)][i] += 1
                    byptfail["f{}".format(x)][i] += 1 

                dl_size.append(int(tmp[8*i + 4]))               
                total_time.append(float(tmp[8*i + 7]))
                # dl_speed.append(float(dl_size[-1]/total_time[-1])) 
                #commented dl_speed for now
                dl_speed.append(0) 
                  # print(pt_failures)
                # print(y,x,i)
                # input()
        db["rw{}".format(y)]["db{0}".format(x)] = {"Website":copy.deepcopy(websites),"Download_Size":copy.deepcopy(dl_size),"Download_Speed":copy.deepcopy(dl_speed), "Total_Time":copy.deepcopy(total_time)}

# calculating averages from db and storing in new avg_db
#print(db)
#jnsdkfjn

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
        
        if avgdiv == 0: #it removes the outliers reaching to 60 sec in the image
            avg_t_for_pts[x].append(0)
        else:
            avg = avgsum/avgdiv
            avg_t_for_pts[x].append(avg)
        

for i in range(14):
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

#----------------------------------------------------------------------

print(len(avg_t_for_pts))
plot_array = [avg_t_for_pts[0], avg_t_for_pts[1], avg_t_for_pts[2], avg_t_for_pts[3], avg_t_for_pts[4], avg_t_for_pts[5], 
              avg_t_for_pts[6], avg_t_for_pts[7], avg_t_for_pts[8], avg_t_for_pts[9], avg_t_for_pts[10], avg_t_for_pts[11], avg_t_for_pts[12], avg_t_for_pts[13]]
plt.boxplot(plot_array, whis=(0, 100))
pt_names = [ 'Tor', 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek', 'Camoufler', 'Dnstt', 'MassBrowser', 'Psiphon', 'Conjure', 'WebTunnel']
plt.xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,13,14], pt_names)
plt.xlabel(f"Tor & diff. Pluggable Transports Loc:{location}")
plt.ylabel(y_axis_var)
plt.title("File-Download")
# plotting
# plt.boxplot([db["db1"]['Total_Time'], db["db2"]['Total_Time'], db["db3"]['Total_Time'], db["db4"]['Total_Time'], db["db5"]['Total_Time'], db["db9"]['Total_Time']])

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

pd.options.display.max_columns = None
pd.options.display.max_rows = None
print(pd.DataFrame(pt_failures))

print(avg_t_for_pts[0:5])

a = pd.DataFrame(pt_failures)
print(a.columns)
for i in range(1,2):
    for j in range(5):
        print(f":: {a.iloc[j,i][0]}")

