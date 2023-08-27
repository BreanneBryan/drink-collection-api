from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Drink, drink_schema, drinks_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'naw'}

# @api.route('/data')
# def viewdata():
#     data = get_contact()
#     response = jsonify(data)
#     print(response)
#     return render_template('index.html', data = data)

@api.route('/drinks', methods = ['POST'])
@token_required
def create_drink(current_user_token):
    name = request.json['name']
    drink_type = request.json['drink_type']
    flavor_profile = request.json['flavor_profile']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    drink = Drink(name, drink_type, flavor_profile,user_token = user_token  )

    db.session.add(drink)
    db.session.commit()

    response = drink_schema.dump(drink)
    return jsonify(response)

@api.route('/drinks', methods = ['GET'])
@token_required
def get_drink(current_user_token):
    a_user = current_user_token.token
    drinks = Drink.query.filter_by(user_token = a_user).all()
    response = drinks_schema.dump(drinks)
    return jsonify(response)

@api.route('/drinks/<id>', methods = ['GET'])
@token_required
def get_drink_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        drink = Drink.query.get(id)
        response = drink_schema.dump(drink)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/drinks/<id>', methods = ['POST','PUT'])
@token_required
def update_drink(current_user_token,id):
    drink = Drink.query.get(id) 
    print(request)
    drink.name = request.json['name']
    drink.drink_type = request.json['drink_type']
    drink.flavor_profile = request.json['flavor_profile']
    user_token = current_user_token.token

    db.session.commit()
    response = drink_schema.dump(drink)
    return jsonify(response)


# DELETE ENDPOINT
@api.route('/drinks/<id>', methods = ['DELETE'])
@token_required
def delete_drink(current_user_token, id):
    drink = Drink.query.get(id)
    db.session.delete(drink)
    db.session.commit()
    response = drink_schema.dump(drink)
    return jsonify(response)