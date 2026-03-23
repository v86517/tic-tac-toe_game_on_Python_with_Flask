from flask import Flask

from flask_jwt_extended import JWTManager

from src.web.route.auth_route import *
from src.web.route.game_route import *
from src.di.container import Container

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config["JWT_TOKEN_LOCATION"] = ["headers"] #наверное можно закоментить
    app.config['container'] = Container()

    JWTManager(app)

    app.register_blueprint(auth)

    app.register_blueprint(game_view)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=5000)