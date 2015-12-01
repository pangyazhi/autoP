import time
from functools import wraps
from flask import abort
import rom
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from . import login_manager


class Permission:
    ADMIN = 0x80
    VIEW = 0x01
    UPDATE = 0x02
    RUN = 0x04
    CREATE = 0x08


class User(UserMixin, rom.Model):
    # id = rom.Integer(required=True, index=True, unique=True, keygen=rom.IDENTITY)
    email = rom.String(required=True, index=True, unique=True, keygen=rom.IDENTITY)
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


class Role(rom.Model):
    # id = rom.Integer(required=True, unique=True, index=True, keygen=rom.IDENTITY)
    name = rom.String(unique=True)
    permissions = rom.Integer()
    users = rom.ForeignModel(User)

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.get_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.save()


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMIN)(f)


if __name__ == '__main__':
    # user = User(email='huangjien3@gmail.com', password='Passw0rd')
    # user.save()
    # print(user)
    user = User.get_by(email='huangjien@gmail.com')
    print(user)

