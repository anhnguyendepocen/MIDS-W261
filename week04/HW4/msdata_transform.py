# HW 4.2
#
# Read a CSV file that contains page visits by customers
# A customer id record is followed by a number of page id records which are the pages
# the customer visited on the web site
# Transform the data such that the page visits contain the customer ids on the same record
# The result is the elimination of the standalone customer id record and an extended page
# visit record containing the page id and customer id
# The file contains other records which are output unmodified
#
import sys
with open('anonymous-msweb.data','rU') as datafile:
    
    # iterate over the lines in the data file
    for line in datafile.readlines():
        
        # split the line into the CSV fields (tokens)
        tokens = line.strip().split(',')
        
        # if a customer record then retain the customer id
        if tokens[0] == 'C':
            customer_id = tokens[2]
            
        # if a page visit record then transform to append the customer id
        # V,pageid,count,C,cust_id
        elif tokens[0] == 'V':
            sys.stdout.write('{0},{1},{2},{3},{4}\n'.format('V',tokens[1],tokens[2],'C',customer_id))
            
        # otherwise just output the line
        else:
            sys.stdout.write(line)