import unittest
from data import userdata, User, recipes, Recipe


class TestUser(unittest.TestCase):
    """Test for user and info provided"""

    def setUp(self):
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
        meal = Recipe('Pizza', 'Carbs', 'Blah blah blah 2 spoons, and voila cooked')
        self.assertIn(meal.recipe_id, recipes, msg='recipe was added')
        self.assertIn('Pizza', recipes[meal.recipe_id]['Recipe name'],)
