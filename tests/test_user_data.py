import unittest
from data import userdata, User, recipes, Recipe
from app.app import app
from flask_testing import TestCase

class TestUser(unittest.TestCase):
    """Test for user and info provided"""

    def setUp(self):
        self.app = app
        self.client = self.app.test_client
        self.app.testing = True
        self.Sir3n = User('Sir3n.sn@gmail.com', 'Kali2017', 'Dhulkifli', 'Hussein')
        self.Johndoe = User('Johndoe@gmail.com', 'Kali2017', 'John', 'Doe')

    def test_user_registeration_credentials_is_stored(self):
        """Returns true if credentials are stored in a database"""
        self.assertTrue(userdata[self.Sir3n.user_id]['email'], 'Sir3n.sn@gmail.com')

    def test_user_password_is_encrypted(self):
        """Returns true if password is encrypted"""
        self.assertNotEqual(userdata[self.Sir3n.user_id]['password'], 'Kali2017', msg='Password is not encrypted')

    def test_password_salts_are_random(self):
        """Returns true if each users password is encrypted differently
        even when passwords are the same
        here we use the example john and sir3n
        both users share the same password"""
        self.assertNotEqual(userdata[self.Sir3n.user_id]['password'], userdata[self.Johndoe.user_id]['password'])

    def test_recipe_is_created(self):
        """Tests if user recipe is added to dictionery"""
        meal = Recipe('current_user', 'Pizza', 'Carbs', 'Blah blah blah 2 spoons, and voila cooked')
        self.assertIn('current_user', recipes, msg='recipe was added')
        self.assertIn('Pizza', recipes['current_user'][meal.recipe_id]['Recipe name'],)


class MyViewTestCase(TestCase):
    """Test for views"""
    def create_app(self):
        """Creates app instance"""
        test_app = app
        test_app.config['TESTING'] = True
        return test_app

    def setUp(self):
        self.Sir3n = User('Sir3n.sn@gmail.com', 'Kali2017', 'Dhulkifli', 'Hussein')

    def test_app_running(self):
            self.app.test_client().get('/')
            self.assert_template_used('index.html')

    def test_sign_up_page(self):
        rv = self.app.test_client().get('/Sign-up')
        assert b"Sign-up" in rv.data
        self.assert_template_used('Sign-up.html')

    def test_sign_up_user(self):
        rv = self.app.test_client().post('/Sign-up', data={
            "first_name": 'Kali',
            "last_name": 'Kali',
            "email": 'Kali@gmail.com',
            "password": '12345678',
            "confirm": '12345678'
        }, follow_redirects=True)
        assert b'You are now registered and can login' in rv.data

    def test_login_user_with_wrong_email(self):
        login = self.app.test_client().post('/login', data=
        {"email": 'Kaligraph@gmail.com',
         "password": '12345678',
         })

        assert b'email not found' in login.data

    def test_login_user_with_wrong_password(self):
        self.Sir3n = User('Sir3n.sn@gmail.com', 'Kali2017', 'Dhulkifli', 'Hussein')
        login = self.app.test_client().post('/login', data={
            "email": 'Sir3n.sn@gmail.com',
            "password": '12345678910'
        }, follow_redirects=True)
        assert b'Password does not match. Please try again' in login.data

    def test_unauthorized_user_access_recipe_page(self):
        unauthorized = self.app.test_client().get('/myrecipes', follow_redirects=True)
        assert b'Unauthorized to view this page. Please login' in unauthorized.data

    def test_unauthorized_user_access_category_page(self):
        unauthorized = self.app.test_client().get('/Categories', follow_redirects=True)
        assert b'Unauthorized to view this page. Please login' in unauthorized.data

    def test_unauthorized_user_access_edit_recipe_page(self):
        unauthorized = self.app.test_client().get('/edit_recipes/1', follow_redirects=True)
        assert b'Unauthorized to view this page. Please login' in unauthorized.data

    def test_logout_user(self):
        logout = self.app.test_client().get('/logout', follow_redirects=True)
        assert b"You have successfully logged out" in logout.data