import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items

blp = Blueprint("items",__name__, description="Operations on items")
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self,item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404,message = "Item not found")
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message":"item deleted"}, 204
        except KeyError:
            abort(404,message = "Item not found")
        
    def put(self, item_id):
        json_data = request.get_json()
        if "price" not in json_data or "name" not in json_data:
            abort(400, message="Bad request. Ensure 'price' and 'name' are included in the json payload")
        item = items[item_id]
        item |= json_data
        return item
    

@blp.route('/item')
class ItemList(MethodView):
    def get(self):
        return {"stores":list(items.values())}
    def post(self):
        json_dat = request.get_json()
        store_id = uuid.uuid4().hex
        new_store = {**json_dat, "id":store_id}
        items[store_id] = new_store
        return new_store, 201 
    
    
        