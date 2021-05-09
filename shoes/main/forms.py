from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

Shoe_Type = [(1, '男款'), (2, '女款'), (3, '男女同款')]
Shoe_Size = [(240,'240'), (245,'245'), (250, '250'), (255, '255'), (260, '260')]
class ShoeForm(FlaskForm):
    number = StringField('鞋号', validators=[DataRequired()])
    name = StringField('鞋名', validators=[DataRequired()])
    type = SelectField('款式', choices=Shoe_Type, coerce=int, default=3)
    size = SelectField('尺码', choices=Shoe_Size, coerce=int)
    submit = SubmitField('提交')

class ShoeAddForm(FlaskForm):
    number = StringField('鞋号', validators=[DataRequired()])
    name = StringField('鞋名', validators=[DataRequired()])
    type = SelectField('款式', choices=Shoe_Type, coerce=int, default=3)
    size = SelectField('尺码', choices=Shoe_Size, coerce=int)
    count = IntegerField('数量', validators=[DataRequired()])
    note = TextAreaField('备注', validators=[Optional()])
    submit = SubmitField('保存')

class ShoeDeleteForm(FlaskForm):
    number = StringField('鞋号', validators=[DataRequired()])
    type = SelectField('款式', choices=Shoe_Type, coerce=int, default=3)
    size = SelectField('尺码', choices=Shoe_Size, coerce=int)
    count = IntegerField('数量', validators=[DataRequired()])
    note = TextAreaField('备注', validators=[Optional()])
    submit = SubmitField('删除')

class ShoeQueryForm(FlaskForm):
    number = StringField('鞋号', validators=[Optional()])
    name = StringField('鞋名', validators=[Optional()])
    type = SelectField('款式', choices=Shoe_Type, coerce=int, default=3)
    size = SelectField('尺码', choices=Shoe_Size, coerce=int)
    submit = SubmitField('查询')

class ShoeNoteForm(FlaskForm):
    number = StringField('鞋号', validators=[Optional()])
    name = StringField('鞋名', validators=[Optional()])
    type = SelectField('款式', choices=Shoe_Type, coerce=int, default=3)
    size = SelectField('尺码', choices=Shoe_Size, coerce=int)
    note = TextAreaField('备注', validators=[Optional()])
    submit = SubmitField('备注')



