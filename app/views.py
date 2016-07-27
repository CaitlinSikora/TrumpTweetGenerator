from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
from .forms import Trumpinator
from generateTrumpTweet import generate_tweet, print_stamps
import pickle, random
import json

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}
    posts = [
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           list_posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@app.route('/tweet', methods=['GET', 'POST'])
def tweeter():
    new_tweet = generate_tweet(pickle.load(open('app/static/trumpAllModel.p')))
    return render_template('tweet.html',
                           title='Trump Tweet Generator',
                           tweet=new_tweet[0], 
                           references=new_tweet[1],
                           num_ref = new_tweet[2],
                           back_img = ['https://static1.squarespace.com/static/55fa115ee4b01a082ee73da3/t/56b8f028c6fc088f59af8713/1454960683612/solar-panels.jpg','http://departed.co/wp-content/uploads/2016/03/Barack-Obama.jpg','http://static2.politico.com/dims4/default/56c2277/2147483647/resize/1160x%3E/quality/90/?url=http%3A%2F%2Fs3-origin-images.politico.com%2F2015%2F07%2F24%2F150723_trump_ap3_1160.jpg'])

@app.route('/trump', methods=['GET', 'POST'])
def trumper():
    form = Trumpinator()
    if form.validate_on_submit():
        flash('Trump mood requested="%s"' %
              (form.mood.data))
        return redirect('/index')
    return render_template('trumper.html',
                           title='MOOD',
                           form=form)