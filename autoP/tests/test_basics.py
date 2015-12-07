import unittest
from autoP import create_app


class BasicsTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app('testing')
        cls.current_app = cls.app
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        # db.create_all()

    @classmethod
    def tearDownClass(cls):
        # db.session.remove()
        # db.drop_all()
        cls.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])

