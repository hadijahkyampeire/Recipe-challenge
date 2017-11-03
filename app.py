from flask import Flask, render_template, request, session, flash, url_for, redirect
from wtforms import Form, StringField, PasswordField, TextAreaField, validators
from werkzeug.security import check_password_hash
from data import User, userdata, recipes, Recipe
from functools import wraps

app = Flask(__name__)


def login_required(f):
    """Creates a decorator @login required that wraps around any function
    and adds a layer of protection against unauthorized users"""
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized to view this page. Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def index():
    """routes to the index page"""
    return render_template('index.html')


@app.route('/myrecipes')
@login_required
def myrecipes():
    """routes to the recipes page for authorized users"""
    try:
        email = session['email']
    except KeyError:
        return redirect(url_for('sign_up'))
    if recipes:
        try:
            return render_template('myrecipes.html', recipes_list=recipes[email], email=email)
        except KeyError:
            msg = 'Create your first recipe'
            return render_template('myrecipes.html', msg=msg)
    else:
        msg = 'Create your first recipe'
        return render_template('myrecipes.html', msg=msg)


@app.route('/Categories', methods=['GET', 'POST'])
@login_required
def categories():
    """routes to the categories page
    handles post request from user and adds them to the
    database in this case a dictionary, adds them to recipe page"""
    email = session['email']
    form = RecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        recipe_name = form.recipe_name.data
        recipe_type = form.recipe_type.data
        recipe = form.recipe.data
        Recipe(email, recipe_name, recipe_type, recipe)
        flash('New recipe added', 'success')
        return redirect(url_for('myrecipes'))
    return render_template('Categories.html', form=form)


@app.route('/edit_recipes/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_recipes(id):
    email = session['email']
    result = recipes[email][int(id)]
    form = RecipeForm(request.form)
    if request.method == 'GET':
        form.recipe_name.data = result['Recipe name']
        form.recipe_type.data = result['Recipe Type']
        form.recipe.data = result['Recipe']
    if request.method == 'POST' and form.validate():
        recipe_name = form.recipe_name.data
        recipe_type = form.recipe_type.data
        recipe = form.recipe.data
        Recipe(email, recipe_name, recipe_type, recipe)
        del recipes[email][int(id)]
        flash('Recipe Updated', 'success')
        return redirect(url_for('myrecipes'))
    return render_template('edit_recipes.html', form=form)


class RegistrationForm(Form):
    """Creates a registration form with validations for users to sign up"""
    first_name = StringField(u'First Name', validators=[validators.Length(min=3, max=20),
                             validators.input_required()])
    last_name = StringField(u'Last Name', validators=[validators.Length(min=3, max=20),
                            validators.input_required()])
    email = StringField(u'Email', validators=[validators.Length(min=10, max=30),
                        validators.input_required(), validators.Email()])
    password = PasswordField('Password', [
        validators.DataRequired(), validators.Length(min=8, max=25),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])

    confirm = PasswordField('Confirm Password')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Routes to the login page and signs in the user
    if email and password(hashed) matches the one in the user dictionary
    also creates a logged in session for the user"""
    if request.method == 'POST':
        # Get user data
        email = request.form['email']
        password_given = request.form['password']
        # compare
        email = hash(email)
        if email in userdata:
            if check_password_hash(userdata[email]['password'], password_given):
                session['logged_in'] = True
                session['user'] = userdata[email]['First Name']
                return redirect('myrecipes')

            else:
                error = 'Password does not match. Please try again'
                return render_template('Sign-in.html', error=error)
        else:
            error = 'email not found'
            return render_template('Sign-in.html', error=error)

    return render_template('Sign-in.html')


@app.route('/logout')
def logout():
    """clears the logged in user session and return him/her to the login page"""
    session.clear()
    flash('You have successfully logged out', 'success')
    return redirect(url_for('login'))


@app.route('/Sign-up', methods=['GET', 'POST'])
def sign_up():
    """Gives user ability to sign-up
    stores their information in userdata dictionery
    which will be used during login"""
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        # email is used here to as a unique value for every user object
        # email = form.email.data  # actual email used as object name
        email = User(form.email.data, form.password.data, form.first_name.data, form.last_name.data)
        session['email'] = email.user_id
        flash('You are now registered and can login', 'success')
        return redirect(url_for('login'))
    return render_template('Sign-up.html', form=form)


class RecipeForm(Form):
    """Creates the recipe form to rendered in the add recipe page
    (Category page)"""
    recipe_name = StringField(u'Recipe Name', validators=[validators.Length(min=3, max=30),
                              validators.input_required()])
    recipe_type = StringField(u'Recipe Type', validators=[validators.Length(min=6, max=30),
                              validators.input_required()])
    recipe = TextAreaField(u'Recipe', validators=[validators.Length(min=30),
                           validators.input_required()])


@app.route('/delete/<string:id>', methods=['POST'])
def delete(id):
    """Deletes a recipe when invoked"""
    email = session['email']
    del recipes[email][int(id)]
    flash('Recipe Deleted', 'success')
    return redirect(url_for('myrecipes'))


app.secret_key = 'Sir3n.sn@gmail.com'
