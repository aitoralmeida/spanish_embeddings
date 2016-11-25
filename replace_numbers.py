import glob
import string
import sys
import re
if __name__ == '__main__':
    print "Starting..."
    # check and process input arguments
    if len(sys.argv) < 3:
        print globals()['__doc__'] % locals()
        sys.exit(1)
    inp, outp = sys.argv[1:3]
    output = open(outp, 'w')
    with open(inp, 'r') as corpus:
        for line in corpus:
            print line
            line = line.replace("\n", "")
            line = re.sub(r'((\d*[.,])?\d+)', '$NUM$', line)
            line = re.sub(r'\$NUM\$%','$PERCENT$', line )
            print line
            output.write(line + "\n")
    output.close()
