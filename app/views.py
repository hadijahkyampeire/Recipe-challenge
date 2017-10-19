# The view function for this app

from flask import render_template
from app import app

@app.route('/')
def index():
    '''Responds with the index template'''
    return render_template('index.html')


@app.route('/index.html')
def index2():
    '''Also responds with the index template'''
    return render_template('index.html')


@app.route('/myrecipes.html')
def myrecipes():
    '''Responds with my recipes template'''
    return render_template('myrecipes.html')


@app.route('/Sign-in.html')
def sign_in():
    '''Responds with the login page'''
    return render_template('Sign-in.html')

@app.route('/Sign-up.html')
def sign_up():
    '''Returns with the sign up page'''
    return render_template('Sign-up.html')


@app.route('/Categories.html')
def categories():
    '''Returns the categories page'''
    return render_template('Categories.html')