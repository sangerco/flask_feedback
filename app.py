from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask-feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """ redirect to register page """
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """ display form to register user
        log user into session """
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken! Please choose another.')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Successfully created user profile!', 'success')
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """ display form to log in user
        log user into session """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password']
    return render_template('login.html', form=form)

@app.route('/users/<username>')
def user_page(username):
    """ authenticate user in session
        redirect if not in session
        render template if is in session """
    user = User.query.get_or_404(username)
    if user.username == session['username']:
        flash(f'Welcome Back, {user.username}', 'success')
        all_feedback = Feedback.query.filter_by(username=username).all()
        return render_template('user.html', user=user, feedbacks=all_feedback)
    else:
        flash('Please login to view this page!', 'danger')
    return redirect('/login')

@app.route('/users/<username>/delete')
def delete_user(username):
    """ delete user from database
        delete all user feedback from database """
    user = User.query.get_or_404(username)
    if user.username == session['username']:
        feedback = Feedback.query.filter_by(username=username).all()
        db.session.delete(feedback)
        db.session.commit()

        db.session.delete(user)
        db.session.commit()
        
        return redirect('/register')
    else:
        flash('You do not have permission to do this!', 'danger')
    return redirect('/login')
    

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """ render form to add feedback
        add feedback data to database
        redirect back to user page
        """
    user = User.query.get_or_404(username)
    if user.username == session['username']:
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            
            new_feedback = Feedback(title=title, content=content, username=session['username'])
            db.session.add(new_feedback)
            db.session.commit()
            flash('Added new feedback.', 'success')
            return redirect(f'/users/{user.username}')
    else:
        flash('Must be logged in to add a new comment!')
    return render_template('add-feedback.html', form=form, user=user)

@app.route('/feedback/<int:id>/update', methods=['GET', 'POST'])
def update_feedback(id):
    """ render feedback update form
        update feedback data in db
        redirect back to feedback form
        """
    f = Feedback.query.get_or_404(id)
    if f.username == session['username']:
        form = FeedbackForm(obj=f)
        if form.validate_on_submit():
            f.title = form.title.data
            f.content = form.content.data
            f.username = session['username']
            db.session.commit()
            return redirect(f'/users/{f.username}')
        else:
            return render_template('edit-feedback.html', form=form, f=f)
    else:
        flash('You must be logged in to perform this function!', 'danger')
        return redirect('/login')


@app.route('/feedback/<int:id>/delete', methods=['GET', 'POST'])
def delete_feedback(id):
    """ authenticate feedback author
        delete feedback
        """
    f = Feedback.query.get_or_404(id)
    if f.username == session['username']:
        db.session.delete(f)
        db.session.commit()

        return redirect(f'/users/{f.username}')
    else:
        flash('You must be logged in to perform this function!', 'danger')
        return redirect('/login')


@app.route('/logout')
def logout_user():
    session.pop('username')
    flash('Logged Out.', 'info')
    return redirect('/register')

