import sys

NOISE = 999
input_f_name =""


class object():
    def __init__(self, index =0,dot = (-1,-1), isvisit = 0, c_num = -1):
        self.index = index
        self.dot = dot
        self.isvisit = isvisit
        self.c_num = c_num

def dist(c_pts, o_pts):
    x1, y1 = c_pts
    x2, y2 = o_pts
    dist = (((x2 - x1)**2) + ((y2- y1)**2))**0.5
    return dist

def find_neighbor(c_object ,object_list, eps ):
    n_list =set()
    
    for i in range(len(object_list)):
        if c_object.index != i:
            if dist(c_object.dot, object_list[i].dot) <= eps :
                n_list.add(i)

    return n_list

def output_f(object_list, cluster_id ,C_list):
    str_output_f = input_f_name[0:-4] + "_cluster_"+str(cluster_id)+".txt"
    f = open(str_output_f, 'w')
    for id in C_list :
        f.write(str(id)+"\n")
    f.close()



def DBSCAN(object_list, eps, min_pts,cluster_num):
    cluster_id =0;
    
    for i in range(len(object_list)):
        C_list =[]
        N_list =set()
        
        if object_list[i].isvisit == 0:
            object_list[i].isvisit = 1
            N_list = N_list | find_neighbor(object_list[i],object_list,eps)

            if len(N_list) >= min_pts :
                object_list[i].cluster_num = cluster_id
                C_list.append(i)
                
                while 1 :
                    is_changed = 0
                
                    for ob_id in N_list:
                        if object_list[ob_id].isvisit ==0:
                            object_list[ob_id].isvisit =1
                            n_list = find_neighbor(object_list[ob_id],object_list,eps)
                            #print "n_list = " + str(len(n_list))
                            if len(n_list) >= min_pts :
                                cnt_p_N_list = len(N_list)
                                N_list = N_list | n_list
                                #print "N_list = " + str(len(N_list))
                                if cnt_p_N_list != len(N_list):
                                    is_changed =1
                    
                        if object_list[ob_id].c_num == -1 :
                            object_list[ob_id].c_num = cluster_id
                            C_list.append(ob_id)
                        
                    if is_changed == 0:
                        break
                                        
                if len(C_list) >= min_pts :
                    output_f(object_list, cluster_id ,C_list)
                    # print len(C_list)
                    cluster_id = cluster_id+1
                if cluster_id >= cluster_num:
                    break

            else :
                object_list[i].c_num = NOISE



def pre_treatment(input_f_name) :
    object_list=[]
    f = open(input_f_name)
    def make_clean(str):
        str = str.strip()
        return str
    file_line =[map(make_clean,line.split('\t')) for line in f]
    for i in range(len(file_line)) :
        index = int(file_line[i][0])
        x = float(file_line[i][1])
        y = float(file_line[i][2])
        object_list.append(object(index = index, dot=(x,y)))
    
    f.close()
    return object_list


if __name__ == '__main__' :
    input_f_name = sys.argv[1]
    cluster_num = int(sys.argv[2])
    eps = float(sys.argv[3])
    min_pts = int(sys.argv[4])
    
    object_list = pre_treatment(input_f_name)
    DBSCAN(object_list, eps, min_pts, cluster_num)
    


