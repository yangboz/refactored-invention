from flask import Flask, jsonify, request

app = Flask(__name__)

# A list to store our "database" of items
items = []

@app.route('/items', methods=['GET'])
def list_items():
    """Returns a list of all items in the database, with links to individual item resources."""
    item_list = []
    for item in items:
        item_dict = {
            'id': item['id'],
            'name': item['name'],
            '_links': {
                'self': f'/items/{item['id']}',
                'update': f'/items/{item['id']}',
                'delete': f'/items/{item['id']}'
            }
        }
        item_list.append(item_dict)
    return jsonify({
        '_links': {
            'self': '/items',
            'create': '/items'
        },
        'items': item_list
    })

@app.route('/items', methods=['POST'])
def create_item():
    """Creates a new item in the database and returns the newly created item resource."""
    data = request.get_json()
    # Generate a unique id for the new item
    new_id = max([item['id'] for item in items]) + 1 if items else 1
    new_item = {
        'id': new_id,
        'name': data['name'],
    }
    items.append(new_item)
    return jsonify({
        '_links': {
            'self': f'/items/{new_id}',
            'update': f'/items/{new_id}',
            'delete': f'/items/{new_id}'
        },
        'item': new_item
    }), 201

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """Returns a single item resource."""
    item = [item for item in items if item['id'] == item_id]
    if not item:
        return '', 404
    item = item[0]
    return jsonify({
        '_links': {
            'self': f'/items/{item_id}',
            'update': f'/items/{item_id}',
            'delete': f'/items/{item_id}'
        },
        'item': item
    })

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """Updates an existing item in the database and returns the updated item resource."""
    data = request.get_json()
    item = [item for item in items if item['

