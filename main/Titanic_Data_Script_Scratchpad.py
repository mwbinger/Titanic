__author__ = 'Andrew'

import numpy as np
from random import random, randrange
from pylab import *
import matplotlib
import numpy as np
import Basic_IO_functions as io

#get the csv file and convert into an array
train_array = io.read_csv_into_array("train.csv")

#Create a 2d array of just survive and some other element
survive_array = np.array([train_array[:,0]])
gender_array = np.array([train_array[:,3]])

#concatenate the two arrays to be two columns with many rows
survive_gender_array = ([])

#survive_gender_array = [survive_array[0,2],gender_array[0,2]]

i = 0
ii = survive_array.size
while i < ii:
    survive_gender_array.append((survive_array[0,i],gender_array[0,i]))
    print i
    #print 'printing survive gender array'
    #print survive_gender_array
    i = i+1

#print out that result in a table
#io.convert_into_csv(survive_gender_array,"array concat")

#do a linear regression on the array against the first column