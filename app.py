from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/myrecipes')
def myrecipes():
    return render_template('myrecipes.html')

@app.route('/login')
def login():
    return render_template('Sign-in.html')

@app.route('/Sign-up')
def Sign_up():
    return render_template('Sign-up.html')

@app.route('/Categories')
def categories():
    return render_template('Categories.html')


if __name__ == '__main__':
    app.run(debug=True)