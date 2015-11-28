import time

import rom
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import login_manager


class Permission:
    ADMIN = 0x80
    VIEW = 0x01
    UPDATE = 0x02
    RUN = 0x04
    CREATE = 0x08


class User(UserMixin, rom.Model):
    email = rom.String(required=True, unique=True)
    password_hash = rom.String()
    authenticated = rom.Boolean(default=False)
    created_at = rom.Float(default=time.time)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


@login_manager.user_loader
def load_user(user_id):
    return User.get_by(email=user_id)


if __name__ == '__main__':
    # user = User(email='huangjien3@gmail.com', password='Passw0rd')
    # user.save()
    # print(user)
    user = User.get_by(email='huangjien@gmail.com')
    print(user)

