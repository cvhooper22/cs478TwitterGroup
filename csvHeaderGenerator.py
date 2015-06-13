import numpy
import csv
from decimal import *


# array to hold all the instances in this dataset
instances = []

folder = "csvData\\"
input_filename = "twitter_users_12.csv"
output_filename = "distance_headers_12.csv"

distance_matrix = numpy.zeros(shape=(2354, 2354))

with open((folder + input_filename), 'rb') as my_file:
    csv_reader = csv.reader(my_file)
    for row in csv_reader:
        instances.append(row)

instances_size = len(instances)
distance_matrix = numpy.zeros(shape=(instances_size, instances_size))
# Populate the distance matrix by filling up rows at a time

header_array = []
for x in range(instances_size):
    header_array.append(instances[x][6].strip("\'"))


with open((folder + output_filename), "w") as output_file:
    headers_row = ','.join(header_array)
    output_file.write(headers_row)
    
print "Done"


