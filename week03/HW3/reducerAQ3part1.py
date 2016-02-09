#!/usr/bin/env python

from operator import itemgetter
import sys

def main(separator='\t'):
    total = 1
    total_first = True
    
    # input comes from STDIN (standard input)
    for line in (sys.stdin):
        item, count = line.split(separator)
        try:
            if item == '*':
                total = int(count)
                if total_first:
                    sys.stderr.write("reporter:counter:Code Call Counters,reducer saw total first,1\n")
                    sys.stderr.write("reporter:counter:Code Call Counters,unique items,1\total")
            else:
                sys.stderr.write("reporter:counter:Code Call Counters,reducer pairs,1\n")
                sys.stdout.write("{0}{1}{2}\n".format(item, separator, count))
                total_first = False

        except ValueError:
            sys.stderr.write("reporter:counter:Code Call Counters,reducer skipped pairs,1\n")            
            # count was not a number, so silently discard this item
            pass
        
if __name__ == "__main__":
    # increment counter for combiner call, write to STDERR
    sys.stderr.write("reporter:counter:Code Call Counters,reducer,1\n")
    main()