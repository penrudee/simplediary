import imp
import re
from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db 
from app.models import User 
from app.forms import LoginForm, RegisterForm
from app.auth import auth_bp
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

@auth_bp.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.index"))
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user.password is None or not form.password.data:
            flash("Invalid username or password")
        login_user(user, remember=form.remember_me.data )
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main_bp.index')
        return redirect(next_page)

    return render_template('login.html',form=form, title="Sign In")

@auth_bp.route('/signup',methods=['POST','GET'])
def signup():
    form = RegisterForm()
    
    if request.method == 'POST':
        username = form.username.data 
        email = form.email.data 
        password = form.password.data 
        

        newuser= User(username=username, email=email, password=password)
        db.session.add(newuser)
        db.session.commit()
        return redirect(url_for('auth_bp.login'))
    return render_template("register.html",form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    print('logout')
    return redirect(url_for('auth_bp.login'))
