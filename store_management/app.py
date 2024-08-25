import secrets
import os
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask import jsonify

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
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        #check the database if the user is a admin
        if identity == 1:
            return {"is_admin":True}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "message":"The token has expired.","error":"token_exired"
            }),401,
        )
    
    @jwt.invalid_token_loader
    def invalide_token_callback(error):
        return (
            jsonify(
                {
                    "message":"Signature verification failed.", "error":"invalide_token"
                }
            ),401,
        )
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description":"Request does not contain an access token",
                    "error":"authorization_required",
                }
            ),401
        )

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


    @app.before_request
    def Create_table():
        db.create_all()

    api = Api(app)
    api.register_blueprint(ItemBluePrint)
    api.register_blueprint(StoreBluePrint)
    api.register_blueprint(TagBluePrint)
    api.register_blueprint(UserBluePrint)
    
    return app
