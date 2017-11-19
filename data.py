from werkzeug.security import generate_password_hash
userdata = {}


class User:
    """defines the user"""
    def __init__(self, email, password, first_name, last_name):
        global userdata
        user_id = hash(email)
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        userdata[user_id] = {'email': self.email, 'password': self.password,
                             'First Name': self.first_name, 'Last Name': self.last_name}


all_categories = {}
recipes = {}


class Category:
    """Stores the user Category"""
    category_id = 0
    global all_categories

    def __init__(self, user_id, category_name):
        self.category_name = category_name
        self.category_id = Category.category_id
        if user_id not in all_categories:
            all_categories[user_id] = {}
        all_categories[user_id].update({self.category_id: {'Category name': self.category_name,
                                                           'Category recipes': {}, }})
        Category.category_id += 1


class Recipe:
    """Stores the user recipes"""
    recipe_id = 0
    global recipes
    global all_categories

    def __init__(self, user_id, category_id, recipe_name, recipe):
        self.recipe_name = recipe_name
        self.recipe = recipe
        self.recipe_id = Recipe.recipe_id
        if category_id not in recipes:
            recipes[category_id] = {}
        recipes[category_id].update({self.recipe_id: {'Recipe name': self.recipe_name,
                                                      'Recipe': self.recipe}})
        all_categories[user_id][category_id]['Category recipes'].update(recipes[category_id])
        Recipe.recipe_id += 1
