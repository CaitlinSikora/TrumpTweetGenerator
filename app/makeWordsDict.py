# -*- coding: utf-8 -*-
import json, datetime, sys, pickle
from nltk.tokenize import TweetTokenizer
import collections
import math
from operator import itemgetter

dict_words = {}
count_dates = collections.Counter()

candidate=sys.argv[1]
min_year = int(sys.argv[2])
max_year = int(sys.argv[3])

def tokenize_tweet(tweet):
	return TweetTokenizer().tokenize(tweet.lower())

def process_date(stamp):
    return datetime.datetime.strptime(stamp, '%d %b %Y').strftime("%Y%m")

for i in range(min_year,max_year+1):
 	file_name = 'static/'+str(i)+candidate+'.p'
 	parsed = pickle.load(open(file_name, "rb"))
 	# with open(file_name,'r') as f:
 	# 	data = f.read()
 	# parsed = json.loads(data)

	for tweet in parsed:
		time = tweet["timestamp"].split(' - ')
		date_ind = int(process_date(time[1]))
		text_list = tokenize_tweet(tweet["text"])
		for word in text_list:
			if word in dict_words:
				dict_words[word].append({'date_ind':date_ind,'time':tweet["timestamp"]})
			else:
				dict_words[word]=[{'date_ind':date_ind,'time':tweet["timestamp"]}]

pickle.dump(dict_words, open('static/'+candidate+'WordsDict.p', "wb" ))
# with open('static/'+candidate+'WordsDict.json', 'w') as outfile:
# 	outfile.write(json.dumps(dict_words))