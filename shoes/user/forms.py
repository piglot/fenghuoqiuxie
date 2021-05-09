from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Optional

class RoleChangeForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    role = SelectField('用户权限', 
                        choices=[(1, '管理员'), (2, '普通用户')],
                        coerce=int,
                        default=2)
    submit = SubmitField('修改')

class UserDeleteForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    submit = SubmitField('删除')