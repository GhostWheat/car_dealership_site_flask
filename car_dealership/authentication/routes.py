from flask import Blueprint, render_template, request, redirect, url_for, flash
from car_dealership.forms import UserLoginForm
from car_dealership.models import User, db
from werkzeug.security import check_password_hash

from flask_login import login_user, logout_user, current_user, login_required



auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserLoginForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            username= form.username.data
            password = form.password.data
            print(email, username)

            user = User(email, username, password = password)

            db.session.add(user)
            db.session.commit()

            flash(f'You have successfully created a user account {username}', 'user-created')

            return redirect(url_for('auth.signin'))

    except:
        raise Exception('Invalid Form Data: please check your form')
    return render_template('signup.html', form=form)



@auth.route('/signin', methods = ['GET', 'POST'])
def signin():
    form = UserLoginForm()
   
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            print(email,password)

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                print(f"this is the logged user: {logged_user}")
                login_user(logged_user)
                flash(f"You were successfully logged in: Via email/password", "auth-success")
                return redirect(url_for('site.profile'))

            else: 
                flash('Your email/password is incorrect', 'auth-failed')
                return redirect(url_for('auth.signin'))
    
    except:
        raise Exception('Invalid Form Data: Please check your Form')

    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))
