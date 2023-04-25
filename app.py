from flask import Flask, render_template, request, redirect, session,flash,abort
import numpy as np
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, or_
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(25))
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    body = db.Column(db.String(140), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
@app.route('/', methods=["GET"])
def index():
    text_input = request.args.get('search')
    text_input = request.args.get('search')
    if text_input is None or len(text_input) == 0:
        posts = Tweet.query.all()
    else:
        posts = db.session.query(Tweet).filter(or_(Tweet.body.like(text_input), Tweet.title.like(text_input))).all()
    users = User.query.all()
    return render_template("index.html", posts = posts,users=users)

@app.route('/new', methods=['GET','POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')
        user_id = current_user.id
        post = Tweet(title=title,body=body,user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('new.html')

@app.route('/<int:id>/edit',methods=['GET','POST'])
@login_required
def edit(id):
    post = Tweet.query.get(id)
    if post.user_id != current_user.id:
        abort(403)
    if request.method == 'GET':
        return render_template('edit.html', post=post)
    else:
        title = request.form.get('title')
        body = request.form.get('body')
        post.title = title
        post.body = body
        db.session.add(post)
        db.session.commit()
        return redirect('/')

@app.route('/<int:id>/delete', methods=['GET'])
@login_required
def delete(id):
    post = Tweet.query.get(id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            flash('ユーザー名とパスワードを入力してください。')
            return redirect('/signup')
        elif len(username) < 4 or len(password) < 8:
            flash('ユーザー名は4文字以上、パスワードは8文字以上である必要があります。')
            return redirect('/signup')
        elif User.query.filter_by(username=username).first():
            flash('ユーザー名が既に使用されています。')
            return redirect('/signup')
        else:
            user = User(username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(user)
            db.session.commit()
            flash('ユーザー登録が完了しました。')
            return redirect('/login')
    else:
        return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/')
        else:
            flash('ユーザー名またはパスワードが間違っています。')
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

if __name__ == "__main__":
    app.run(debug=True)