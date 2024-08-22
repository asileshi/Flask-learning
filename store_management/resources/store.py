import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

blp = Blueprint("store", __name__, description="Oprations on store")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self,store_id):
        try:
            return store[store_id]
        except KeyError:
            abort(404, message="store not found")
    def delete(self, store_id):
        try:
            del store[store_id]
            return {"mesage":"store delted"}
        except KeyError:
            abort(404,message="store not found")
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def put(Json_data, store_id):
        json_data = request.get_json()
        st = store[store_id]
        st |= json_data
        return st

@blp.route('/store')
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return store.values()
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, json_dat):
        json_dat = request.get_json()
        store_id = uuid.uuid4().hex
        new_store = {**json_dat, "id":store_id}
        store[store_id] = new_store
        return new_store, 201 
    
        