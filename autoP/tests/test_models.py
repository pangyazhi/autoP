import unittest
from autoP.models import User, init_db


class ModelsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    def test_users(self):
        user = User(email='random@user.com', password='Passw0rd')
        user.save()
        user = User.get_by(email='random@user.com')
        self.assertFalse(user.verify_password('wrong'))
        self.assertTrue(user.verify_password('Passw0rd'))
        user.delete()
        user = User.get_by(email='huangjien@gmail.com')
        self.assertFalse(user.verify_password('wrong'))
        self.assertTrue(user.verify_password('Passw0rd'))

