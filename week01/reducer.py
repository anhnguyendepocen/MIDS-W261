#!/usr/bin/python
import sys
sum = 0
for line in sys.stdin:
    try:
        sum += int(line)
    except:
        pass
sys.stdout.write('{0}'.format(sum))