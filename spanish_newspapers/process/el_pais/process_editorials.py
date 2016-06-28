# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 10:22:28 2016

@author: aitor
"""
#USAGE: python process_editorials.py items.json editorials.text

import json
import string
import sys


if __name__ == '__main__':
    print "Starting..."
    # check and process input arguments
    if len(sys.argv) < 3:
        print globals()['__doc__'] % locals()
        sys.exit(1)
    inp, outp = sys.argv[1:3]
    output = open(outp, 'w')
    
    i = 0    
    editorials = json.load(open(inp, 'r'))
    for editorial in editorials:
        text = editorial['text'].lower()
        exclude = set(string.punctuation)
        processed_text = ''.join(ch for ch in text if ch not in exclude)
        processed_text = processed_text.encode('utf-8')
        output.write(processed_text + "\n")
        i = i + 1
        if (i % 5000 == 0):
            print "Saved %s editorials" % (i)
 
    output.close()
    print "Finished Saved %s editorials" % (i)