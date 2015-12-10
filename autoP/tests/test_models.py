import unittest
from autoP.models import User, init_db, find_in_document
from autoP import create_app, app


class ModelsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')  # testing is lower case
        cls.current_app = cls.app
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        init_db()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def test_users(self):
        user = User(email='random@user.com', password='Passw0rd')
        user.save()
        user = find_in_document(User, email='random@user.com')
        self.assertFalse(user.verify_password('wrong'))
        self.assertTrue(user.verify_password('Passw0rd'))
        user.delete()
        user = find_in_document(User, email='huangjien@gmail.com')
        self.assertFalse(user.verify_password('wrong'))
        self.assertTrue(user.verify_password('Passw0rd'))

    def login(self, username, password):
        return self.app.test_client().post('/login', data=dict(
            email=username,
            password=password
            ), follow_redirects=True)

    def logout(self):
        return self.app.test_client().get('/logout', follow_redirects=True)

    def test_login_logout(self):
        rv = self.login('huangjien@gmail.com', 'Passw0rd')
        assert 'Logged in successfully.' in rv.data
        rv = self.logout()
        assert 'You have been logged out.' in rv.data
        rv = self.login('adminx', 'Passw0rd')
        assert 'We don\'t know you' in rv.data
        rv = self.login('huangjien@gmail.com', 'defaultx')
        assert 'wrong password' in rv.data


