#!/usr/bin/python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
ham = []
spam = []
with open('classification_results.txt','r') as infile:
    for line in infile.readlines():
        try:
            _id, label, cls, lh, ls = line.strip().split('\t')
            try:
                ham.append(float(lh))
            except:
                ham.append(0.0)
            try:
                spam.append(float(ls))
            except:
                spam.append(0.0)
        except:
            pass

plt.figure(figsize=(15,5))
p = plt.subplot(1, 2, 1)
p.hist(ham,100)
plt.title('Ham Log Probability Frequencies')

p = plt.subplot(1, 2, 2)
p.hist(spam,100)
plt.title('Spam Log Probability Frequencies')     