# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 09:49:03 2016

@author: aitor
"""

from datetime import datetime
import requests
import string
import sys
import time

from bs4 import BeautifulSoup

BASE_URL = "https://www.boe.es/diario_boe/txt.php?id=BOE-A-"
ERROR = u'<p>Error: No se encontró el documento original.</p>' #that document does not exists
MAX_DOCUMENTS = 60000 # max docments each year
MINIMUN_LENGTH = 30 # we do not process paragraphs with less than this chars    
years = range(1981, 2017)
classes = ['parrafo', 'parrafo_2']
punctuation = set(string.punctuation) 
punctuation.add(u'–')


print 'Starting web scrapping...'
i = 0
for year in years:
    output_file = "boe_%s.text" % (year)
    output = open(output_file, 'w')
    print '%s - Processing year %s' % (datetime.now().ctime(), year)
    sys.stdout.flush()
    for index in range(1, MAX_DOCUMENTS):        
        url = "%s%s-%s" % (BASE_URL, year, index)        
        retries = 0
        status_code = 0   
        while status_code != 200:
            try:
                r = requests.get(url)
                status_code = r.status_code
            except:
                print '%s - retry: %s' % (datetime.now().ctime(), retries)
                sys.stdout.flush()
                status_code = -11111
            if status_code != 200:
                 print '%s - Error %s, retry %s, waiting 3 min' % (datetime.now().ctime(), status_code, retries)
                 sys.stdout.flush()
                 time.sleep(3 * 60)
            retries +=1
            if retries > 5:
                break
        if retries > 5:
            continue            
        web = r.text
        i += 1
        if ERROR in web:
            print '%s - No more documents in %s' % (datetime.now().ctime(), year)
            sys.stdout.flush()
            break
        soup = BeautifulSoup(web, "html.parser")   
        for paragraph in soup.findAll('p'):
            try:
                clazz = paragraph['class'][0]
                if clazz in classes:
                    text = paragraph.text.strip().lower()
                    if len(text) > MINIMUN_LENGTH:
                        processed_text = ''.join(ch for ch in text if ch not in punctuation)
                        output.write(processed_text + "\n") 
            except:
                pass
        if i % 5000 == 0:
            print '%s - %s documents saved' % (datetime.now().ctime(), i)
            sys.stdout.flush()
            output.flush()
            time.sleep(1 * 60)
    print '%s - waiting 3 min between years' % (datetime.now().ctime())
    sys.stdout.flush()
    output.close()
    time.sleep(3 * 60)
print 'done'

