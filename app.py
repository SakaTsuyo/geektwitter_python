import os
from flask import Flask, render_template, request, redirect, session
import numpy as np
import sqlite3 as sqlite
import pandas as pd
import datetime
import db.tweet as tweet


app = Flask(__name__)

@app.route('/')
def index():
    tweets = tweet.get_tweets()
    return render_template("index.html", tweets=tweets)

@app.route('/new', methods=['GET','POST'])
def new():
    if request.method == 'GET':
        return render_template('new.html')
    elif request.method == 'POST':
        tweet_content = request.form.get('tweet')
        tweet.add_tweet(tweet_content)
        return redirect('/')

@app.route('/edit')
def edit():
    return render_template('edit.html')

if __name__ == "__main__":
    tweet.create_tweet_table()
    app.run(debug=True)