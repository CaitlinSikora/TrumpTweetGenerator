# -*- coding: utf-8 -*-
import pickle, random
import json
from operator import itemgetter
import datetime
from trumpWords import find_unique_words, grab_links, tokenize_tweet, find_word_data
import app, time

def print_stamps(stamps,candidate,year_dict,dict_words):
	word_dict = {}
	orig_dict = {}
	stamp_dict= {}
	for stamp in stamps:
		year = stamp[-4:]
		time = stamp.split(' - ')[0]
		date = stamp.split(' - ')[1]
		orig_date = ' '.join([date.split()[1]+'.',date.split()[0]+',',date.split()[2]])
		# file_name = 'app/static/'+year+candidate+'.json'
		# with open(file_name,'r') as f:
		# 	data = f.read()
		parsed = year_dict[year]
		tweet = next((item for item in parsed if item['timestamp'] == stamp), None)
		original_text = tweet['text']
		if stamp not in stamp_dict:
			important_words = find_unique_words(original_text,candidate,dict_words)
			images = grab_links(important_words, candidate)
			stamp_dict[stamp]=important_words,images
			print "found images for: ", important_words
			#print stamp[0]
		else:
			images = stamp_dict[stamp[1]]
		orig_dict[stamp.replace(' ','').replace(':','').replace('-','')]={
			'sort_date': datetime.datetime.strptime(date, '%d %b %Y').isoformat(),
			'orig_time': time,
			'orig_date': orig_date,
			'orig_text': original_text,
			'imp_words': important_words,
			'imgs':images,
			'words_used': stamps[stamp]}
		for word in stamps[stamp]:
			word_dict[word]=stamp.replace(' ','').replace(':','').replace('-','')
	return orig_dict, word_dict

