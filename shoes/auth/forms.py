from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

from ..models import User

class LoginForm(FlaskForm):
    #StringField构造函数中的可选参数validators是一个由WTForms内建的验证函数组成的列表，
    #在接受用户提交的数据之前验证数据
    #email = StringField('电子邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')

class RegistrationForm(FlaskForm):
    email = StringField('电子邮箱', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('用户名',
                            validators=[DataRequired(),
                                        Length(1, 64),
                                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                        'Usernames must have only letters,'
                                        'numbers, dots or underscores')]
                            )
    password = PasswordField('密码',
                            validators=[DataRequired(),
                                        EqualTo('password2', message='两次输入的密码必须匹配.')]
                            )
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        """用户自定义的email验证函数"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册.')

    def validate_username(self, field):
        """用户自定义的username验证函数"""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已被使用.')
