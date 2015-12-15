from datetime import datetime
from flask import render_template, redirect, url_for, flash, abort, request, jsonify
from flask_login import logout_user, login_required, login_user

from autoP.models import User, load_user, query_results
from forms import LoginForm, RegistrationForm, SearchForm
from . import app


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Automation Center',
        year=datetime.now().year,
        message='Welcome to the Automation Center'
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        message='Contact me if you have any questions.'
    )


@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        message='Project Brief.'
    )


@app.route('/show')
def show():
    """Renders the listUsers page."""
    return render_template(
        'listUsers.html',
        title='List Users',
        message='These are the users in our system'
    )


@app.route('/dash_board')
def dash_board():
    return render_template(
        'dash_board.html',
        title = 'Dash Board',
        message='Welcome to the Automation Center'
    )


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        # input some search here
        search_string = form.search.data
        flash(search_string)
        app.logger.info(form.search.data)
        return redirect(url_for('search_result', query=search_string))
        # redirect(url_for('search'))
    return render_template('search.html', form=form)


@app.route('/search_result/<string:query>')
@login_required
def search_result(query):
    results = query_results(query)
    return render_template('_results.html', query=query, results=results)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        users = load_user(form.email.data)
        if users is None:
            flash(message='We don\'t know you', category='error')
            return render_template('login.html', form=form)
        user = users
        if user.verify_password(form.password.data):
            login_user(user)
            flash(message='Logged in successfully.', category='message')
            return redirect(url_for('dash_board'))
        else:
            flash(message='wrong password', category='error')
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.get_by(email=form.email.data):
            flash(message='User already existing.', category='error')
            return redirect(url_for('register'))
        user = User(email=form.email.data, password=form.password.data)
        user.save()
        flash('User is registered!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/shutdown')
def server_shutdown():
    if app.testing:
        return 'Cannot shutdown testing......'
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down the server......'


@app.errorhandler(403)
def forbidden(error):
    return handle_error(error, 'Forbidden', 403)


@app.errorhandler(404)
def not_found(error):
    return handle_error(error, 'Page Not Found', 404)


@app.errorhandler(500)
def internal_server_error(error):
    return handle_error(error, 'Internal Server Error', 500)


def handle_error(error, server_error, error_code):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({'error': server_error})
        response.status_code = error_code
        return response
    return render_template('error.html', message='Internal Server Error:'), error_code
