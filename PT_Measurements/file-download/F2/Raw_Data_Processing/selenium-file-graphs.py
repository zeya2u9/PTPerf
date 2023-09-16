import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import copy

#create the graph
fig = plt.figure()
#ax = fig.add_axes([0,0,1,1])

# TODO
# - convert box graph to line graph

locations = ["fra-blr" , "fra-tor" , "nyc-lon" , "sgp-blr" , "sgp-tor" , "fra-lon" , "nyc-blr" , "nyc-tor" , "sgp-lon"]


graph_array = []
# structure is [[avg of one file size indexed for each pt][...][...][...][...]]
# avg_divisor = []

pt_names = [ 'Tor-only' , 'Obfs4', 'Marionete', 'Shadowsocks', 'Stegotorus', 'Cloak', 'Snowflake', 'Meek', 'Camoufler', 'Dnstt', 'MassBrowser', 'Psiphon', 'Conjure', 'WebTunnel']

for i in range(len(pt_names)):
    print(i, f" :  {pt_names[i]}")
print("\n")
pt_num = int(input('graph for which PT? [0 to 13] : '))


if pt_num == 8:

    tor_only_locs = ["Tor-only-lon" , "Tor-only-blr" , "Tor-only-tor"]
    #TOR ONLT DIR STRUCT
    
    for i in range(len(tor_only_locs)):
        graph_array.append([])
        for j in range(5):
            graph_array[i].append(0)


    fd = {}
    for i in range(len(tor_only_locs)):
        fd[tor_only_locs[i]] = {}
        for j in range(1,3):
            try:
                # print(tor_only_locs[i], "rw{}".format(j), "read")
                fd[tor_only_locs[i]]["rw{}".format(j)]  = open(r"selenium_overall_result1000/file_download/all-pts/file-download/result_web{0}/n-trf-tr0.txt".format(j, tor_only_locs[i]), 'r')
            except:
                print("not done ---")
                pass

    ogdl = [5242880, 10485760, 20971520, 52428800, 104857600]
    # print(fd)
    file_dictionary = {}
    for i in range(len(tor_only_locs)):
        file_dictionary[tor_only_locs[i]] = {}


    for location in range(len(tor_only_locs)):
         for fsize in range(5):
            avgsum = 0
            avgdiv = 0
            for iteration in range(1,3):
                # print("iteration: ", iteration, "-----", "SIZE: ", fsize)
                try:
                    if "rw{}".format(iteration) not in file_dictionary[tor_only_locs[location]]:
                        file_dictionary[tor_only_locs[location]]["rw{}".format(iteration)] = fd[tor_only_locs[location]]["rw{}".format(iteration)].read().split()

                    tmp = file_dictionary[tor_only_locs[location]]["rw{}".format(iteration)]
                    # print("\n" ,"iteration: ", iteration, "-----", "SIZE: ", fsize, "\n" , tmp, "\n")
                    # print(float(tmp[12*fsize + 12]))
                    # print("WENT THROUGH!")
                    if int(float(tmp[12*fsize + 3])) == ogdl[fsize]:
                        avgsum += float(tmp[12*fsize + 12])
                        avgdiv += 1
                        # print("UPDATED AVGSUM: ", avgsum)
                except Exception as e:
                    print("not done --------")
                    print("error: ", e)

            # print("avgdiv: ", avgdiv, "iteration: ", iteration, "SIZE: ", fsize)
            # print("avgsum: ", avgsum, "iteration: ", iteration, "SIZE: ", fsize)
            graph_array[location][fsize] = avgsum/avgdiv

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
else:

    locations = ["all-pts" ]
    
    
    for i in range(len(locations)):
        graph_array.append([])
        for j in range(5):
            graph_array[i].append(0)


    fd = {}
    for i in range(len(locations)):
        fd[locations[i]] = {}
        for j in range(1,6):
            try:
                print(r"selenium_overall_result1000/file_download/all-pts/file-download/result_web{0}/n-trf-tr{1}.txt".format( j, pt_num))
                fd[locations[i]]["rw{0}".format(j)] = open(r"selenium_overall_result1000/file_download/all-pts/file-download/result_web{0}/n-trf-tr{1}.txt".format( j, pt_num), 'r')
            except:
                pass

    print(fd)

    ogdl = [5242880, 10485760, 20971520, 52428800, 104857600]
    file_dictionary = {}
    for i in range(len(locations)):
        file_dictionary[locations[i]] = {}

    for location in range(len(locations)):
         for fsize in range(5):
            avgsum = 0
            avgdiv = 0
            for iteration in range(1,6):
                try:
                    if "rw{}".format(iteration) not in file_dictionary[locations[location]]:
                        file_dictionary[locations[location]]["rw{}".format(iteration)] = fd[locations[location]]["rw{}".format(iteration)].read().split()
                    tmp = file_dictionary[locations[location]]["rw{}".format(iteration)]
                    print(f"iteration No: {iteration}-----------------------------")
                    if pt_num in [8, 10]: 
                        continue

                    print(float(tmp[8*fsize + 4]))
                    print(float(tmp[8*fsize + 7]))
                    if int(float(tmp[8*fsize + 4])) == ogdl[fsize]: 
                        avgsum += float(tmp[8*fsize + 7])
                        avgdiv += 1
                except Exception as e:
                    print(e, "222ssqwscx")
                
            print(avgdiv)
            if avgdiv != 0:
                graph_array[location][fsize] = avgsum/avgdiv

# plt.boxplot(graph_array)
file_sizes = ["5MB", "10MB", "20MB", "50MB", "100MB"]
temp = pd.DataFrame(columns=locations, index=[1,2,3,4,5])
print(temp)

if pt_num != 8:

    plt.xticks([i+1 for i in range(len(locations))], locations)
    plt.xlabel(f"Locations of PT: {pt_names[pt_num]}")
    plt.ylabel("Time Taken (in sec)")
    plt.title(f"File-Download Time Taken By {pt_names[pt_num]} for each location")
    # plotting

    # structure of graph_array is [location][avgtime]
    plots = []
    for i in range(5):
        plots.append([])


    for i in range(5):
        for j in range(len(locations)):
            plots[i].append(graph_array[j][i])
            #data-points
            temp.iloc[i,j] = graph_array[j][i]
    temp.to_csv(f"selenium_overall_result1000/file_download/graphs-values/{pt_names[pt_num]}_file_data.csv")   
    # plt.show()
    # input()
    # for i in range(5):
        # plt.plot( [i+1 for i in range(len(locations))] , plots[i] , label = file_sizes[i] )

else:

    plt.xticks([i+1 for i in range(len(tor_only_locs))], tor_only_locs)
    plt.xlabel(f"Locations of PT: {pt_names[pt_num]}")
    plt.ylabel("Time Taken (in sec)")
    plt.title(f"File-Download Time Taken By {pt_names[pt_num]} for each location")
    # plotting

    # structure of graph_array is [location][avgtime]
    plots = []
    for i in range(5):
        plots.append([])

    for i in range(5):
        for j in range(len(tor_only_locs)):
            plots[i].append(graph_array[j][i])
            temp.iloc[i,j] = graph_array[j][i]
    temp.to_csv(f"selenium_overall_result1000/file_download/graphs-values/{pt_names[pt_num]}_file_data.csv")   
    input()

    # for i in range(5):
        # plt.plot( [i+1 for i in range(len(tor_only_locs))] , plots[i] , label = file_sizes[i] )

plt.legend()
# plt.show()
