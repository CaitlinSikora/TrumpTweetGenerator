# -*- coding: utf-8 -*-

from __future__ import division
import json, datetime, sys
import nltk
from nltk.tokenize import TweetTokenizer
import nltk.tag
import collections
import math, random
from operator import itemgetter
from image_grab import grab_wide, grab_widest

# A function to tokenize tweets
def tokenize_tweet(tweet):
	return TweetTokenizer().tokenize(tweet.lower())

# A function to get the counts of a word over all the candidates tweets
def find_word_data(key_word,candidate,dict_words):
	# Process the word
	key_word = key_word.lower().replace(":", "").replace(".", "").replace(",", "").replace("?", "").replace("!", "").replace('"', '')
	# Create the counter
	count_dates = collections.Counter()

	# Look for the word
	if key_word in dict_words:
		# Sort the date entries for the word
		word_entries = sorted(dict_words[key_word], key=itemgetter('date_ind'))
		# Count the number of instances for each date ind (representing weeks)
		count_dates.update([item['date_ind'] for item in word_entries])
		new_list=[]
		# Go through all of the weeks and add the count for the word for each week
		for j in range(1,13):
			for i in range(2009,2017):
				date = j+(100*i)
				if date in count_dates:
					new_list.append({'x':date,'y':count_dates[date]})
				else:
					new_list.append({'x':date,'y':0})
		new_list = sorted(new_list, key=itemgetter('x'))
		# Return the total count and the list for the plot
		return len(dict_words[key_word]), new_list
	else:
		return

# Find the Google Image search terms from each tweet
def find_unique_words(tweet,candidate,dict_words):
	toktweet = tokenize_tweet(tweet)
	pos_tagged = nltk.pos_tag(tweet.split())
	#print pos_tagged

	chunked_nes = nltk.ne_chunk(pos_tagged) 
	nes = [' '.join(map(lambda x: x[0], ne.leaves())) for ne in chunked_nes if isinstance(ne, nltk.tree.Tree)]
	#print nes
	
	propernouns = [tokenize_tweet(word.lower())[0] for word,pos in pos_tagged if pos == 'NNP']
	#print propernouns
	
	count_occur = collections.Counter()
	count_occur.update(toktweet)
	unique = {}
	for entity in nes:
		if len(entity.split())>1:
			unique[entity]= 3
	for word in toktweet:
		if word in propernouns:
			PPN = 0.9
		else:
			PPN = 0
		if "@" in word:
			PPN += 1
		if word in nes:
			PPN += 0.9
		if "http" not in word:
			unique[word]= PPN + count_occur[word]/len(dict_words[word])
	sorted_unique = [word for word in sorted(unique.iteritems(), key=itemgetter(1), reverse=True) if len(word[0])>3]
	sorted_unique = sorted_unique[:3]
	final_list = []
	megaword = []
	for item in sorted_unique:
		if '@' not in item[0]:
			megaword.append(item[0])
		else:
			final_list.append(item)
	if len(megaword)>1:
		final_list.insert(0,[' '.join(megaword),3])
	print final_list
	return [item[0] for i,item in enumerate(final_list) if i<2 or item[1]>1]

# Get links for the images in the background
def grab_links(key_words, candidate):
	back_up_links = {'HillaryClinton':['static/clinton4.jpg',
										'static/clinton.jpg',
										'static/clinton3.jpg',
										'static/clinton5.jpg',
										'static/clinton2.jpg'],
					'Trump':['static/trump.jpg',
							'static/trump2.jpg',
							'static/trump3.jpg',
							'static/trump4.jpg',
							'static/trump5.jpg']}

	# Call grab_wide, which calls the function to do the search and selects the widest of the links
	links = []
	for key_word in key_words:
		new_link = grab_wide(key_word)
		if new_link:
			links.append(new_link)
	# If no links were found, choose a random backup image
	if len(links)==0:
		index = random.randint(0,4)
		links.append(back_up_links[candidate][index])
	return links
