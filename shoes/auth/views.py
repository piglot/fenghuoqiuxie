from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user

from . import auth_blueprint
from .. import db
from ..models import User
from ..email import send_email

from .forms import LoginForm, RegistrationForm


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            #session['username'] = user
            #db.session.commit()
            #next = request.args.get('next')
            #if next is None or not next.startswith('/'):
            #    next = url_for('main.index')
            #return redirect(next)
            return redirect(url_for('main.index'))
        flash('用户名或密码错误.')
    return render_template('auth/login.html', form=form)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        #token = user.generate_confirmation_token()
        #send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        #flash('确认邮件已发至您的邮箱.')
        flash('You can now login.')
        #return redirect(url_for('main.index'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_blueprint.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))

"""
@auth_blueprint.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.endpoint[:5] != 'auth.' \
        and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))
"""

@auth_blueprint.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')
    #return redirect(url_for('main.index'))

@auth_blueprint.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))
