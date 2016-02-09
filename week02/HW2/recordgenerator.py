#!/usr/bin/python
import random
import sys

# get number of records to generate
num_records = int(sys.argv[1])

# generator function to create random integers in the range of 1 to sys.maxint
def gen(n):
    count = 0
    while count < n:
        yield (random.randint(1, sys.maxint))
        count += 1
        
# Generate a set of num_record key,value pairs with integer keys generated by the generator
# and write them to an output file in the form of "integer,NA"
for i in gen(num_records):
    sys.stdout.write('{0},{1}\n'.format(i,"NA"))