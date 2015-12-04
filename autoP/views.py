from datetime import datetime
from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import logout_user, login_required, login_user
from autoP.models import User, load_user
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


@app.route('/search', methods=['GET', 'POST'])
# @login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        # do some search here
        app.logger.info(form.search.raw_data)
    return render_template('search.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        users = load_user(form.email.raw_data)
        if users.__len__() == 0:
            flash('We don\'t know you')
            return render_template('login.html', form=form)
        user = users[0]
        if user.verify_password(form.password.raw_data[0]):
            login_user(user)
            flash('Logged in successfully.')
            return redirect(url_for('search'))
        else:
            flash('wrong password')
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
            flash('User already existing.')
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
