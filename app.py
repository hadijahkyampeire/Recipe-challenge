from flask import Flask, render_template, request, session, flash, url_for, redirect
from wtforms import Form, StringField, PasswordField, TextAreaField, validators
from werkzeug.security import check_password_hash
from data import User, userdata, recipes, Recipe, Category, all_categories
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


@app.route('/create')
@login_required
def create():
    """Routes to the category page for authorized users only"""
    if categories:
        email = session['email']
        try:
            return render_template('create.html', categories_list=all_categories[email], email=email)
        except KeyError:
            msg = 'Create your first Recipe Category'
            return render_template('create.html', msg=msg)
    else:
        msg = 'Create your first Recipe Category'
        return render_template('create.html', msg=msg)


class CategoryForm(Form):
    """Creates the category form to be rendered in the add recipe page
    (Category page)"""
    category_name = StringField(u'Category Name', validators=[validators.Length(min=3, max=30),
                                validators.input_required()])


@app.route('/Create_categories', methods=['GET', 'POST'])
@login_required
def create_categories():
    """routes to the categories creation page
    handles post request from user and adds them to the
    database in this case a dictionary, adds them to category page"""
    email = session['email']
    form = CategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        category_name = form.category_name.data
        Category(email, category_name)
        flash('New Category added', 'success')
        return redirect(url_for('create'))
    return render_template('Create_categories.html', form=form)


@app.route('/edit_categories/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_categories(id):
    email = session['email']
    result = all_categories[email][int(id)]
    form = CategoryForm(request.form)
    if request.method == 'GET':
        form.category_name.data = result['Category name']
    if request.method == 'POST' and form.validate():
        category_name = form.category_name.data
        Category(email, category_name)
        del all_categories[email][int(id)]
        flash('Category Updated', 'success')
        return redirect(url_for('create'))
    return render_template('edit_categories.html', form=form)


@app.route('/delete_category/<string:id>', methods=['POST'])
@login_required
def delete_category(id):
    """Deletes a recipe when invoked"""
    email = session['email']
    del all_categories[email][int(id)]
    flash('Category Deleted', 'success')
    return redirect(url_for('create'))


@app.route('/create/<string:id>/myrecipes')
@login_required
def myrecipes(id):
    """Routes to the recipes page for authorized users only"""
    id = int(id)
    if id or id == 0:
        email = session['email']
        try:
            all_categories[email][id]

        except KeyError:
            flash('The category does not exist', 'danger')
            return redirect(url_for('create'))
        if recipes:
            email = session['email']
            try:
                return render_template('myrecipes.html', recipes_list=all_categories[email][id]['Category recipes'],
                                       email=email, id=id, category_name=all_categories[email][id]['Category name'])
            except KeyError:
                msg = 'Create your first recipe'
                return render_template('myrecipes.html', msg=msg, id=id, category_name=all_categories[email][id]['Category name'])
        else:
            msg = 'Create your first recipe'
            return render_template('myrecipes.html', msg=msg, id=id, category_name=all_categories[email][id]['Category name'])
    else:
        flash('The category does not exist', 'danger')
        return redirect(url_for('create'))


@app.route('/Categories', methods=['GET', 'POST'])
@login_required
def categories():
    """routes to the categories page
    handles post request from user and adds them to the
    database in this case a dictionary, adds them to recipe page"""
    email = session['email']
    category_id = request.args.get('val', '')
    form = RecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        recipe_name = form.recipe_name.data
        recipe = form.recipe.data
        Recipe(email, int(category_id), recipe_name, recipe)
        flash('New recipe added', 'success')
        return redirect(url_for('myrecipes', id=category_id))
    return render_template('Categories.html', form=form)


@app.route('/edit_recipes/<string:id>', methods=['GET', 'POST'])
@login_required
def edit_recipes(id):
    """Edit the recipes in the categories"""
    email = session['email']
    category_id = request.args.get('val', '')
    result = recipes[int(category_id)][int(id)]
    form = RecipeForm(request.form)
    if request.method == 'GET':
        form.recipe_name.data = result['Recipe name']
        form.recipe.data = result['Recipe']
    if request.method == 'POST' and form.validate():
        recipe_name = form.recipe_name.data
        recipe = form.recipe.data
        Recipe(email, int(category_id), recipe_name, recipe)
        del recipes[int(category_id)][int(id)]
        del all_categories[email][int(category_id)]['Category recipes'][int(id)]
        flash('Recipe Updated', 'success')
        return redirect(url_for('myrecipes', id=category_id))
    return render_template('edit_recipes.html', form=form)


@app.route('/delete/<string:recipe_id>', methods=['POST'])
@login_required
def delete(recipe_id):
    """Deletes a recipe when invoked"""
    email = session['email']
    category_id = request.args.get('val', '')
    del recipes[int(category_id)][int(recipe_id)]
    del all_categories[email][int(category_id)]['Category recipes'][int(recipe_id)]
    flash('Recipe Deleted', 'success')
    return redirect(url_for('myrecipes', id=category_id))


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
                session["email"] = email
                return redirect('create')

            else:
                error = 'Password does not match. Please try again'
                return render_template('Sign-in.html', error=error)
        else:
            error = 'email not found'
            return render_template('Sign-in.html', error=error)

    return render_template('Sign-in.html')


@app.route('/logout')
@login_required
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
        if hash(form.email.data) not in userdata:
            User(form.email.data, form.password.data, form.first_name.data, form.last_name.data)
            flash('You are now registered and can login', 'success')
            return redirect(url_for('login'))
        else:
            error = "The email address already exists"
            return render_template('Sign-up.html', error=error, form=form)
    return render_template('Sign-up.html', form=form)


class RecipeForm(Form):
    """Creates the recipe form to rendered in the add recipe page
    (Category page)"""
    recipe_name = StringField(u'Recipe Name', validators=[validators.Length(min=3, max=30),
                              validators.input_required()])
    recipe = TextAreaField(u'Recipe', validators=[validators.Length(min=30),
                           validators.input_required()])


app.secret_key = 'Sir3n.sn@gmail.com'
