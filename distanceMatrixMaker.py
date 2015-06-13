import numpy
import csv
from decimal import *
from scipy.spatial import distance

#define the weights for the different attribute distances
keywords_weight = Decimal(1.0)
wordcount_weight = Decimal(0.4)
num_key_words_weight = Decimal(0.2)
num_hash_weight = Decimal(0.5)
if_in_reply_weight = Decimal(0.2)
username_weight = Decimal(0.0)
screen_name_weight = Decimal(0.0)
url_weight = Decimal(0.0)
verified_weight = Decimal(0.0)
followers_count_weight = Decimal(0.5)
favorites_count_weight = Decimal(0.6)
tweet_count_weight = Decimal(0.3)
num_links_weight = Decimal(0.1)
user_mentions_weight = Decimal(0.1)
symbols_used_weight = Decimal(0.3)
time_weight = Decimal(0.7)
user_age_weight = Decimal(0.3)
retweet_count_weight = Decimal(0.6)
favorited_count_weight = Decimal(0.6)
media_freq_weight = Decimal(0.4)

def compute_distance(instance1, instance2):
    total_distance = 0

    #
    total_distance += keywords_weight * compute_keyword_distance(instance1[0], instance2[0])

    total_distance += wordcount_weight * euclidean(instance1[1], instance2[1])

    total_distance += num_key_words_weight * euclidean(instance1[2], instance2[2])

    total_distance += num_hash_weight * euclidean(instance1[3], instance2[3])

    total_distance += if_in_reply_weight * euclidean(instance1[4], instance2[4])

    total_distance += username_weight * compute_string_distance(instance1[5], instance2[5])

    total_distance += screen_name_weight * compute_string_distance(instance1[6], instance2[6])

    total_distance += url_weight * compute_string_distance(instance1[7], instance2[7])

    total_distance += verified_weight * compute_verified_distance(instance1[8], instance2[8])

    total_distance += followers_count_weight * euclidean(instance1[9], instance2[9])

    total_distance += favorited_count_weight * euclidean(instance1[10], instance2[10])

    total_distance += tweet_count_weight * euclidean(instance1[11], instance2[11])

    total_distance += num_links_weight * euclidean(instance1[12], instance2[12])

    total_distance += user_mentions_weight * euclidean(instance1[13], instance2[13])

    total_distance += symbols_used_weight * euclidean(instance1[14], instance2[14])

    total_distance += time_weight * compute_time_distance(instance1[15], instance2[15])

    total_distance += user_age_weight * euclidean(instance1[16], instance2[16])

    total_distance += retweet_count_weight * euclidean(instance1[17], instance2[17])

    total_distance += favorited_count_weight * euclidean(instance1[18], instance2[18])

    total_distance += media_freq_weight * euclidean(instance1[19], instance2[19])

    return total_distance


def compute_keyword_distance(tweets1, tweets2):
    # currently computes distance by finding words that are the same and then returning 1/ num shared words
    # if there are no matching words, returns a distance of 2
    shared_words = 0.0

    pure_string1 = tweets1.strip('\'')
    pure_string2 = tweets2.strip('\'')
    
    tweet_set1 = set(pure_string1.split())
    tweet_set2 = set(pure_string2.split())
    
    shared_words = tweet_set1 & tweet_set2
    shared_words_count = len(shared_words)
    
    if shared_words_count != 0.0:
        return Decimal(1.0 / float(shared_words_count))
    else:
        return Decimal(2.0)

def compute_string_distance(string1, string2):
    return abs(len(string2) - len(string1))

def compute_verified_distance(verif1, verif2):
    if verif1 == 'True' and verif2 == 'True':
        return 1
    elif verif1 == 'False' and verif2 == 'False':
        return 1
    else:
        return 0

def compute_time_distance(time1, time2):
    return euclidean(get_time_val(time1), get_time_val(time2))

def get_time_val(time):
    if time == 'late':
        return '0.0'
    if time == 'morning':
        return '1.0'
    if time == 'afternoon':
        return '2.0'
    if time == 'evening':
        return '3.0'

def euclidean(this_x, this_y):
    dec_x = Decimal(this_x)
    dec_y = Decimal(this_y)
    return numpy.sqrt(dec_x**2 + dec_y**2)

# array to hold all the instances in this dataset
instances = []

folder = "csvData\\"
input_filename = "twitter_users_500.csv"
output_filename = "distance_matrix_500.csv"

distance_matrix = numpy.zeros(shape=(2354, 2354))

with open((folder + input_filename), 'rb') as my_file:
    csv_reader = csv.reader(my_file)
    for row in csv_reader:
        instances.append(row)

instances_size = len(instances)
distance_matrix = numpy.zeros(shape=(instances_size, instances_size))
# Populate the distance matrix by filling up rows at a time
for x in range(instances_size):
    for y in range(instances_size):
        print "Working on cell {px},{py}".format(px=x, py=y)
        if x == y:
            distance_matrix[x][y] = 0.0
        else:
            if distance_matrix[y][x] != 0.0:
                # avoid recalculating
                distance_matrix[x][y] = distance_matrix[y][x]
            else:
                distance_matrix[x][y] = compute_distance(instances[x], instances[y])

with open((folder + output_filename), "w") as output_file:
    for row in distance_matrix:
        csv_row = ','.join(map(str, row))
        output_file.write(csv_row + '\n')
print "Done"


