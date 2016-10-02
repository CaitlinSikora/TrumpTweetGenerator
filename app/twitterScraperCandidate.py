#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re, sys, pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from app import app

# Get private twitter user account data
username = app.config['TWITTER_ACCOUNT']['username']
password = app.config['TWITTER_ACCOUNT']['password']

# A function to get and save the desired tweet data
def tweet_info(tweet):
	time = tweet.find_element_by_class_name('tweet-timestamp').get_attribute('title')
	try: 
		text = tweet.find_element_by_class_name('tweet-text').text
	except:
		text = "no text"
	return {
		"text" : text,
		"timestamp" : time
	}

# Create a headless browsert and log in to Twitter
driver = webdriver.Chrome('/Applications/chromedriver')
driver.get('https://twitter.com/search?q=donald%20trump&src=typd')
user = driver.find_element_by_class_name('LoginForm-username').find_element_by_tag_name('input')
user.send_keys(username)
password = driver.find_element_by_class_name('LoginForm-password').find_element_by_tag_name('input')
password.send_keys(password)
submit = driver.find_element_by_class_name('submit')
submit.submit()

# These are the search parameters.
candidate=sys.argv[1]
urls = [['https://twitter.com/search?q=from%3A'+candidate+'%20since%3A','%20until%3A','%20include%3Aretweets&src=typd'],
['https://twitter.com/search?f=tweets&vertical=default&q=from%3A'+candidate+'%20since%3A','%20until%3A','%20include%3Aretweets&src=typd']]
dates = ['-01-01','-02-01','-03-01','-04-01','-05-01','-06-01','-07-01','-08-01','-09-01','-10-01','-11-01','-12-01','-12-31']
min_year = int(sys.argv[2])
max_year = int(sys.argv[3])

# Loop through the years:
for j in range(min_year,max_year+1):
	year = str(j)
	tweets = []
	# Loop through the months:
	for i,date in enumerate(dates[:len(dates)-1]):
		# Go through most popular and all tweets by the author (one url for each)
		for url in urls:
			start = dates[i]
			end = dates[i+1]
			run_url= url[0]+year+start+url[1]+year+end+url[2]
			driver.get(run_url)
			lastHeight = driver.execute_script("return document.body.scrollHeight")
			# Scroll down to the bottom to load all content.
			while True:
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(1)
				newHeight = driver.execute_script("return document.body.scrollHeight")
				if newHeight == lastHeight:
					driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					time.sleep(3)
					newHeight = driver.execute_script("return document.body.scrollHeight")
					# Fake out the browser by scrolling up and down a few times.
			        if newHeight == lastHeight:
			        	time.sleep(5)
				    	print "Scroll up"
			        	driver.execute_script("window.scrollTo(0, document.body.scrollHeight-2000);")
				    	time.sleep(1)
				    	print "back down"
				    	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				    	time.sleep(3)
				    	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				    	time.sleep(1)
				    	newHeight = driver.execute_script("return document.body.scrollHeight")
				    	if newHeight == lastHeight:
				    	# 	time.sleep(10)
				    	# 	print "Scroll up 2"
					    # 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight-2000);")
					    # 	time.sleep(5)
					    # 	print "back down 2"
					    # 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					    # 	time.sleep(3)
				    	# 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				    	# 	time.sleep(3)
					    # 	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					    # 	time.sleep(3)
					    # 	newHeight = driver.execute_script("return document.body.scrollHeight")
					    # 	if newHeight == lastHeight:
					    	break
				lastHeight = newHeight

			# Get all the tweets
			elems = driver.find_elements_by_class_name('tweet')
			combed_elems = []
			seen = set()

			# Comb the tweets to eliminate extra items
			for elem in elems:
				try:
					elem.find_element_by_class_name('username')
					combed_elems.append(elem)
				except:
					user = "withheld"
			# Get the data for each tweet and keep track in seen to avoid redundancies.
			for stream in combed_elems[:len(combed_elems)-2]:
				tweetdat = tweet_info(stream)
				if tweetdat["timestamp"] not in seen:
					seen.add(tweetdat["timestamp"])
					tweets.append(tweetdat)
			print len(tweets)

	# Write each year to its own file
	print year,len(tweets)
	out_name = 'static/'+year+candidate+'.p'
	pickle.dump(tweets, open(out_name, "wb" ))
	# with open(out_name, 'w') as outfile:
	#     json.dump(tweets, outfile)

