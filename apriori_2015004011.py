
# -*- coding: utf-8 -*-
# 2015004011 / Dohyun Kim / major in Software Engineering
#Implement apriori algorithm with Python

import sys
from collections import Counter
from itertools import combinations


# Self_Joinging
def Self_Joining(pre_level_list,level) :
    this_c_list = []
    if level < 3 :                                          #Handle for level 2 separately
        uni_set = combinations(pre_level_list,level)
        for item in uni_set:                                #To create a list with 'set' as an element
            this_c_list.append(set(item))
    else :                                                  #Handle for other level
        uni_set = set()
        for a in pre_level_list:
            for b in pre_level_list:
                uni_set = set(a)|set(b)                             #Union of two previous results
                #Check the condition of the candidate
                if a != b and len(uni_set) == level and \
                    prunning(pre_level_list, uni_set, level) \
                    and check_duplicate(uni_set,this_c_list):
                        this_c_list.append(uni_set)             #Add as a candidate
    return this_c_list

#Used by  'Self_Joining' function
#check duplicate
def check_duplicate(uni_set, this_c_list) :
    for item in this_c_list:
        if set(item)&uni_set == uni_set:
            return False
    return True

#Prunning using the downward closure property
def prunning(pre_level_list, uni_set, level):
    cnt = 0
    for list in pre_level_list:
        if set(list)&uni_set == set(list):
            cnt += 1
        if cnt == level:
            return True
    return False

#Divide the dictionary's key to make a list of lists with integer elements.
def dic_to_list(this_level_dic):
    this_list = []
    for item in this_level_dic.keys() :
        this_list.append(set(item.split(" ")))
    return this_list

#Scan database to check frequency
def check_frequent(this_level_list_c) :
    this_level_dic = {}
    item_name = ""
    for item in this_level_list_c :                             #Initialize dictionary
        item_name = " ".join(list(item))                        #with element as key and support as value
        this_level_dic[item_name] = 0
    
    for item in this_level_list_c :                                 #Scan database
        for transaction in transaction_list :
            if set(item).issubset(set(transaction)) :
                item_name = " ".join(list(item))
                this_level_dic[item_name] = this_level_dic[item_name] +1
    return this_level_dic

#Delete candidate if support is less than min_support
def pruning_frequent(this_level_dic) :
    next_level_dic = this_level_dic.copy()
    for item in next_level_dic.keys() :
        if next_level_dic[item] < min_sup_cnt :
            del next_level_dic[item]
    return next_level_dic

#Used by print_association
#Divide int by float type
def div_int( num1 , num2) :
    result = float(num1)/float(num2)
    return result*100

#Used by print_association
#make output format
def make_str (item_set, sub_set,all_trans_cnt,cnt_item,cnt_sub):
    assosiation_set = item_set - set(sub_set)
    my_str = "{"+ ",".join(list(sub_set))+ "}\t{" + ",".join(list(assosiation_set)) + "}\t" + str('%.2f'%div_int(cnt_item,all_trans_cnt)) +"\t"+str('%.2f'%div_int(cnt_item,cnt_sub))
    return my_str

#make result output with associative rule
def print_association(all_trans_cnt,level,this_level_list,transaction) :
    f = open(output_f_str,'a')
    cnt_item =0
    cnt_sub =0
    
    for item_set in this_level_list :                               #frequent item
        for i in range(1,level) :
            for sub_set in combinations(item_set, i):               #associative_item_set
                cnt_item =0
                cnt_sub =0
                for tran in transaction :
                    if  set(item_set).issubset(set(tran)) :
                        cnt_item +=1
                    if  set(sub_set).issubset(set(tran)) :
                        cnt_sub +=1
                f.write( make_str(item_set, sub_set,all_trans_cnt,cnt_item,cnt_sub)+"\n")
    f.close()

#Generate first result
def first_freq(f) :
    counter = Counter()
    while 1 :
        line = f.readline()
        if not line : break
        if '\r\n' in line :
            line = line[:-2]
        if '\n' in line :
            line = line[:-1]
        split_line = line.split('\t')
        transaction_list.append(split_line)
        counter.update(split_line)
    return dict(counter)


#main

open_f_str = "/Users/dohuni/Desktop/test/"+sys.argv[2]
output_f_str ="/Users/dohuni/Desktop/test/"+sys.argv[3]
f = open(open_f_str,'r')

transaction_list =[]                                        #transaction_list
L_list = [[0]]                                              #list of frequent item set about each level

level_1_dict= first_freq(f)                                 #Generate fist result
level_1_list = level_1_dict.keys()                          #make a list of frequent items

all_trans_cnt = len(transaction_list)                       # all transaction count
min_sup_cnt = all_trans_cnt * 0.01 * int(sys.argv[1])        # minimum support count

C_list = level_1_list                                       # Level 1 candidates
level_1_dict = pruning_frequent(level_1_dict)
L_list.append(level_1_dict.keys())

level = 1

while 1 :
    level = level+1
    C_list = Self_Joining(L_list[level-1],level)            #self joining
    this_level_dic = check_frequent(C_list)                 #Scan database to check frequency
    this_level_dic = pruning_frequent(this_level_dic)       #Delete candidate if support is less than min_support
    this_level_list = dic_to_list(this_level_dic)           #prepare to put in L_list

    if len(this_level_dic) == 0 :                           #Termination condition
        break
    print_association(all_trans_cnt,level,this_level_list,transaction_list)     # print result at file
    L_list.append(this_level_list)





