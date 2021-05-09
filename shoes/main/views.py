from datetime import datetime, time
from flask import render_template, session, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required

from . import main_blueprint
from ..models import User, Shoe
from ..decorators import admin_required, super_admin_required
from .forms import ShoeForm, ShoeAddForm, ShoeQueryForm, ShoeDeleteForm, ShoeNoteForm
from .. import db

from . import logic

@main_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def index():
    #shoes = Shoe.query.all()
    #return render_template('index.html', shoes=shoes, current_user=current_user)
    return render_template('index.html')

@main_blueprint.route('/shoe_index', methods=['GET', 'POST'])
@login_required
def shoe_index(shoe_num=None):
    if shoe_num:
        shoe = Shoe.query.filter_by(number=shoe_num).first()
        return render_template('main/shoe_index.html', shoe=shoe)
    else:
        shoes = Shoe.query.all()
        return render_template('main/shoe_index.html', shoes=shoes)

@main_blueprint.route('/shoes')
@login_required
def shoes():
    #shoes_data = logic.get_shoes()
    #return shoes_data
    shoes = Shoe.query.all()
    return render_template('shoes.html', shoes=shoes)

@main_blueprint.route('/shoe/<string:shoe_name>')
@login_required
def shoe_info(shoe_num):
    #shoe_info = logic.get_shoe(shoe_id)
    #return shoe_info
    shoe = Shoe.query.filter_by(number=shoe_num).first()
    return render_template('shoe.html', shoe=shoe)

@main_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_shoes():
    form = ShoeAddForm()
    if form.validate_on_submit():
        shoe = Shoe.query.filter_by(name=form.name.data,
                                    number=form.number.data,
                                    type=form.type.data,
                                    size=form.size.data).first()
        if shoe:
            shoe.count += form.count.data
            shoe.note = form.note.data
        else:
            count = form.count.data
            shoe = Shoe(name=form.name.data,
                        number=form.number.data,
                        type=form.type.data,
                        size=form.size.data,
                        count=count,
                        note=form.note.data)
            db.session.add(shoe)
            db.session.commit()
        return redirect(url_for('main.shoe_index'))
    return render_template('main/add.html', form=form)

@main_blueprint.route('/del', methods=['GET', 'POST'])
@login_required
@admin_required
def del_shoes():
    form = ShoeDeleteForm()
    action = False
    if form.validate_on_submit():
        shoe = Shoe.query.filter_by(number=form.number.data,
                                    type=form.type.data,
                                    size=form.size.data).first()
        if shoe:
            if shoe.count > form.count.data:
                shoe.count -= form.count.data
                shoe.note = form.note.data
                action = True
            elif shoe.count == form.count.data:
                Shoe.query.filter_by(number=form.number.data,
                                    type=form.type.data,
                                    size=form.size.data).delete()
                action = True
            else:
                flash('此鞋库存不足')
        else:
            flash('此鞋不在库存中')
    if action:
        return redirect(url_for('main.shoe_index'))
    else:
        return render_template('main/delete.html', form=form)

@main_blueprint.route('/query', methods=['GET', 'POST'])
@login_required
def query_shoes():
    form = ShoeQueryForm()
    if form.validate_on_submit():
        if form.number.data:
            shoe = Shoe.query.filter_by(number=form.number.data,
                                    type=form.type.data,
                                    size=form.size.data).first()
        else:
            shoe = Shoe.query.filter_by(name=form.name.data,
                                    type=form.type.data,
                                    size=form.size.data).first()
        if shoe:
            return render_template('main/shoe_index.html', shoe=shoe)
        else:
            flash('没有找到数据')
    return render_template('main/query.html', form=form)

@main_blueprint.route('/update_notes', methods=['GET', 'POST'])
@login_required
def update_notes():
    form = ShoeNoteForm()
    if form.validate_on_submit():
        if form.number.data:
            shoe = Shoe.query.filter_by(number=form.number.data,
                                    type=form.type.data,
                                    size=form.size.data).first()
        else:
            shoe = Shoe.query.filter_by(name=form.name.data,
                                    type=form.type.data,
                                    size=form.size.data).first()
        shoe.note = form.note.data
        db.session.commit()
        if shoe:
            return render_template('main/shoe_index.html', shoe=shoe)
        else:
            flash('没有找到数据')
    return render_template('main/update_notes.html', form=form)