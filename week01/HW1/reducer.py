#!/usr/bin/python
## reducer.py
## Author: Ron Cordell
## Description: reducer code for HW1.4
## given a list of intermediate word count files, compute NB classification
import sys
counts = {}
term_counts = {}
spam_doc_ids = []
ham_doc_ids = []
spam_doc_word_count = 0.0
ham_doc_word_count = 0.0
spam_term_count = 0.0
ham_term_count = 0.0
terms = 0.0

for intermediate_file in sys.argv:
    with open(intermediate_file, 'rU') as infile:
        # intermediate files are id <tab> class <tab> word <tab> term_flag <tab> count per line
        for line in infile.readlines():
            word_count = line.split('\t')
            if len(word_count) == 5:
                # some things to make this more readable
                mail_id = word_count[0]
                label = word_count[1]
                word = word_count[2]
                if word_count[3] == '0':
                    vocab_word = False
                else:
                    vocab_word = True
                count = float(word_count[4].strip())

                if (mail_id, label, vocab_word, word) in counts:
                    counts[(mail_id, label, vocab_word, word)] += count
                else:
                    counts[(mail_id, label, vocab_word, word)] = count

spam = { k:v for k,v in counts.items() if k[1] == '1' }
for k in spam:
    spam_doc_word_count += spam[k]
    if k[0] not in spam_doc_ids:
        spam_doc_ids.append(k[0])
    if k[2]:
        if k[3] in term_counts:
            term_counts[k[3]]['spam_count'] += spam[k]
        else:
            term_counts[k[3]] = {'spam_count' : spam[k],
                                 'ham_count' : 0.0,
                                  'prob_ham'  : 0.0,
                                  'prob_spam' : 0.0}
    
ham = { k:v for k,v in counts.items() if k[1] == '0' }
for k in ham:
    ham_doc_word_count += ham[k]
    if k[0] not in ham_doc_ids:
        ham_doc_ids.append(k[0])
    if k[2]:
        if k[3] in term_counts:
            term_counts[k[3]]['ham_count'] += ham[k]
        else:
            term_counts[k[3]] = {'ham_count' : ham[k],
                                 'spam_count' : 0.0,
                                  'prob_ham'  : 0.0,
                                  'prob_spam' : 0.0}
                       
# now we should have consolidated the intermediate counts and we can compute the rest

# count the number of terms
term_count = len(term_counts.keys()) * 1.0

prior = (len(spam_doc_ids)*1.0)/(1.0*(len(spam_doc_ids) + len(ham_doc_ids)))

# calculate the P(term|class) for each term
for term in term_counts:
    term_counts[term]['prob_ham'] = (term_counts[term]['ham_count'] + 1.0)/(ham_doc_word_count + term_count)
    term_counts[term]['prob_spam'] = (term_counts[term]['spam_count'] + 1.0)/(spam_doc_word_count + term_count)

# for debugging
if False:    
    for k in counts:
        print '{0} {1} {2} {3} {4}'.format(k[0],k[1],k[2],k[3],counts[k])
    for t in term_counts:
        print '{0} {1} {2} {3} {4}'.format(t, term_counts[t]['spam_count'], 
                                       term_counts[t]['ham_count'],
                                       term_counts[t]['prob_spam'],
                                       term_counts[t]['prob_ham'])
    print len(spam_doc_ids)
    print len(ham_doc_ids)
    print spam_doc_word_count
    print ham_doc_word_count
    print term_count
    print prior

right = 0.0
for email in spam_doc_ids + ham_doc_ids:
    if email in ham_doc_ids:
        true_class = '0'
    else:
        true_class = '1'
    docs = {k:v for k,v in counts.items() if k[0]==email}
    label = '0'
    prob_spam = 0.0
    prob_ham  = 0.0
    for term in term_counts:
        # does this email contain any of the vocabulary terms
        ham = { k:v for k,v in docs.items() if k[3] == term }
        for h in ham:           
            if ham[h] > 0.0:
                if prob_spam > 0.0:
                    prob_spam = prob_spam * term_counts[term]['prob_spam']**ham[h]
                    prob_ham = prob_ham * term_counts[term]['prob_ham']**ham[h]
                else:
                    prob_spam = prior * term_counts[term]['prob_spam']**ham[h]
                    prob_ham = (1.0 - prior) * term_counts[term]['prob_ham']**ham[h]
    if prob_spam > 0.0:
        if prob_spam > prob_ham:
            label = '1'
    sys.stdout.write('{0}\t{1}\t{2}\n'.format(email, true_class, label))
    if true_class == label:
        right += 1.0
sys.stdout.write('Score: {0}/{1}'.format(right, len(spam_doc_ids) + len(ham_doc_ids)))