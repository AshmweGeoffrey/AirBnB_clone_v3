#!/usr/bin/python3
"""City view module"""

from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects for a specific State"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]

    return jsonify(cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object based on its city_id"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object based on its city_id"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    city.delete()
    storage.save()

    return (jsonify({}))


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a City"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    data = request.get_json()

    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    data['state_id'] = state_id
    city = City(**data)
    city.save()

    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Updates a City object based on its city_id"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for attr, val in data.items():
        if attr not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, attr, val)

    city.save()

    return jsonify(city.to_dict())
