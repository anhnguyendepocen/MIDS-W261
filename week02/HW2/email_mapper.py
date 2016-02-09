#!/usr/bin/python
## mapper.py
## Author: Ron Cordell
## Description: mapper code for HW2.3
## Given input on STDIN read lines and count occurrences of words
## Output a key, value => (token, email id, class, term_flag) = count

from math import log, exp
import sys
import re

prior = 0.0
zero_prob_ham = 0
zero_prob_spam = 0
terms = {}
# open the file with the term probabilities (model) and load into the terms dictionary
# each line in the file is 
#   term <tab> ham_probability <tab> ham_count <tab> spam_prob <tab> spam_count <tab> prior

# all values are floats

with open('term_probabilities.txt','r') as termfile:
    for line in termfile.readlines():
        term, ham_prob, ham_count, spam_prob, spam_count, _prior = line.strip().split('\t')
        terms[term.strip()] = {'ham_prob'  : float(ham_prob),  'ham_count'  : float(ham_count),
                       'spam_prob' : float(spam_prob), 'spam_count' : float(spam_count)}
        prior = float(_prior)

## Lines in the file have 4 fields:
## ID \t SPAM \t SUBJECT \t CONTENT \n
WORD_RE = re.compile(r"[\w']+")

# read each line from stdin, one email per line
for line in sys.stdin:
    log_prob_ham = log(1.0 - prior)
    log_prob_spam = log(prior)

    try:
        email_id, label, subject, body = line.split('\t')
    except ValueError:
        email_id, label, body = line.split('\t')
        subject = ''

    pred_label = None
        
    # extract only words from the combined subject and body text
    text = WORD_RE.findall(subject + ' ' + body)
    for token in text:
        t = token.strip().lower()
        if t in terms:
            # if we have a zero probability for either class conditional then add a minute value
            # to offset the effects
            if terms[t]['spam_prob'] > 0.0:
                log_prob_spam += log(terms[t]['spam_prob'])
                
                # if the term only occurs in spam, then mark this as spam and move on.
                if terms[t]['ham_prob'] <= 0.0:
                    pred_label = '1'
                    zero_prob_ham += 1
            if terms[t]['ham_prob'] > 0.0: 
                log_prob_ham += log(terms[t]['ham_prob'])
                
                # if we've only ever seen this term in ham, then mark as such and move on.
                if terms[t]['spam_prob'] <= 0.0:
                    pred_label = '0'
                    zero_prob_spam += 1

                    
    # if we didn't encounter a term that's not in one class then calculate the class
    if not pred_label:
        # We have what we need to classify the email
        # emit the classification
        if log_prob_spam > log_prob_ham:
            pred_label = '1'
        else:
            pred_label = '0'
            
    # for each email emit the id <tab> label <tab> prediction <tag> log_prob_ham <tab> log_prob_spam
    print '{0}\t{1}\t{2}\t{3}\t{4}'.format(email_id, label, pred_label, log_prob_ham, log_prob_spam)
    
# after all emails have been processed emit :<tab> zero ham probability count <tab> zero spam probability count
# the ':' lets the reducer know to treat it differently from the email classification
# pad out the end to keep the number of fields consistent
print ':\t{0}\t{1}\t{2}\t{3}'.format(zero_prob_ham, zero_prob_spam, ' ', ' ')