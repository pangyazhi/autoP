import time
from functools import wraps
import datetime
from flask_login import UserMixin, current_user
from werkzeug.exceptions import abort
from werkzeug.security import generate_password_hash, check_password_hash
from autoP import login_manager, delete_db
from mongoengine import *


class Permission:
    ADMIN = 'ADMIN'
    UPDATE = 'UPDATE'
    CREATE = 'CREATE'
    DELETE = 'DELETE'
    VIEW = 'VIEW'
    RUN = 'RUN'


ALL_PERMISSIONS = {
    Permission.ADMIN,
    Permission.UPDATE,
    Permission.CREATE,
    Permission.DELETE,
    Permission.VIEW,
    Permission.RUN
}


def find_in_document(Document, **kwargs):
    qs = Document.objects(**kwargs)
    if qs is None:
        return None
    return qs.first()


# def regex_search(Document, searchString, *args):
#     m = []
#     for a in args:
#         m.append(Q(**{a : regex.compile(searchString)}))
#
#     query = QCombination(QCombination.AND, m)
#     return Document.objects(query)

class Role(Document):
    name = StringField(unique=True)
    description = StringField()
    permissions = ListField(StringField(choices=ALL_PERMISSIONS))
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(), required=True)

    @staticmethod
    def regex_search(query_string):
        return Role.objects(Q(name__icontains=query_string) or
                            Q(description__icontians=query_string) or
                            Q(permissions__S__icontains=query_string))

    @staticmethod
    def get(name):
        qs = Role.objects(name=name)
        if qs is None:
            return None
        return qs.first()

    @staticmethod
    def insert_roles():

        roles = {'User': {
            Permission.VIEW,
            Permission.CREATE},
            'Moderator': {
                Permission.UPDATE,
                Permission.RUN,
                Permission.VIEW},
            'Guest': {
                Permission.VIEW},
            'Administrator': {
                Permission.UPDATE,
                Permission.ADMIN,
                Permission.RUN,
                Permission.VIEW
            }
        }
        for r in roles:
            role = Role.objects(name=r)
            if role.__len__() == 0:
                ro = Role(name=r)
                ro.save()
                for p in roles[r]:
                    ro.update(push__permissions=p)
                ro.save()


class User(UserMixin, Document):
    email = StringField(required=True)
    description = StringField()
    password = StringField()
    password_hash = StringField()
    role = ReferenceField(Role)
    authenticated = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(), required=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if 'password' in kwargs:
            self.set_password(kwargs['password'])
        if self.role is None:
            self.role = Role.get(name='User')

    # TODO add regular expression search later
    @staticmethod
    def regex_search(query_string):
        return User.objects(Q(email__icontains=query_string) or Q(description__icontians=query_string))

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        self.password = None

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

    def __repr__(self):
        return self.email


@login_manager.user_loader
def load_user(user_id):
    return find_in_document(User, email=user_id)


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


class UiObject(Document):
    name = StringField(required=True)
    description = StringField()
    xpath = StringField()
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(), required=True)

    @staticmethod
    def regex_search(query_string):
        return UiObject.objects(Q(name__icontains=query_string) or
                            Q(description__icontians=query_string),
                            Q(xpath__icontians=query_string))

class Computer(Document):
    name = StringField(required=True)
    description = StringField()
    ipAddress = StringField()
    osVersion = StringField(required=True)
    status = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(), required=True)

    @staticmethod
    def regex_search(query_string):
        return Computer.objects(Q(name__icontains=query_string) or
                            Q(description__icontians=query_string),
                            Q(status__icontians=query_string))


class Variable(Document):
    name = StringField(required=True)
    data = StringField()
    description = StringField()
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(), required=True)

    @staticmethod
    def regex_search(query_string):
        return Variable.objects(Q(name__icontains=query_string) or
                            Q(description__icontians=query_string),
                            Q(data__icontians=query_string))


