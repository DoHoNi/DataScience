#-*- coding: utf-8 -*-
import sys
import collections

#The class that contains the information of node in decision tree.
# 'col' is index of standard attribute
# 'level' is level of decision tree.
# 'value_list' has values of standard attribute
# 'child_list' has list of child nodes
# 'result' has result, If it is a leaf node
# 'rp_result' is result that replace the actual result
class decision_node(object):
    def __init__(self, col=-1, level=None, value_list=None, child_list = None, result=None,rp_result = None):
        self.col = col
        self.level = level
        self.value_list = value_list
        self.child_list = child_list
        self.result = result
        self.rp_result = rp_result

#Returns the attribute value that has the largest number at class lable
def best_result(result_dict):
    result = None
    best_cnt =0
    for r in result_dict.keys():
        if result_dict[r] > best_cnt:
            best_cnt = result_dict[r]
            result = r
    return result

#Check the values in a specific column, and return a list of list of rows with the same value
def divideset(rows, column, col_values):
    div_rowss =[]
    for value in col_values :
        #The function checks that the value of a specific column in the row that is entered as a parameter is equal to value.
        divid_func = lambda row: row[column] == value
        t_rows = [row for row in rows if divid_func(row)]
        div_rowss.append(t_rows)
    return div_rowss

#Counts the values of the class label respectively.
def count_class(rows):
    result = collections.defaultdict(int)
    for row in rows:
        r = row[len(row)-1]
        result[r] +=1
    return dict(result)

#Function to calculate entropy
def entropy(rows):
    from math import log
    log2 = lambda x: log(x)/ log(2)
    results = count_class(rows)
    ent = 0.0
    for r in results:
        p = float(results[r])/len(rows)
        ent -= p*log2(p)
    return ent

#This function that counts the total number of rows in a list of rows
def count_rowss(rowss):
    cnt =0
    for rows in rowss:
        cnt += len(rows)
    return cnt

#This recursive function that builds the tree by choosing the best dividing criteria for the current set
def buildtree(attri_rows,level) :
    final_result = collections.defaultdict(int)
    result_cnt = count_class(attri_rows)
    
    if len(attri_rows)<2 or level > len(attri_rows[0]) :
        return decision_node(result = result_cnt)

    rp_result = best_result(result_cnt)
    cur_entropy = entropy(attri_rows)

    best_gain = 0.0
    best_col = None
    best_value_list = None
    best_div_list =None

    col_last = len(attri_rows[0])-1
    for col in range(0,col_last):
        col_values = list(set([row[col] for row in attri_rows]))
        
        #Attribute selection measure is ID3
        div_rowss = divideset(attri_rows, col, col_values)
        if count_rowss(div_rowss) >1 :
            gain = cur_entropy
            div_rowss_cnt = count_rowss(div_rowss)
            for i in range(0,len(div_rowss)):
                p = float(len(div_rowss[i])) / div_rowss_cnt
                gain -= p * entropy(div_rowss[i])
            if gain > best_gain :
                best_gain = gain
                best_col = col
                best_value_list = col_values
                best_div_list = div_rowss

    if best_gain >0:
        node_list = []
        for rows in best_div_list:
            new_node = buildtree(rows,level+1)
            node_list.append(new_node)
        return decision_node(col=best_col, value_list = best_value_list, child_list = node_list,rp_result=rp_result)
    else :
        return decision_node(result =count_class(attri_rows))

#The function that determines the class label value of the test set
def test_decision(tree,test_rows):
    results_rows = []
    for row in test_rows:
        result = classify(tree,row)
        row.append(result)
        results_rows.append(row)
    return results_rows

#Search the decision tree and return class label value
def classify(tree,test_row):
    if tree.result != None :
        return tree.result.keys()[0]
    else :
        val = test_row[tree.col]
        #If there is a child node that matches value
        if val in tree.value_list:
            for i in range(0,len(tree.value_list)):
                if val == tree.value_list[i]:
                    return classify(tree.child_list[i],test_row)
        #If there is no child node matching value, use 're_result'.
        else:
            return tree.rp_result
#check the decision tree at consol window
def print_tree(tree,attri_name):
    if tree.result != None:
        print tree.result
    else:
        print attri_name[tree.col] +'?'
        for i in range(0,len(tree.value_list)):
            print ' '+ tree.value_list[i] + '->'
            print_tree(tree.child_list[i],attri_name)

#Functions that print the results to a file
def print_result_f(f_result_name,attri_name,result_rows):
    f = open(f_result_name,'w')
    str = "\t".join(attri_name)+'\n'
    f.write(str)
    for row in result_rows:
        str = "\t".join(row)+'\n'
        f.write(str)
    f.close()

#This function is preprocessing function that read file and make them into lists
def pre_treatment(file_name) :
    f = open(file_name)
    def make_clean(str):
        str = str.strip()
        return str
    file_line = [map(make_clean,line.split('\t')) for line in f]
    attri_name = file_line.pop(0)      #att_name list
    attri_list = file_line             #att list
    f.close()
    return attri_name,attri_list

# Main Function
if __name__ == '__main__' :
    #You need to modify the program path.
    f_train_name = "/Users/dohuni/Desktop/dt.py/"+sys.argv[1]
    f_test_name = "/Users/dohuni/Desktop/dt.py/"+sys.argv[2]
    f_result_name = "/Users/dohuni/Desktop/dt.py/"+sys.argv[3]

    attri_name,attri_list = pre_treatment(f_train_name)
    test_name,test_rows = pre_treatment(f_test_name)
    tree = buildtree(attri_list,1)
    #print_tree(tree,attri_name)
    result_rows = test_decision(tree,test_rows)
    print_result_f(f_result_name,attri_name,result_rows)





