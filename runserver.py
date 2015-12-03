from os import environ
from autoP import create_app

if __name__ == '__main__':
    config = environ.get('CONFIG') or 'default'
    app = create_app(config)
    app.run()
