#!/usr/bin/env python

from itertools import groupby
from operator import itemgetter
import sys

def read(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main(separator='\t'):
    total = 1
    total_first = True
    
    # input comes from STDIN (standard input)
    data = read(sys.stdin, separator=separator)
    # groupby groups multiple word-count pairs by word,
    # and creates an iterator that returns consecutive keys and their group:
    #   current_word - string containing a word (the key)
    #   group - iterator yielding all ["&lt;current_word&gt;", "&lt;count&gt;"] items
    for current_word, group in groupby(data, itemgetter(0)):
        try:
            total_count = sum(int(count) for current_word, count in group)
            if current_word == '*':
                total = total_count
                sys.stderr.write("reporter:counter:Code Call Counters,reducer total indicators,1\n")
                sys.stderr.write("reporter:counter:Code Call Counters,reducer word count,{0}\n".format(total))
                if total_first:
                    sys.stderr.write("reporter:counter:Code Call Counters,reducer recvd total first,1\n")
            else:
                sys.stderr.write("reporter:counter:Code Call Counters,reducer processed,1\n")
                sys.stdout.write("{0:20}\t{1:10}\t{2}\n".format(current_word, total_count, 
                                                              float(total_count)/float(total))) 
                total_first = False
                
        except ValueError:
            sys.stderr.write("reporter:counter:Code Call Counters,reducer skipped pairs,1\n")            
            # count was not a number, so silently discard this item
            pass

if __name__ == "__main__":
    # increment counter for combiner call, write to STDERR
    sys.stderr.write("reporter:counter:Code Call Counters,reducer,1\n")
    main()