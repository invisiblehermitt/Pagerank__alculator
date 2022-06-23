import numpy as np
import sys

arguments = sys.argv
dataset = open(arguments[1])
dataset = dataset.readlines()

#  handle the dataset
data = dataset[4:len(dataset)]

for i in range(len(data)):  #  去除每一行最后的回车
    #i = i[:len(i)-1]
    data[i] = data[i][:len(data[i])-1]
    data[i] = data[i].split("\t")

connect_sheet = {}  #  记录每个点去往哪些点,即从key 到内容
#for i in range(875713):
for i in data:
    connect_sheet[i[0]] = []
    if connect_sheet.get(i[1]) == None:
        connect_sheet[i[1]] = []

#print("data[0] 的第一项： ", type(connect_sheet.get(data[0][0])))
for i in data:
    connect_sheet.get(i[0]).append(i[1])

#print(len(connect_sheet))
#initial_pr = {}
PR = {}
N = len(connect_sheet)

for i in connect_sheet:
    #initial_pr[i] = 1/N
    PR[i] = 1/N # used to be 0


out_count = {}
for i in connect_sheet:
    out_count[i] = len(connect_sheet.get(i))
#print(out_count['1982'])

def get_outlinks(connect,PR):
    in_links = {}
    for i in connect:
        in_links[i] = []

    for i in connect:
        local_outs = connect.get(i)
        for k in local_outs:
            in_links[k].append(PR[i]/len(local_outs))

    return in_links

def reducer(connect,PR,in_link,N): # connect used to be in the parameters
    #new_inlinks = {}
    #for i in connect:
    #    new_inlinks[i] = []

    for i in in_link:
        PR[i] = (1-0.8)/N
        if len(in_link.get(i)) > 0:
            local_in_link = in_link.get(i)
            #for m in local_in_link:
            PR[i] += 0.8*sum(local_in_link)

    return PR


#print(pagerank_calculater(connect_sheet,PR,out_count,N))

def sort_by_value(dict):  #function which sorts a dictionary by value
    sorted_keys = sorted(dict, key=dict.get, reverse=True)
    #sorted_dict = {}

    #for w in sorted_keys:
    #    sorted_dict[w] = dict[w]
    return sorted_keys

count = 0
#print(get_outlinks(connect_sheet, PR))


while True:
    count += 1
    key_list_by_pr = sort_by_value(PR)
    top1_value = PR[key_list_by_pr[0]]

    link_in = get_outlinks(connect_sheet, PR)
    PR = reducer(connect_sheet,PR,link_in,N)
    #print(PR)
    updated_keylist = sort_by_value(PR)
    updated_top1 = PR[updated_keylist[0]]
    #print(updated_top1)

    if abs(top1_value - updated_top1) < 1e-10:
        #with open("top10_pg.txt", "w") as o:
        #    o.write("Top ten largest page rank: \n")
        #    o.write("Node id:   page rank value: \n")
        #    for i in updated_keylist:
        #        temp = i + '\t' + str(PR[i]) + '\n'
        #        o.write(temp)
            #o.write("end of top 10\n")

        print("Top ten largest page rank: ")
        print("Node id: ", '\t', "page rank value")
        for i in updated_keylist[0:10]:
            print(i, '\t', PR[i])


        with open("pagerank_result.txt","w") as f:
            f.write("Node id:   page rank value: \n")
            for i in PR:
                temp = i + '\t' + str(PR[i]) + '\n'
                f.write(temp)


        #print(updated_keylist[0:10])
        #print(count)
        break

#print("Node id: ", '\t', "page rank value")
#for i in PR:
#    print(i, '\t', PR[i])





