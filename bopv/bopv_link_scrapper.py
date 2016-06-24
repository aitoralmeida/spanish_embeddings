# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 14:51:35 2016

This script recovers the links to all the documents in the bopv

@author: aitor
"""

from datetime import datetime
import requests
import sys
import time

from bs4 import BeautifulSoup

BASE_URL = "https://www.euskadi.eus/y22-bopv/es/p43aBOPVWebWar/VerParalelo.do?cs"
MAX_DOCUMENTS = 1000000 # max docments each year
EXPECTED_LENGTH = len('000001')
years = range(1978, 2017)
classes = [u'bopvBloquedcha']

print 'Starting web scrapping...'
i = 0
output_file = "bopv_links.text"
output = open(output_file, 'w')
for year in years:    
    current_summary = 0
    last_summary = 0
    
    print '%s - Processing year %s' % (datetime.now().ctime(), year)
    sys.stdout.flush()
    
    for index in range(1, MAX_DOCUMENTS):
        print '%s - %s' % (datetime.now().ctime(), i)
        sys.stdout.flush()
        #build URL, adding 0-s to the current document until EXPECTED_LENGHT
        current_document = (EXPECTED_LENGTH - len(str(i))) * '0' + str(i)  
#        url = "%s%s%s" % (BASE_URL, year, current_document)
        url = 'https://www.euskadi.eus/y22-bopv/es/p43aBOPVWebWar/VerParalelo.do?cs1978000001'
        # recover web
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
        soup = BeautifulSoup(web, "html.parser")  
        #find current summary
        for h2 in soup.find_all('h2'):            
            try:
                if h2['class'][0] == 'tituGeneral':
                    h2_text = h2.text
                    if not 'Sumario ' in h2_text:
                        continue
                    current_summary = h2_text.split(u'º')[1].strip()
                    current_summary = current_summary.split(u',')[0]
                    break
            except:
                pass
            
        print '%s - Last summary: %s, current summary: %s' % (datetime.now().ctime(), last_summary, current_summary)
        sys.stdout.flush()
        if current_summary <= last_summary: 
            print '%s - No more documents in %s' % (datetime.now().ctime(), year)
            sys.stdout.flush()
            last_summary = current_summary
            break       
        
        for div in soup.findAll('div'):            
            try:
                clazz = div['class'][0]
                if clazz in classes:
                    link = div.find('a').get('href') 
                    if not 'pdf' in link:                        
                        output.write(link + "\n") 
            except:
                pass
        
        if i % 1000 == 0:
            print '%s - %s documents saved' % (datetime.now().ctime(), i)
            sys.stdout.flush()
            output.flush()             
    print '%s - waiting 1 min between years' % (datetime.now().ctime())
    sys.stdout.flush()
    output.close()
    time.sleep(1 * 60)
    
print 'Fin'
            