# -*- coding: utf-8 -*-

import json, datetime
from nltk.tokenize import TweetTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import collections
import math
from operator import itemgetter
import sys

sid = SentimentIntensityAnalyzer()

def tokenize_tweet(tweet):
	#return TweetTokenizer().tokenize(tweet.lower())
	return tweet.split()

def process_tweet(tweet):
	ss = sid.polarity_scores(tweet["text"])
	stamp = tweet["timestamp"]
	text_list = tokenize_tweet(tweet["text"])
	text_list.insert(0,'BEGIN')
	text_list.insert(1,'HERE')
	text_list.append('END')
	text_list.append(stamp)
	text_list.append(math.floor(ss["compound"]*10)/10)
	return text_list

def generate_trigram(words):
    if len(words) < 3:
        return
    for i in xrange(len(words) - 2):
        yield (words[i], words[i+1], words[i+2])

candidate=sys.argv[1]
min_year = int(sys.argv[2])
max_year = int(sys.argv[3])
print max_year
print min_year
model = {}

for i in range(min_year,max_year+1):
 	file_name = 'static/'+str(i)+candidate+'.json'
 	with open(file_name,'r') as f:
 		data = f.read()
 	parsed = json.loads(data)

	for tweet in parsed:
		processed = process_tweet(tweet)
		sent = processed[len(processed)-1]
		stamp = processed[len(processed)-2]
		processed = processed[:-2]


		for word1, word2, word3 in generate_trigram(processed):
			key = str((word1, word2))
			if key in model:
				model[key].append((word3, stamp, sent))
			else:
				model[key] = [(word3, stamp, sent)]

json.dump(model, open('static/'+candidate+"Model.json", "wb"))