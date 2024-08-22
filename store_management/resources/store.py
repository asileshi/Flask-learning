import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import store

blp = Blueprint("store", __name__, description="Oprations on store")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
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
    def put(store_id):
        json_data = request.get_json()
        if "name" not in json_data or "id" in json_data:
            abort(400,message="Bad request. invalide payload format")
        st = store[store_id]
        st |= json_data
        return st

@blp.route('/store')
class StoreList(MethodView):
    def get(self):
        return {"stores":list(store.values())}
    def post(self):
        json_dat = request.get_json()
        store_id = uuid.uuid4().hex
        new_store = {**json_dat, "id":store_id}
        store[store_id] = new_store
        return new_store, 201 
    
        