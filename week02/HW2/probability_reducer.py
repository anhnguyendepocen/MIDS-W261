#!/usr/bin/python
## reducer.py
## Author: Ron Cordell
## Description: reducer code for HW1.4
## given a list of intermediate word count files, compute NB classification
import sys

term_counts = {}
spam_doc_ids = []
ham_doc_ids = []
spam_doc_word_count = 0.0
ham_doc_word_count = 0.0
spam_term_count = 0.0
ham_term_count = 0.0
terms = 0.0
current_key = None
current_count = 0

# STDIN consists of single lines of: token <tab> id <tab> class <tab> term_flag <tab> count
# Assume that the proper parameters have been set such that Hadoop knows to treat the first 4 fields
# as the key so that they are properly sorted when they reach the reducer
# See http://blog.cloudera.com/blog/2013/01/a-guide-to-python-frameworks-for-hadoop/ for an example

# perform the accumulation functions for each key, value received
def accumulate_key(key , _count, spam_doc_word_count, ham_doc_word_count, term_counts):
    # accumulate the key, values in a dictionary
    _token = key[0]
    _id = key[1]
    _label = key[2]
    _term = key[3]

    # accumulate into ham and spam dictionaries also
    if _label == '1':
        spam_doc_word_count += _count
        if _id not in spam_doc_ids:
            spam_doc_ids.append(_id)
        if _term == '1':
            if _token in term_counts:
                term_counts[_token]['spam_count'] += _count
            else:
                term_counts[_token] = {'spam_count' : _count,
                                     'ham_count' : 0.0,
                                      'prob_ham'  : 0.0,
                                      'prob_spam' : 0.0} 
    else:                
        ham_doc_word_count += _count
        if _id not in ham_doc_ids:
            ham_doc_ids.append(_id)
        if _term == '1':
            if _token in term_counts:
                term_counts[_token]['ham_count'] += _count
            else:
                term_counts[_token] = {'ham_count' : _count,
                                      'spam_count' : 0.0,
                                      'prob_ham'  : 0.0,
                                      'prob_spam' : 0.0}
    return spam_doc_word_count, ham_doc_word_count

# process the STDIN stream
for line in sys.stdin:
    # split the line into the key components and the value
    token, email_id, label, term, token_count = line.split('\t')

    # this makes reading the code a little easier
    if term == '0':
        vocab_word = False
    else:
        vocab_word = True

    # if we've been accumulating for this key, keep accumulating
    # this works because the input is sorted on the key
    if current_key == (token, email_id, label, term):
        current_count += int(token_count)
    else:
        # we've just received a different key from what we've been accumulating
        # wrap up with the current key
        if current_key:
            spam_doc_word_count, ham_doc_word_count = accumulate_key(current_key, 
                                                                     float(current_count), 
                                                                     spam_doc_word_count, 
                                                                     ham_doc_word_count, 
                                                                     term_counts)
        # start a new accumulation    
        current_count = int(token_count)
        current_key = (token, email_id, label, term)

# add the last key we've been accumulating
if current_key == (token, email_id, label, term):
    spam_doc_word_count, ham_doc_word_count = accumulate_key(current_key, 
                                                             float(current_count), 
                                                             spam_doc_word_count, 
                                                             ham_doc_word_count, 
                                                             term_counts)      
                       
# now we should have consolidated the intermediate counts and we can compute the rest

# count the number of terms
term_count = len(term_counts.keys()) * 1.0
# compute the prior
prior = (len(spam_doc_ids)*1.0)/(1.0*(len(spam_doc_ids) + len(ham_doc_ids)))

# calculate the P(term|class) for each term

# HW 2.4 - IMPLEMENT LAPLACE +1 SMOOTHING HERE
# HW 2.5 - IMPLEMENT MIN 3 TERM COUNT HERE

terms_to_drop = []
for term in term_counts:
    # if either the spam or ham term count is > 3, keep this term in the model
    if term_counts[term]['ham_count'] >= 3 or term_counts[term]['spam_count'] >= 3:
        term_counts[term]['prob_ham'] = (term_counts[term]['ham_count'] + 1)/(ham_doc_word_count + term_count)
        term_counts[term]['prob_spam'] = (term_counts[term]['spam_count'] + 1)/(spam_doc_word_count + term_count)
    else:
        # add the term to be removed to the list; we can't remove it while iterating over the dictionary
        terms_to_drop.append(term)

for term in terms_to_drop:
    term_counts.pop(term, None)  

# now emit the model
for term in term_counts:
    # output term <tab> probability_ham <tab> ham_count <tab> probability_spam <tab> spam_count <tab> prior
    print '{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(term, term_counts[term]['prob_ham'], 
                                           term_counts[term]['ham_count'],
                                           term_counts[term]['prob_spam'], 
                                           term_counts[term]['spam_count'], 
                                           prior)