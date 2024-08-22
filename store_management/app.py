from db import store, items
from flask import Flask, request
from flask_smorest import abort
import uuid

app = Flask(__name__)

@app.get('/store')
def get_store():
    return {"store":list(store.values())}

@app.post('/store')
def create_store():
    json_dat = request.get_json()
    store_id = uuid.uuid4().hex
    new_store = {**json_dat, "id":store_id}
    store[store_id] = new_store
    return new_store, 201 

@app.post('/item')
def create_item():
    json_dat = request.get_json()
    if json_dat["id"] not in store:
        abort(message = "Store not found"), 404
    item_id = uuid.uuid4().hex
    new_item = {**json_dat, "id":item_id}
    items[item_id] = new_item
    return new_item, 201

@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404,message = "Item not found")

@app.get('/item')
def get_items():
    return {"items":list(items.values())}

@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message":"item deleted"}, 204
    except KeyError:
        abort(404,message = "Item not found")

@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del store[store_id] 
        return {"message":"store deleted"}, 204
    except KeyError:
        abort(404,message = "Store not found")

@app.put('/item/<string:item_id>')
def update_item(item_id):
    json_data = request.get_json()
    if "price" not in json_data or "name" not in json_data:
        abort(400, message="Bad request. Ensure 'price' and 'name' are included in the json payload")
    item = items[item_id]
    item |= json_data
    return item 

@app.put('/store/<string:store_id>')
def update_store(store_id):
    json_data = request.get_json()
    if "name" not in json_data or "id" in json_data:
        abort(400,message="Bad request. invalide payload format")
    st = store[store_id]
    st |= json_data
    return st