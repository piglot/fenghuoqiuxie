from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin

from . import db, login_manager

"""
class Permission:
    QUERY = 1
    COMMENT = 2
    ADD = 4
    DELETE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    #default = db.Column(db.Boolean, default=False, index=True)
    #permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
    #db.relationship() 中的 backref 参数向 User 模型中添加一个 role 属性，从而定义反向关系。
    #这一属性可替代 role_id 访问 Role 模型，此时获取的是模型对象，而不是外键的值。

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def __repr__(self):
        return '<Role %r>' % self.name

    @staticmethod
    def insert_roles():
        roles = {'User': (Permission.QUERY,Permission.COMMENT),
                'Administrator': (Permission.ADMIN,) }
        default_role = 'User'
"""

class User(UserMixin, db.Model):
    # ...
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    #role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.Column(db.Integer, default=2)
    is_admin = db.Column(db.Boolean, default=False)
    is_super_admin = db.Column(db.Boolean, default=False)
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email == current_app.config['FLASKY_SUPER_ADMIN']:
            self.role = 0

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

class Shoe(db.Model):
    __tablename__ = 'shoe'
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64), index=True)
    type = db.Column(db.String(20), index=True)
    size = db.Column(db.String(20), index=True)
    count = db.Column(db.Integer, nullable=False, index=True)
    note = db.Column(db.Text, nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.user_loader
def load_shoes(shoe_id):
    return User.query.get(int(shoe_id))
