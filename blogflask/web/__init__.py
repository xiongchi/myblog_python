
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

app = Flask(__name__)
db = SQLAlchemy()


def create_app(config_name):
    app.config.from_object(config[config_name])
    db.init_app(app)
    # 项目启动时运行
    with app.test_request_context():
        db.create_all()
        pass
    from web.stock import stock
    app.register_blueprint(stock, url_prefix='/stock')
    return app


