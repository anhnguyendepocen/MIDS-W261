#!/usr/bin/python
## mapper.py
## Author: Ron Cordell
## Description: mapper code for HW2.4
## Given input on STDIN read lines and count occurrences of words
## Output a key, value => (token, email id, class, term_flag) = count

import sys
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB

X_train = []
Y_train = []

## Lines in the file have 4 fields:
## ID \t SPAM \t SUBJECT \t CONTENT \n
WORD_RE = re.compile(r"[\w']+")

for line in sys.stdin:
    try:
        email_id, label, subject, body = line.split('\t')
    except ValueError:
        email_id, label, body = line.split('\t')
    
    # extract only words from the combined subject and body text
    X_train.append(subject + ' ' + body)
    Y_train.append(int(label))
    
# Use the TfidVectorizer to create the feature vectors
#vectorizer = TfidfVectorizer(token_pattern = "[\w']+")
vectorizer = TfidfVectorizer()
vf = vectorizer.fit(X_train,Y_train)

clf = MultinomialNB()
clf.fit(vf.fit_transform(X_train), Y_train)
print 'Error Rate: {0}'.format(1.0 - clf.score(vf.fit_transform(X_train), Y_train))

# The change in the tfidf vectorizer to use the same token regex as our mapper results in 
# a 2% increase of training error, from 16% to 18%
clf = BernoulliNB()
clf.fit(vf.fit_transform(X_train), Y_train)
print 1.0 - clf.score(vf.fit_transform(X_train), Y_train)