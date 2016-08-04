import json, datetime, sys
from nltk.tokenize import TweetTokenizer
import collections
import math
from operator import itemgetter
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

dict_words = {}
count_dates = collections.Counter()
#key_word = sys.argv[1]
sid = SentimentIntensityAnalyzer()

candidate=sys.argv[1]
min_year = int(sys.argv[2])
max_year = int(sys.argv[3])

def tokenize_tweet(tweet):
	return TweetTokenizer().tokenize(tweet.lower())

def process_date(stamp):
    return datetime.datetime.strptime(stamp, '%d %b %Y').strftime("%Y%m")

for i in range(min_year,max_year+1):
 	file_name = 'static/'+str(i)+candidate+'.json'
 	with open(file_name,'r') as f:
 		data = f.read()
 	parsed = json.loads(data)

	for tweet in parsed:
		time = tweet["timestamp"].split(' - ')
		# this_date = datetime.datetime.strptime(time[1], '%d %b %Y')
		# date_ind = (this_date[0]-2009)*53+this_date[1]
		date_ind = int(process_date(time[1]))
		text_list = tokenize_tweet(tweet["text"])
		at = [text for text in text_list if text.startswith("@") and len(text)>1]
		ss = sid.polarity_scores(tweet["text"])
		sent = ss["compound"]
		for word in text_list:
			if word in dict_words:
				dict_words[word].append({'date_ind':date_ind,'time':tweet["timestamp"],'sent':sent})
			else:
				dict_words[word]=[{'date_ind':date_ind,'time':tweet["timestamp"],'sent':sent}]

with open('static/'+candidate+'WordsDict.json', 'w') as outfile:
	outfile.write(json.dumps(dict_words))

'''print key_word, " dict: ", len(dict_words[key_word])

count_dates.update(dict_words[key_word])

weeks = count_dates.keys()
instances = [count_dates[week] for week in weeks]

plt.bar(weeks, instances)
plt.ylabel("instances")
plt.title(str(key_word)+" tweets")
plt.show()'''