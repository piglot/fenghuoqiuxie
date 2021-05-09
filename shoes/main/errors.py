from flask import render_template
from . import main_blueprint


# 如果使用 errorhandler 修饰器，那么只有蓝本中的错误才能触发处理程序
# 要想注册程序全局的错误处理程序，必须使用 app_errorhandler
@main_blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@main_blueprint.app_errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500