def generate_tweet(candidate,min_year,max_year):
	t0 = time.time()
	print time.time() - t0
	model = app.models[candidate]
	print "model gotten"
	new_tweet = []
	stamps = {}

	word1 = "BEGIN"
	word2 = "HERE"
	prev_key = []
	open_quotes = 0
	close_quotes = 0

	while True:
		print time.time() - t0
		# Select the next word in the generated tweet.
		next_word = random.choice(model[str((word1,word2))])
		print next_word
		# Update the bigram 
		word1, word2  = word2, next_word[0]

		#handle_punctuation_end(new_word,word1,prev_key,next_word,open_quotes,close_quotes,new_tweet,stamps)
		new_word = next_word[0].replace(u"“", "\"")
		new_word = new_word.replace(u"”", "\"")
		new_word = new_word.replace("(","")
		new_word = new_word.replace(")","")
		for i,_ in enumerate(new_word):
			if _ == '\"':
				if i == 0 and len(new_word)>1:
					open_quotes += 1
					#print _, new_word, "open"
					#print open_quotes
				else:
					close_quotes += 1
					#print _, new_word, "close"
					#print close_quotes
		if new_word == "END":
			if "\"" in word1 and open_quotes>close_quotes:
				new_tweet[-1]=new_tweet[-1]+"\""
				#print "added close"
				for entry in stamps[prev_key[-1]]:
					#print entry
					if entry == word1:
						stamps[prev_key[-1]].remove(entry)
						#print entry, "entry"
						entry = new_tweet[-1]
						stamps[prev_key[-1]].append(entry)
						#print entry, "added close"
				close_quotes += 1
				#print close_quotes
				#print stamps[prev_key[-1]]
			elif "\"" in word1 and open_quotes<close_quotes:
				if close_quotes - open_quotes > 1:
					#print "added open"
					for entry in stamps[prev_key[0]]:
						#print entry
						if entry == new_tweet[0]:
							stamps[prev_key[0]].remove(entry)
							#print entry, "entry"
							entry = "\""+new_tweet[0]
							#print entry, "added open"
							stamps[prev_key[0]].append(entry)
							new_tweet[0] = entry
					open_quotes += 1
					#print open_quotes
					#print stamps[prev_key[0]]
				if close_quotes - open_quotes == 1:
					new_tweet[-1]=new_tweet[-1][:-1]
					#print "removed close"
					for entry in stamps[prev_key[-1]]:
						#print entry
						if entry == word1:
							stamps[prev_key[-1]].remove(entry)
							#print entry, "entry"
							entry = new_tweet[-1]
							#print entry, "removed close"
							stamps[prev_key[-1]].append(entry)
					close_quotes -= 1
					#print close_quotes
					#print stamps[prev_key[-1]]
			elif open_quotes>close_quotes:
				if open_quotes-close_quotes>1 and "\"" in new_tweet[0]:
					#print "remove open"
					for entry in stamps[prev_key[0]]:
						#print entry
						if entry == new_tweet[0]:
							stamps[prev_key[-1]].remove(entry)
							#print entry, "entry"
							entry = new_tweet[0][1:]
							#print entry, "removed open"
							stamps[prev_key[-1]].append(entry)
							new_tweet[0]=entry
					open_quotes -= 1
					##print close_quotes
					##print stamps[prev_key[-1]]
				if open_quotes-close_quotes==1:
					new_tweet[-1]=new_tweet[-1]+"\""
					#print "added close"
					for entry in stamps[prev_key[-1]]:
						#print entry
						if entry == word1:
							stamps[prev_key[-1]].remove(entry)
							#print entry, "entry"
							entry = new_tweet[-1]
							#print entry, "added close"
							stamps[prev_key[-1]].append(entry)
					close_quotes += 1
					##print close_quotes
					##print stamps[prev_key[-1]]
			elif open_quotes<close_quotes:
				if close_quotes - open_quotes > 1:
					new_tweet[-1]=new_tweet[-1][:-1]
					##print "removed close"
					for entry in stamps[prev_key[-1]]:
						##print entry
						if entry == word1:
							stamps[prev_key[-1]].remove(entry)
							##print entry, "entry"
							entry = new_tweet[-1]
							##print entry, "removed close"
							stamps[prev_key[-1]].append(entry)
					close_quotes -= 1
					##print stamps[prev_key[-1]]
					##print close_quotes
				if close_quotes - open_quotes == 1:
					##print "added open"
					for entry in stamps[prev_key[0]]:
						##print entry
						if entry == new_tweet[0]:
							stamps[prev_key[0]].remove(entry)
							##print entry, "entry"
							entry = "\""+new_tweet[0]
							##print entry, "added open"
							new_tweet[0] = entry
							stamps[prev_key[0]].append(entry)
					##print stamps[prev_key[0]]
					open_quotes += 1
					##print open_quotes
			break

		# If we are not at the end of the tweet, add the new_word to stamps.
		else:
			if next_word[1] in stamps:
				stamps[next_word[1]].append(new_word)
			else:
				stamps[next_word[1]]=[new_word]
		# Add the new_word to the new_tweet.
		new_tweet.append(new_word)
		# Add the current key to prev_key.
		prev_key.append(next_word[1])


	the_tweet = []

	references = print_stamps(stamps,candidate,app.year_dict[candidate],app.dict_words[candidate])
	print "stamps time " + str(time.time() - t0)
	for word in new_tweet:
		the_tweet.append((word,references[1][word]))
	word_data = {}
	for word in new_tweet:
		print "original word", word
		this_word = word.lower().replace(":", "").replace(".", "").replace(",", "").replace("?", "").replace("!", "").replace('"', '')
		print "searching data on this word", this_word
		word_data[this_word]=find_word_data(this_word,candidate,app.dict_words[candidate])
	print time.time() - t0
	return the_tweet, references[0], len(references[0]), word_data


#new_tweet = generate_tweet(pickle.load(open('app/static/trumpAllModel.p')))
##print new_tweet[0]
