# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 14:03:00 2016
@author: aritzbi
"""
import nltk
import glob
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
    spanish_stopwords = []
    for word in nltk.corpus.stopwords.words('spanish'):
        word = word.lower()
        spanish_stopwords.append(word)
    #print spanish_stopwords
    with open(inp, 'r') as corpus:
        for line in corpus:
            line = line.replace("\n", "")
            splitted_line = line.split(" ")
            non_stopwords_line = []
            for word in splitted_line:
                if word not in spanish_stopwords:
                    non_stopwords_line.append(word)
            """print "Antes"
            print line
            print line.split(" ")
            print ' '.join(non_stopwords_line)
            print "Despues"""
            output.write(' '.join(non_stopwords_line) + "\n")
    output.close()
