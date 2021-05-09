from flask import Blueprint

main_blueprint = Blueprint('main', __name__)    #创建蓝本

from . import views, errors # 导入这两个模块就能把路由和错误处理程序与蓝本关联起来