from flask import render_template, flash, redirect
from app import app
from generateTrumpTweet import generate_tweet, print_stamps
from trumpWords import find_word_data
import random
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Presidential Tweet Machine',
                           slogan="Our most important decision, with the help of Twitter")

@app.route('/vis')
def vis():
    return render_template('datavis.html',
                           title='Presidential Tweet Machine',
                           slogan="Our most important decision, with the help of Twitter")

@app.route('/trump', methods=['GET', 'POST'])
def trump():
    candidate = 'Trump'
    new_tweet = generate_tweet(candidate,2009,2016)
    return render_template('tweet.html',
                           title='Trump Tweet Machine',
                           slogan='Making America great again, one tweet at a time',
                           candidate='Trump',
                           tweet=new_tweet[0], 
                           references=new_tweet[1],
                           num_ref = new_tweet[2],
                           counts= new_tweet[3],
                           back_img = ['static/trump.jpg','static/trump2.jpg','static/trump3.jpg','static/trump4.jpg','static/trump5.jpg'])

@app.route('/clinton', methods=['GET', 'POST'])
def clinton():
    candidate = 'HillaryClinton'
    new_tweet = generate_tweet(candidate,2013,2016)
    return render_template('tweet.html',
                           title='Clinton Tweet Machine',
                           candidate='Clinton',
                           slogan="I'm with her... on Twitter, and also we're stronger together",
                           tweet=new_tweet[0], 
                           references=new_tweet[1],
                           num_ref = new_tweet[2],
                           counts= new_tweet[3],
                           back_img = ['static/clinton4.jpg','static/clinton.jpg','static/clinton3.jpg','static/clinton5.jpg','static/clinton2.jpg'])
