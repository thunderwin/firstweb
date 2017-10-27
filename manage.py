#encoding: utf-8
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from firstweb import app
from exts import db
from models import User,Question,Answer

manager = Manager(app)
# 使用Migrate 绑定APP 和 DB方便增加数据库表

migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

if __name__ == '__main__':
    manager.run()
