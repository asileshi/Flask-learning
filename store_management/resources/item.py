import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items
from schemas import ItemSchema, ItemUpdateSchema

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
    @blp.arguments(ItemUpdateSchema)
    def put(self, json_data, item_id):
        json_data = request.get_json()
        item = items[item_id]
        item |= json_data
        return item
    

@blp.route('/item')
class ItemList(MethodView):
    def get(self):
        return {"stores":list(items.values())}
    @blp.arguments(ItemSchema)
    def post(self, json_dat):
        store_id = uuid.uuid4().hex
        new_store = {**json_dat, "item_id":store_id}
        items[store_id] = new_store
        return new_store, 201 
    
    
        