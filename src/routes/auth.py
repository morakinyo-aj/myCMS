from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from utils import bcrypt, db
from models.models import User
from forms.login import LoginForm
from forms.register import RegisterForm



def init_auth_routes(app):
    @app.route("/register", methods=['GET','POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html', form=form)
    
    @app.route("/login", methods=['GET','POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or pasword','error')
        return render_template('login.html', form=form)

    @app.route("/logout", methods=['GET','POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))