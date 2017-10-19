import unittest


from app import app

class BasicTest(unittest.TestCase):
    '''Test if flask app returns correct results'''


    def SetUp(self):
        self.app = app.test_client()

    def  test_main_page(self):
        '''Tests flask redirects with no errors'''
        response = self.app.get('/', follow_redirects=True, content_type='html/text')
        self.assertEqual(response.status_code, 200)