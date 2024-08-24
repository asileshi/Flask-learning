from models import ItemModel
from db import db
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items",__name__, description="Operations on items")
@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self,item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Get operation not implemented")
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted successfully"}
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, json_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.name = json_data["name"]
            item.price = json_data["price"]
        else:
            item = ItemModel(id = item_id, **json_data)
        db.session
        db.session.commit()
        return item

@blp.route('/item')
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit() 
            return item
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item")

        return item
    
        