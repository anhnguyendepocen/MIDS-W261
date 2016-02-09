#!/usr/bin/python
## reducer.py
## Author: Ron Cordell
## Description: reducer code for HW1.4
## given a list of intermediate word count files, compute NB classification
import sys
from math import log,exp

zero_prob_ham = 0
zero_prob_spam = 0

right = 0
wrong = 0

# STDIN consists of lines of one of two kinds - one that starts with ':' and one that doesn't
# For the line that starts with a colon, accumulate the zero probability counts it has
# Otherwise the line is the email id, label, class, log probability ham, log probability spam

# Assume that the proper parameters have been set such that Hadoop knows to treat the first 4 fields
# as the key so that they are properly sorted when they reach the reducer
# See http://blog.cloudera.com/blog/2013/01/a-guide-to-python-frameworks-for-hadoop/ for an example

# process the STDIN stream
for line in sys.stdin:
    fields = line.strip().split('\t')
    
    # if this isn't a zero probability count 
    if fields[0] != ':':
        # output the email id, label, prediction
        print '{0}\t{1}\t{2}\t{3}\t{4}'.format(fields[0], fields[1], fields[2], fields[3], fields[4])
        
        # tally the error rate
        if fields[1].strip() != fields[2].strip():
            wrong += 1
        else:
            right += 1
    else:
        # this is actually the zero probability counters so tally them
        zero_prob_ham += int(fields[1])
        zero_prob_spam += int(fields[2])
    
print 'Error Rate: {0}/{1}'.format(wrong, right + wrong)
print 'Zero Probabilities: Spam {0} \tHam {1}'.format(zero_prob_spam, zero_prob_ham)