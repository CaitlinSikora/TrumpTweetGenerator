from flask import Flask

app = Flask(__name__)
app.config.from_object('config')

from app import views


import sys, time
from sys import getsizeof
import multiprocessing
import gc, pickle

def open_year_files(candidate, min_year, max_year):
	year_dict = {}
	for i in range(min_year,max_year+1):
	 	file_name = 'app/static/'+str(i)+candidate+'.p'
	 	year_dict[str(i)] = pickle.load(open(file_name, "rb"))
	return year_dict

models = {}
models['realDonaldTrump'] = pickle.load(open('app/static/realDonaldTrumpModel.p', "rb"))
models['HillaryClinton'] = pickle.load(open('app/static/HillaryClintonModel.p', "rb"))
dict_words = {}
dict_words['realDonaldTrump'] = pickle.load(open('app/static/realDonaldTrumpWordsDict.p', "rb"))
dict_words['HillaryClinton'] = pickle.load(open('app/static/HillaryClintonWordsDict.p', "rb"))
year_dict={}
year_dict['realDonaldTrump']= open_year_files('realDonaldTrump', 2009, 2016)
year_dict['HillaryClinton']= open_year_files('HillaryClinton', 2013, 2016)

