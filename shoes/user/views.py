from flask import render_template, redirect, request, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user

from . import user_blueprint
from .. import db
from ..models import User
from ..decorators import admin_required, super_admin_required

from .forms import RoleChangeForm, UserDeleteForm

@user_blueprint.route('/user_index', methods=['GET', 'POST'])
@login_required
@super_admin_required
def user_index():
    users = User.query.all()
    return render_template('user/user_index.html', users=users)

@user_blueprint.route('/user_permission', methods=['GET', 'POST'])
@login_required
@super_admin_required
def user_permission():
    form = RoleChangeForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            user.role = form.role.data
            return render_template('user/user_index.html', user=user)
        else:
            flash('无此用户')
    return render_template('user/user_permission.html', form=form)

@user_blueprint.route('/user_delete', methods=['GET', 'POST'])
@login_required
@super_admin_required
def user_delete():
    form = UserDeleteForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            User.query.filter_by(username=form.username.data).delete()
            flash('删除成功')
            return redirect(url_for('user.user_delete'))
        else:
            flash('无此用户')
    return render_template('user/user_delete.html', form=form)