class Environment(Document):
    name = StringField(required=True)
    description = StringField()
    status = StringField(required=True)
    variables = ListField(Variable)
    client = ReferenceField(Computer, required=True)
    appServer = ReferenceField(Computer, required=True)
    dbServer = ReferenceField(Computer, required=True)
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(), required=True)

    def add_variable(self, name, data):
        variable = Variable(name=name, data=data, parent=self)
        variable.save()

    @staticmethod
    def regex_search(query_string):
        return Environment.objects(Q(name__icontains=query_string) or
                            Q(description__icontians=query_string),
                            Q(status__icontians=query_string))


class TestActivity(Document):
    name = StringField(required=True)
    description = StringField()
    author = ReferenceField(User)
    enabled = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(), required=True)

    @staticmethod
    def regex_search(query_string):
        return TestActivity.objects(Q(name__icontains=query_string) or
                            Q(description__icontians=query_string))


class Instance(Document):
    name = StringField(required=True)
    suite = ReferenceField(TestActivity)
    status = StringField(required=True, default='Not Start')
    environment = ReferenceField(Environment)
    description = StringField()
    variables = ListField(Variable)
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(), required=True)

    @staticmethod
    def regex_search(query_string):
        return Instance.objects(Q(name__icontains=query_string) or
                            Q(description__icontians=query_string),
                            Q(status__icontians=query_string))


class DataObject(Document):
    name = StringField(required=True)
    description = StringField()
    data = ListField(Variable)
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(), required=True)

    @staticmethod
    def regex_search(query_string):
        return DataObject.objects(Q(name__icontains=query_string) or
                            Q(description__icontians=query_string))


class Result(Document):
    name = StringField(required=True)
    description = StringField()
    instance = ReferenceField(Instance)
    original = StringField()
    final = StringField()
    stopped_at = DateTimeField(default=datetime.datetime.now())
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(), required=True)

    @staticmethod
    def regex_search(query_string):
        return Result.objects(Q(name__icontains=query_string) or
                            Q(description__icontians=query_string))


class StepResult(Document):
    action = StringField(required=True)
    description = StringField()
    instance = ReferenceField(Instance)
    original = StringField()
    final = StringField()
    data = ListField(Variable)
    uiObject = ReferenceField(UiObject)
    reason = StringField()
    snapshot = StringField()
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(), required=True)


class Task(Document):
    name = StringField(required=True)
    url = StringField(required=True, default='/dash_board')
    description = StringField()
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(), required=True)
    required_role = ListField(Role)

    @staticmethod
    def regex_search(query_string):
        return Task.objects(Q(name__icontains=query_string) or
                            Q(description__icontians=query_string))


class TaskGroup(Document):
    name = StringField(required=True)
    view_task = ReferenceField(Task)
    task_list = ListField(Task)
    description = StringField()
    created_at = DateTimeField(default=datetime.datetime.now(), required=True)
    updated_at = DateTimeField(default=datetime.datetime.now(), required=True)

    @staticmethod
    def regex_search(query_string):
        return TaskGroup.objects(Q(name__icontains=query_string) or
                            Q(description__icontians=query_string))


def init_db():
    delete_db()
    Role.insert_roles()
    admin = User(email='huangjien@gmail.com', password='Passw0rd')
    admin.role = Role.get(name='Administrator')
    admin.save()


def query_results(query_string):
    if ':' in query_string:
        document_type = query_string.split(':')[0].lower()
        func = get_regex_search_method(document_type)
        if func is None:
            return []
        real_query_strings = query_string.split(':')[1].split(' ')
    else:
        real_query_strings = [query_string]
        func = User.regex_search
    results = []
    for qs in real_query_strings:
        for r in func(qs):
            if r not in results:
                results.append(r)
    return results


def get_regex_search_method(document_type):
    functions_map = {
        'user': User.regex_search,
        'usr': User.regex_search,
        'task': Task.regex_search,
        'tsk': Task.regex_search,
        'role': Role.regex_search
    }
    if document_type in functions_map.keys():
        return functions_map[document_type]
    return None

