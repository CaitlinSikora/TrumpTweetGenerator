#!/usr/bin/env python
from __future__ import division
import datetime as dt
import json, sys
from googleapiclient.discovery import build
from random import randint
from app import app

# Get the private google API data from config file.
search_engine_id = app.config['GOOGLE_KEYS']['search_engine_id']
apis = app.config['GOOGLE_KEYS']['apis']

# Search for the key terms
def google_search(key_term, api, search_engine_id):
    search_term = key_term
    num_requests = 1
    search_engine_id = search_engine_id
    api_key = api
    service = build('customsearch', 'v1', developerKey=api_key)
    collection = service.cse()

    try:
        request = collection.list(q=search_term,
            num=10, 
            start=1,
            cx=search_engine_id,
            searchType='image',
            imgSize='xxlarge',
            imgType='photo'
        )
        response = request.execute()
        if response:
            return response
    except:
        return None

# Try API keys
def try_keys(key_word,apis):
    apis = apis
    print "Searched", key_word
    google = None
    for i,key in enumerate(apis):
        if not google:
            print "key", i
            google = google_search(key_word, apis[i], search_engine_id)
    return google

# Grab the widest image
def grab_widest(results):
    parsed = results
    max_aspect_ratio = 0
    for item in parsed['items']:
        if (item['image']['width']/item['image']['height'])>max_aspect_ratio:
          max_aspect_ratio = item['image']['width']/item['image']['height']
          max_link = item['link']
    return max_link

def grab_wide(key_word):
    results = try_keys(key_word,apis)
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

