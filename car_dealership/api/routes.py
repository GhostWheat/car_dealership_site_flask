from flask import Blueprint, request, jsonify
from car_dealership.helpers import token_required
from car_dealership.models import db, Car, car_schema, allcars_schema

api = Blueprint('api',__name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(our_user):
    return {'some':'value'}

#create Car Endpoint
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(our_user):
    color = request.json['color']
    year = request.json['year']
    make = request.json['make']
    model = request.json['model']
    vin = request.json['vin']
    user_token = our_user.token
    customer_id = request.json['customer id'] #IS THIS THE SAME THING AS USER_TOKEN??

    print(f"User Token: {our_user.token}")

    car = Car(color, year, make, model, vin, user_token, customer_id)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)

#retrieve(READ) all cars
@api.route('/cars', methods = ['GET'])
@token_required
def get_allcars(our_user):
    owner = our_user.token
    drones = Drone.query.filter_by(user_token = owner).all()
    response = allcars_schema.dump(drones)

    return jsonify(response)


#retrieve (READ) only one car
@api.route('/cars', methods = ['GET'])
@token_required
def get_car(our_user, id):
    if id:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'message':'Valid ID Required'}), 401


#UPDATE car by id
@api.route('/cars/<id>', methods = ['PUT'])
@token_required
def update_car(our_user, id):
    car = Car.query.get(id)
    car.color = request.json['color']
    car.year = request.json['year']
    car.make = request.json['make']
    car.model = request.json['model']
    car.vin = request.json['vin']
    car.user_token = our_user.token
    car.customer_id = request.json['customer id'] #IS THIS THE SAME THING AS USER_TOKEN??

    db.session.commit()

    response = car_schema.dump(car)

    return jsonify(response)


#DELETE car by ID
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(our_user, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)
    


