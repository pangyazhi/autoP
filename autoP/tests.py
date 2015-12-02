import time
from functools import wraps
import rom
from flask_login import UserMixin, current_user
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from autoP import login_manager


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


class Permission:
    ADMIN = 0x80
    VIEW = 0x01
    UPDATE = 0x02
    RUN = 0x04
    CREATE = 0x08


@login_manager.user_loader
def load_user(user_id):
    return User.get_by(email=user_id)


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


class UiObject(rom.Model):
    name = rom.String(required=True, unique=True, index=True, keygen=rom.SIMPLE)
    description = rom.Text()
    xpath = rom.Text(index=True, keygen=rom.SIMPLE)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)


class Computer(rom.Model):
    name = rom.String(required=True, unique=True, index=True, keygen=rom.SIMPLE)
    ipAddress = rom.String(required=True)
    osVersion = rom.String(required=True)
    status = rom.String(required=True)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)


class Variable(rom.Model):
    name = rom.String(required=True, unique=True, index=True, keygen=rom.SIMPLE)
    data = rom.String()
    description = rom.Text()
    parent = rom.ForeignModel(rom.Model)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)


class Environment(rom.Model):
    name = rom.String(required=True, unique=True, index=True, keygen=rom.SIMPLE)
    status = rom.String(required=True)
    variables = rom.ForeignModel(Variable)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)
    client = rom.ForeignModel(Computer, required=True)
    appServer = rom.ForeignModel(Computer, required=True)
    dbServer = rom.ForeignModel(Computer, required=True)

    def add_variable(self, name, data):
        variable = Variable(name=name, data=data, parent=self)
        variable.save()


class TestActivity(rom.Model):
    name = rom.String(required=True, unique=True, index=True, keygen=rom.SIMPLE)
    description = rom.Text()
    parent = rom.ForeignModel(rom.Model)
    author = rom.ForeignModel(User)
    enabled = rom.Boolean()
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)


class Instance(rom.Model):
    testName = rom.String(required=True, index=True, keygen=rom.SIMPLE)
    suite = rom.ForeignModel(TestActivity)
    status = rom.String(required=True)
    environment = rom.String(Environment)
    description = rom.Text()
    variables = rom.OneToMany(Variable)
    xpath = rom.Text(index=True, keygen=rom.SIMPLE)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)


class DataObject(rom.Model):
    name = rom.String(required=True, unique=True, index=True, keygen=rom.SIMPLE)
    description = rom.Text()
    data = rom.String()
    parent = rom.ForeignModel(rom.Model)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)


class Result(rom.Model):
    name = rom.String(required=True, unique=True, index=True, keygen=rom.SIMPLE)
    description = rom.Text()
    instance = rom.ForeignModel(Instance)
    parent = rom.ForeignModel(rom.Model)
    original = rom.String()
    final = rom.String()
    stopped_at = rom.Float(default=time.time)
    created_at = rom.Float(default=time.time)
    updated_at = rom.Float(default=time.time)


class StepResult(Result):
    action = rom.String(required=True)
    data = rom.ForeignModel(DataObject)
    uiObject = rom.ForeignModel(UiObject)
    reason = rom.String()
    snapshot = rom.String()



