# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 14:27:07 2016

@author: aitor
"""

#USAGE: python merge_txts.py boe boe.text text

import glob
import string
import sys


if __name__ == '__main__':
    print "Starting..."
    # check and process input arguments
    if len(sys.argv) < 3:
        print globals()['__doc__'] % locals()
        sys.exit(1)
    inp, outp, extension = sys.argv[1:4]
    output = open(outp, 'w')
    print 'Input folder:', inp
    print 'Outpuf file:', outp
    i = 0    
    MINIMUN_LENGTH = 20 # we do not process paragraphs with less than this chars     
    exclude = set(string.punctuation) 
    exclude.add(u'–')      
    files_path = inp + '/*.' + extension
    print 'Starting file processing:' + files_path
    for book_file in glob.glob(files_path):
        i = i + 1
        print 'Processing:', book_file
        with open(book_file, 'r') as book:
            for line in book:
                text = line.strip().lower()
                if len(text) > MINIMUN_LENGTH:
                    processed_text = ''.join(ch for ch in text if ch not in exclude)
                    #processed_text = processed_text.encode('utf-8')
                    output.write(processed_text + "\n") 
        if (i % 200 == 0):
            print "Saved %s elements" % (i)
    output.close()
    print "Finished Saved %s elements" % (i)