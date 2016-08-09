#!/usr/bin/env python
from __future__ import division
import datetime as dt
import json, sys
from apiclient.discovery import build
from random import randint
#import BeautifulSoup
#import urllib2

def grab_images_google(key_word, api):
    # Create an output file name in the format "srch_res_yyyyMMdd_hhmmss.json"
    now_sfx = dt.datetime.now().strftime('%Y%m%d_%H%M%S')
    search_term = key_word
    num_requests = 1

    # Key codes we created earlier for the Google CustomSearch API
    search_engine_id = '015037131198447628591:7g7ithuxakq'
    api_key = api

    # The build function creates a service object. It takes an API name and API 
    # version as arguments. 
    service = build('customsearch', 'v1', developerKey=api_key)
    # A collection is a set of resources. We know this one is called "cse"
    # because the CustomSearch API page tells us cse "Returns the cse Resource".
    collection = service.cse()

    try:
    # Make an HTTP request object
        request = collection.list(q=search_term,
            num=10, #this is the maximum & default anyway
            start=1,
            cx=search_engine_id,
            searchType='image',
            imgSize='xxlarge',
            imgType='photo'
        )
        response = request.execute()
        if response:
            #output = json.dumps(response, sort_keys=True, indent=2)
            return response
    except:
        return None

def grab_images(key_word):
    apis = ['AIzaSyBTg-ed_rVXHl4khSn8EXB3wC-F6-IP6tM','AIzaSyBy8oibtBr1kJu4UEL6uVOXkh-IHS9AHzs','AIzaSyAFjKNFRy13MnMvYUYA36kzTfPdGTrPEEk']
    print "Searched", key_word
    print "key 0"
    google = grab_images_google(key_word,apis[0])
    if not google:
        print "key 1"
        google = grab_images_google(key_word,apis[1])
        if not google:
            print "key 2"
            google = grab_images_google(key_word,apis[2])
    return google

def grab_widest(results):
    parsed = results
    max_aspect_ratio = 0
    for item in parsed['items']:
        if (item['image']['width']/item['image']['height'])>max_aspect_ratio:
          max_aspect_ratio = item['image']['width']/item['image']['height']
          max_link = item['link']
    return max_link

def grab_wide(results):
    if results == None:
        return None
    parsed = results
    tester = results['queries']['request']
    # print tester
    if tester[0]['totalResults']!='0'and tester[0]['totalResults']>0:
        links = []
        for item in parsed['items']:
            if (item['image']['width']/item['image']['height'])>1.5:
              links.append(item['link'])
        if len(links)==0:
            return grab_widest(results)
        else:
            ind = randint(0,len(links)-1)
            return links[ind]
    else:
        return None

#api-key: AIzaSyBTg-ed_rVXHl4khSn8EXB3wC-F6-IP6tM or AIzaSyBy8oibtBr1kJu4UEL6uVOXkh-IHS9AHzs or AIzaSyAFjKNFRy13MnMvYUYA36kzTfPdGTrPEEk
#search-engine-id: 015037131198447628591:7g7ithuxakq
#GET https://www.googleapis.com/customsearch/v1?q={search_word}&cref=https%3A%2F%2Fcse.google.com%3A443%2Fcse%2Fpublicurl%3Fcx%3D015037131198447628591%3A7g7ithuxakq&cx=015037131198447628591%3A7g7ithuxakq&imgSize=xlarge&safe=off&searchType=image&key={MY_API_KEY}

