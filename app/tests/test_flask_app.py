"""Tests for Yummy recipes flask applications"""

import unittest
from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from app.views import User


class BasicTest(unittest.TestCase):
    '''Test if flask app returns correct results'''

    def setUp(self):
        self.app = app.test_client()
        self.user = User('Sir3n','Hussein')

    def test_status(self):
        'Tests flask redirects with no errors'
        response = self.app.get('/', follow_redirects=True, content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_user_password(self):
        'Tests if the hash function works '
        self.assertNotEqual(self.user.profile['Sir3n'], 'Hussein', msg='Hash function does not work')

    def test_unauth_password(self):
        'Checks to see if wrong password provided will work'
        self.assertNotEqual(check_password_hash('pbkdf2:sha1:50000$iE1Ecm2A$f7833eff6df352437c4ba42020ca8d33d22325a5','Husni'), True, msg='Hash functions\
        does not work')

    def test_auth_password(self):
        'Tests if the hash function works'
        self.assertEqual(check_password_hash('pbkdf2:sha1:50000$iE1Ecm2A$f7833eff6df352437c4ba42020ca8d33d22325a5', 'Hussein'), True, msg='The hash function does\
        not work')