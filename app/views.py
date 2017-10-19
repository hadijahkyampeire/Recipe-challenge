# The view function for this app
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template

from app import app


#User attributes
class User:
    '''Creates and instantiates the user class with attributes
    email: user email
    password: user password after registeration'''

    def __init__(self, email, password):
        'Instatiates the user attributes'
        self.email = email
        self.password = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)
        self.profile = {self.email:self.password}

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

