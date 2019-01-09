import unittest
from app.models import User, Role, Anonymouser

class UserModelTestCase(unitest.TestCase):
    def test_password_setter(self):
        u = User(password = 'haha')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'haha')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = 'haha')
        self.assertTrue(u.verify_password('haha'))
        self.assertTrue(u.verify_password('haha'))

    def test_password_salts_are_random(self):
        u = User(password='haha')
        u2 = User(password='haha')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_and_permissions(self):
        Role.insert_roles()
        u = User(email='17826839707@163.com', password='123')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))

    def test_anonymous_user(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))
