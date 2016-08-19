# -*- coding: utf-8 -*-
import requests
import re, sys, json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def tweet_info(tweet):
	try:
		idnum = tweet.get_attribute('data-tweet-id')
	except:
		idnum = "no id"
	time = tweet.find_element_by_class_name('tweet-timestamp').get_attribute('title')
	try: 
		text = tweet.find_element_by_class_name('tweet-text').text
	except:
		text = "no text"
	try: 
		link = tweet.find_element_by_class_name('twitter-timeline-link').get_attribute('title')
	except:
		link = ""
	if link == "" or link == None:
		try:
			link = tweet.find_element_by_class_name('twitter-timeline-link').text
		except:
			link =""
	if link == "" or link == None:
		try:
			link = tweet.find_element_by_class_name('twitter-timeline-link').get_attribute('data-expanded-url')
		except:
			link = ""
	if link == "" or link == None:
		try:
			link = tweet.find_element_by_class_name('twitter-timeline-link').get_attribute('href')
		except:
			link = "no link"
	try:
		quote = tweet.find_element_by_class_name('QuoteTweet-text').text
	except:
		quote = "N"
	try:
		author = tweet.find_element_by_class_name('QuoteTweet-screenname').text
	except:
		author = tweet.find_element_by_class_name('username').text
	if quote != "N":
		try:
			inside_html = tweet.find_element_by_class_name('QuoteTweet-text')
		except:
			inside_html = None
	try:
		link = inside_html.find_element_by_class_name('twitter-timeline-link').get_attribute('title')
	except:
		inside_html = None
	try:
		retweet = tweet.find_element_by_class_name('js-retweet-text').text
		retweeted = "Y"
	except:
		retweeted = "N"
	return {
		"idnum" : idnum,
		"text" : text,
		"link" : link,
		"timestamp" : time,
		"retweeted" : retweeted,
		"quote" : quote,
		"author" : author
	}

def print_tweet(tweet,i):
	print "Tweet #",i+1," reads:"
	print "ID: "+tweet.get("idnum")
	print "Text: "+tweet.get("text")
	print "Timestamp: "+tweet.get("timestamp")
	print "Retweeted: "+tweet.get("retweeted")
	print "Quote: "+tweet.get("quote")
	print "Author: "+tweet.get("author")
	print "Link: ",tweet.get("link")
	print "\n" 

out_name = 'static/HillaryClintonTest.json'
with open(out_name, 'w') as outfile:
	print "file works"

driver = webdriver.Chrome('/Applications/chromedriver')
driver.get('https://twitter.com/search?q=donald%20trump&src=typd')
user = driver.find_element_by_class_name('LoginForm-username').find_element_by_tag_name('input')
user.send_keys('caitlin.sikora@gmail.com')
password = driver.find_element_by_class_name('LoginForm-password').find_element_by_tag_name('input')
password.send_keys('AHollowDream1$')
submit = driver.find_element_by_class_name('submit')
submit.submit()

candidate=sys.argv[1]
#https://twitter.com/search?q=from%3AHillaryClinton%20since%3A2016-07-01%20until%3A2016-07-31%20include%3Aretweets&src=typd
urls = [['https://twitter.com/search?q=from%3A'+candidate+'%20since%3A','%20until%3A','%20include%3Aretweets&src=typd'],
['https://twitter.com/search?f=tweets&vertical=default&q=from%3A'+candidate+'%20since%3A','%20until%3A','%20include%3Aretweets&src=typd']]
dates = ['-01-01','-02-01','-03-01','-04-01','-05-01','-06-01','-07-01','-08-01','-09-01','-10-01','-11-01','-12-01','-12-31']

min_year = int(sys.argv[2])
max_year = int(sys.argv[3])
print max_year
print min_year

for j in range(min_year,max_year+1):
	year = str(j)
	tweets = []
	for i,date in enumerate(dates[:len(dates)-1]):
		seen = set()
		for url in urls:
			start = dates[i]
			end = dates[i+1]
			run_url= url[0]+year+start+url[1]+year+end+url[2]
			driver.get(run_url)
			lastHeight = driver.execute_script("return document.body.scrollHeight")
			while True:
				driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				time.sleep(1)
				newHeight = driver.execute_script("return document.body.scrollHeight")
				if newHeight == lastHeight:
					driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					time.sleep(3)
					newHeight = driver.execute_script("return document.body.scrollHeight")
			        if newHeight == lastHeight:
			        	time.sleep(10)
				    	print "Scroll up"
			        	driver.execute_script("window.scrollTo(0, document.body.scrollHeight-2000);")
				    	time.sleep(5)
				    	print "back down"
				    	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				    	time.sleep(3)
				    	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				    	time.sleep(3)
				    	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				    	time.sleep(3)
				    	newHeight = driver.execute_script("return document.body.scrollHeight")
				    	if newHeight == lastHeight:
				    		time.sleep(10)
				    		print "Scroll up 2"
					    	driver.execute_script("window.scrollTo(0, document.body.scrollHeight-2000);")
					    	time.sleep(5)
					    	print "back down 2"
					    	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					    	time.sleep(3)
				    		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				    		time.sleep(3)
					    	driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
					    	time.sleep(3)
					    	newHeight = driver.execute_script("return document.body.scrollHeight")
					    	if newHeight == lastHeight:
					    		break
				lastHeight = newHeight

				
			elems = driver.find_elements_by_class_name('tweet')
			combed_elems = []
			for elem in elems:
				try:
					elem.find_element_by_class_name('username')
					combed_elems.append(elem)
				except:
					user = "withheld"
			for stream in combed_elems[:len(combed_elems)-2]:
				tweetdat = tweet_info(stream)
				#print tweetdat["idnum"]
				if tweetdat["idnum"] not in seen:
					seen.add(tweetdat["idnum"])
					tweets.append(tweetdat)
			print len(tweets)

	print year,len(tweets)
	out_name = 'static/'+year+candidate+'.json'
	with open(out_name, 'w') as outfile:
	    json.dump(tweets, outfile)

