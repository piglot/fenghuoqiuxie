#! -*- coding:utf-8 -*-
import unittest

from shoes import create_app, db
from shoes.models import User, Shoe

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')

manager = Manager(app)

#使用Migrate绑定app和db
migrate = Migrate(app, db)

def make_shell_context():
    """
    make_shell_context()是一个回调函数

    """
    return dict(app=app, db=db, User=User, Shoe=Shoe)

# make_context回调函数注册了程序、数据库实例以及模型，因此这些对象能直接导入shell
manager.add_command("shell", Shell(make_context=make_shell_context))

#添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

@manager.command
def test():
    """Run the unit tests."""
    tests = unittest.TestLoader().discover('shoes.tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
    #app.run(host='127.0.0.1', port=5000)
