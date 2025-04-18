from flask import Flask, render_template
from flask_cors import CORS
from .auth import init_auth_routes 
from .db import init_app
from flask_login import LoginManager

def create_app():
    app = Flask(__name__, static_folder='../static', template_folder='../templates')

    app.config.update(
        SECRET_KEY='dev',
        MYSQL_HOST='localhost',
        MYSQL_PORT=8889,
        MYSQL_USER='root',
        MYSQL_PASSWORD='root',
        MYSQL_DB='Project3',
        MYSQL_UNIX_SOCKET='/Applications/MAMP/tmp/mysql/mysql.sock'
    )

    # 初始化 CORS 和数据库
    CORS(app)
    init_app(app)

    # 初始化登录和 auth 路由
    login_manager = LoginManager()
    login_manager.init_app(app)
    init_auth_routes(app,login_manager)  

    # 前端 vue 静态路由兜底
    @app.route('/')
    @app.route('/<path:path>')
    def index(path=None):
        return render_template("index.html")

    return app
