# coding:utf-8
from config import logger
from web import create_app
from flask_script import Manager, Server

app = create_app('development')

manager = Manager(app)
# 开启多线程
manager.add_command("runserver", Server(threaded=True))

if __name__ == '__main__':
    logger.info("blog run ....")
    app.run()

