import sys
import math

#A function to obtain cosine-similarity for two users
def user_simil(user_id_1, user_id_2):

   # To get both rated items
    both_rated = {}
    for item in train_dic[user_id_1]:
        if item in train_dic[user_id_2]:
            both_rated[item] = 1

    number_of_ratings = len(both_rated)

    # Checking for ratings in common
    if number_of_ratings == 0:
        return 0

    # Sum up the squares of ratiedvalue of each user
    user_1_square_sum = sum([(train_dic[user_id_1][item])**2 for item in train_dic[user_id_1]])
    user_2_square_sum = sum([(train_dic[user_id_2][item])**2 for item in train_dic[user_id_2]])

    # Sum up the product value of both ratied value for each item
    both_sum = sum([train_dic[user_id_1][item] * train_dic[user_id_2][item] for item in both_rated])

    # Calculate the cosine-similarity
    numerator_value = both_sum
    denominator_value = math.sqrt(user_1_square_sum) * math.sqrt(user_2_square_sum)

    if denominator_value == 0:
        return 0
    else:
        r = numerator_value / denominator_value
        return r

#Finds 30 other users who are most similar to user
def most_similar_users(user_id, item ,number_of_users):

    # returns the number_of_users (similar persons) for a given specific person
    most_simil_list = [(user_simil(user_id, other_user), other_user) for other_user in train_dic \
                       if other_user != user_id and item in train_dic[other_user]]

    # Sort the similar persons so the highest scores person will appear at the first
    most_simil_list.sort()
    most_simil_list.reverse()
    return most_simil_list[0:number_of_users]

#The average of all the scores the user has
def get_average(user):
    user_data = train_dic[user].items()
    length = len(user_data)
    sum = 0
    for item, rating in train_dic[user].items():
        sum += rating
    return float(sum) / float(length)

#Expect a score.
def user_rec(test_dic, train_f_name):

    filename = train_f_name + "_prediction.txt"
    output_file = open(filename, 'w')

    for test_user in test_dic:
        test_user_average = get_average(test_user)
        for unknown_item in test_dic[test_user]:
            most_simil_list = most_similar_users(test_user,unknown_item, 30)
            sum_simil = 0
            sum_simil_rank = 0
            for other_user in most_simil_list:
                if unknown_item in train_dic[other_user[1]]:
                    sum_simil += abs(other_user[0])
                    sum_simil_rank += other_user[0]*\
                                      (train_dic[other_user[1]][unknown_item] - \
                                       get_average(other_user[1]))

            if sum_simil == 0:
                r = test_user_average
                if r<1:
                    r = 1
            else :
                r = test_user_average + (sum_simil_rank / sum_simil)
                if r<1:
                    r=1

            result_str = str(test_user)+"\t"+str(unknown_item)+"\t"+str(r)+"\n"
            output_file.write(result_str)

    output_file.close()


#Test_file preprocessing
def pre_treatment_test(input_f_name):
    test_dic ={}
    error_list =[]
    f= open(input_f_name)

    def make_clean(str):
        str = str.strip()
        return str

    test_line = [map(make_clean, line.split('\t')) for line in f]

    for i in range(len(test_line)):
        user_id = int(test_line[i][0])
        item_id = int(test_line[i][1])
        test_dic.setdefault(user_id, {})
        test_dic[user_id].setdefault(item_id,0)

    f.close()
    return test_dic

#Training_file_preprocessing
def pre_treatment_train(input_f_name):
    train_dic = {}
    f = open(input_f_name)

    def make_clean(str):
        str = str.strip()
        return str

    train_line = [map(make_clean, line.split('\t')) for line in f]

    for i in range(len(train_line)):
        user_id = int(train_line[i][0])
        item_id = int(train_line[i][1])
        rating = int(train_line[i][2])
        train_dic.setdefault(user_id, {})
        train_dic[user_id][item_id] = rating

    f.close()
    return train_dic

#main
if __name__ == '__main__':
    train_f_name = sys.argv[1]
    test_f_name = sys.argv[2]

    global train_dic
    global test_dic
    train_dic = pre_treatment_train(train_f_name)
    test_dic = pre_treatment_test(test_f_name)
    user_rec(test_dic,train_f_name)


