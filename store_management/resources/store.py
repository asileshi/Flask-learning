import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import StoreModel

blp = Blueprint("store", __name__, description="Oprations on store")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self,store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted successfully"}
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def put(Json_data, store_id):
        store = StoreModel.query.get_or_404(store_id)
        raise NotImplementedError("Update operation not implemented")
@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
            return store
        except IntegrityError:
            abort(400, message="A store with that name already exists")

        except SQLAlchemyError:
            abort(500, message="An error occured creating the Store")