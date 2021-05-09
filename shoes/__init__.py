from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from config import configs

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()   #db 对象是 SQLAlchemy 类的实例，表示程序使用的数据库，\
                    #同时还获得了 Flask-SQLAlchemy 提供的所有功能

login_manager = LoginManager()
#login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name):
    """
    工厂函数, 接受一个参数，是程序使用的配置名
    """
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(configs[config_name])
    #app.config.from_pyfile('yourconfig.cfg')

    # 初始化
    configs[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # 注册蓝本路由
    from .main import main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    from .user import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app
