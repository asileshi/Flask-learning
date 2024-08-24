import secrets
import os
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
import models
from resources.item import blp as ItemBluePrint
from resources.store import blp as StoreBluePrint
from resources.tag import blp as TagBluePrint
from resources.user import blp as UserBluePrint



def create_app(db_url=None):
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "46832766446820110000213922374257060926"
    jwt = JWTManager(app)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Store REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize the SQLAlchemy object
    db.init_app(app)

    with app.app_context():
        db.create_all()

    api = Api(app)
    api.register_blueprint(ItemBluePrint)
    api.register_blueprint(StoreBluePrint)
    api.register_blueprint(TagBluePrint)
    api.register_blueprint(UserBluePrint)
    
    return app
