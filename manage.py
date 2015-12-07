#!/usr/bin/env python
import os
from autoP import create_app
from autoP.models import *
from flask_script import Manager, Shell

# from flask_migrate import Migrate

app = create_app(os.getenv('CONFIG') or 'default')
manager = Manager(app)


# migrate = Migrate(app)


def make_shell_context():
    return {'app': app, 'User': User, 'Permission': Permission, 'Role': Role, 'Result': Result,
            'StepResult': StepResult, 'DataObject': DataObject}


manager.add_command('shell', Shell(make_context=make_shell_context))


@manager.command
def test():
    import unittest
    tests_dir = os.path.abspath('.')
    tests = unittest.TestLoader().discover(tests_dir)
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profiler.
    :param length:
    :param profile_dir:
    """
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                      profile_dir=profile_dir)
    app.run()


@manager.command
def coverage():
    cov = None
    if os.environ.get('FLASK_COVERAGE'):
        import coverage
        cov = coverage.coverage(branch=True, include='app/*')
        cov.start()

    if os.path.exists('.env'):
        print('Importing environment from .env...')
        for line in open('.env'):
            var = line.strip().split('=')
            if len(var) == 2:
                os.environ[var[0]] = var[1]
    if not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    if cov:
        cov.stop()
        cov.save()
        print('Coverage Summary:')
        cov.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        cov.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        cov.erase()


@manager.command
def deploy():
    """Run deployment tasks."""
    from autoP.models import init_db
    init_db()


@manager.command
def clear():
    """
    Delete everything in the Redis Database
    :return: no return
    """
    import redis
    r = redis.StrictRedis()
    r.flushdb()


if __name__ == '__main__':
    manager.run()
