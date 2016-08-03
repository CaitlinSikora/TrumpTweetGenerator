
from __future__ import division
import json, datetime, sys
import nltk
from nltk.tokenize import TweetTokenizer
import nltk.tag
import collections
import math
from operator import itemgetter
from image_grab import grab_wide, grab_widest, grab_images

def tokenize_tweet(tweet):
	return TweetTokenizer().tokenize(tweet.lower())

def get_entities():
    qry = "It's Tuesday. How many terrible predictions and advice will Karl 1.6% Rove make today?"
    tokens = nltk.tokenize.word_tokenize(qry)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    #print sentt
    person = []
    for subtree in sentt.subtrees(filter=lambda t: t.node == 'PERSON'):
        for leave in subtree.leaves():
            person.append(leave)
    #print "person=", person

def find_word_data(key_word):
	key_word = tokenize_tweet(key_word)[0]
	print "This is YOUR KEY WORD:"
	print key_word
	file_name = 'app/static/'+'TrumpWordsDict.json'
	with open(file_name,'r') as f:
		data = f.read()
	dict_words = json.loads(data)
	count_dates = collections.Counter()
	word_entries = sorted(dict_words[key_word], key=itemgetter('date_ind'))
	count_dates.update([item['date_ind'] for item in word_entries])
	new_list=[]
	for j in range(1,13):
		for i in range(2009,2017):
			date = j+(100*i)
			if date in count_dates:
				new_list.append({'x':date,'y':count_dates[date],'date':'a_Date'})
			elif date in [200901, 200902, 200903,200904, 201608, 201609, 201610, 201611, 201612]:
				print "exception"
			else:
				new_list.append({'x':date,'y':0,'date':'a_Date'})
	new_list = sorted(new_list, key=itemgetter('x'))
	return len(dict_words[key_word]), new_list

def find_unique_words(tweet):
	toktweet = tokenize_tweet(tweet)
	pos_tagged = nltk.pos_tag(tweet.split())
	#print pos_tagged

	chunked_nes = nltk.ne_chunk(pos_tagged) 
	nes = [' '.join(map(lambda x: x[0], ne.leaves())) for ne in chunked_nes if isinstance(ne, nltk.tree.Tree)]
	#print nes
	
	propernouns = [tokenize_tweet(word.lower())[0] for word,pos in pos_tagged if pos == 'NNP']
	#print propernouns
	
	file_name = 'app/static/'+'TrumpWordsDict.json'
	with open(file_name,'r') as f:
		data = f.read()
	dict_words = json.loads(data)
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

def grab_links(key_words):
	links = []
	for key_word in key_words:
		new_link = grab_wide(grab_images(key_word))
		if new_link:
			links.append(new_link)
	return links

#the_tweet = "It's Tuesday. How many more 'The View' Execs will leak that they want @rosie gone? Show is failing."
#print grab_links(find_unique_words(the_tweet))


'''weeks = count_dates.keys()
instances = [count_dates[week] for week in weeks]'''
