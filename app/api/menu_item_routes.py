import json
from flask_login import login_required
from flask import Blueprint, jsonify,request
from app.forms import MenuItemForm
from app.models import db, MenuItem
from app.api.aws import (upload_file_to_s3, get_unique_filename)

menu_items_routes = Blueprint('menu-items', __name__)


@menu_items_routes.route('/')
def menu_items():
    menu_items = MenuItem.query.all()

    return json.dumps({'menuItems': [menu_item.to_dict() for menu_item in menu_items]})


@menu_items_routes.route('/<int:menuItemId>')
def get_menu_item(menuItemId):
    menu_item = MenuItem.query.filter(MenuItem.id == menuItemId).all()

    if not menu_item:
        return jsonify({'message': 'No menu item with that id'}), 404

    return jsonify({ 'menuItemId': menu_item[0].to_dict()['restaurant_id'] })

#get all the menu items for each restaurant
@menu_items_routes.route('/restaurants/<int:restaurantId>')
def menu_items_by_restaurant_id(restaurantId):
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurantId).all()

    if not menu_items:
        return jsonify({'message': 'Restaurant has no menu items'}), 404

    return json.dumps({'menuItems': [menu_item.to_dict() for menu_item in menu_items]})

#create new menu item
@menu_items_routes.route('/restaurants/<int:restaurantId>', methods=['POST'])
def create_menu_item(restaurantId):
    form = MenuItemForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    image_file = request.files.get('image')
    upload = upload_file_to_s3(image_file)

    if 'url' not in upload:
        return upload

    name = request.form.get('name')
    price = request.form.get('price')
    calories = request.form.get('calories')

    new_menu_item = MenuItem(
        restaurant_id=restaurantId,
        name=name,
        price=price,
        image=upload["url"],
        calories=calories
    )

    db.session.add(new_menu_item)
    db.session.commit()

    res = new_menu_item.to_dict()
    return json.dumps(res), 201


#update route
@menu_items_routes.route('/<int:id>', methods=['PUT'])
def update_menu_item(id):
    menu_item = MenuItem.query.get(id)

    if not menu_item:
        return json.dumps({'message': 'Menu Item not found'}), 404

    form = MenuItemForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    name = request.form.get('name')
    price = request.form.get('price')
    calories = request.form.get('calories')
    image_file = request.files.get('image')

    if image_file:
        upload = upload_file_to_s3(image_file)
        menu_item.image=upload['url']

    menu_item.name=name
    menu_item.price=price
    menu_item.calories=calories
    db.session.commit()

    res = menu_item.to_dict()
    return json.dumps(res)


@menu_items_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_menu_item(id):
    menu_item = MenuItem.query.get(id)
    if menu_item:
        db.session.delete(menu_item)
        db.session.commit()
        return json.dumps({'message': 'Menu Item deleted successfully'}), 200

    return json.dumps({'message': 'Menu Item not found'}), 404
