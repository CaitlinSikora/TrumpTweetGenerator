# -*- coding: utf-8 -*-

import json, datetime
import sys, pickle

# Tokenize the tweet
def tokenize_tweet(tweet):
	return tweet.split()

# Process a tweet to be added to the model
def process_tweet(tweet):
	stamp = tweet["timestamp"]
	text_list = tokenize_tweet(tweet["text"])
	text_list.insert(0,'BEGIN')
	text_list.insert(1,'HERE')
	text_list.append('END')
	text_list.append(stamp)
	return text_list

# Generate trigram from a list of words
def generate_trigram(words):
    if len(words) < 3:
        return
    for i in xrange(len(words) - 2):
        yield (words[i], words[i+1], words[i+2])

# Get the arguments needed for each candidate
candidate=sys.argv[1]
min_year = int(sys.argv[2])
max_year = int(sys.argv[3])

#Create the model:
model = {}
for i in range(min_year,max_year+1):
 	file_name = 'static/'+str(i)+candidate+'.p'
 	parsed = pickle.load(open(file_name, "rb"))
 	# with open(file_name,'r') as f:
 	# 	parsed = json.loads(f.read())

 	# Loop through all tweets in the year file
	for tweet in parsed:
		processed = process_tweet(tweet)
		stamp = processed[len(processed)-1]
		processed = processed[:-1]

		# Create and add each trigram to the model with timestamps
		for word1, word2, word3 in generate_trigram(processed):
			key = str((word1, word2))
			if key in model:
				model[key].append((word3, stamp))
			else:
				model[key] = [(word3, stamp)]

pickle.dump(model, open('static/'+candidate+'Model.p', "wb" ))
# json.dump(model, open('static/'+candidate+"Model.json", "wb"))