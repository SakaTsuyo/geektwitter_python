import sqlite3 as sqlite
import pandas as pd

def create_tweet_table():
    conn = sqlite.connect('tweets.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS tweets(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, tweet TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    conn.commit()
    

def add_tweet(tweet_text):
    conn = sqlite.connect('tweets.db')
    c = conn.cursor()
    
    c.execute('INSERT INTO tweets(name, tweet) VALUES (?, ?)', ('User', tweet_text))
    conn.commit()

def get_tweets():
    conn = sqlite.connect('tweets.db')
    c = conn.cursor()
    
    c.execute('SELECT * FROM tweets')
    return c.fetchall()