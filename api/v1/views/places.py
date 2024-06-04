#!/usr/bin/python3
"""Place view module"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects for a specific City"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object based on its place_id"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object based on its place_id"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    place.delete()
    storage.save()

    return (jsonify({}))


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    data = request.get_json()

    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    user = storage.get("User", data['user_id'])

    if user is None:
        abort(404)

    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    data['city_id'] = city_id
    place = Place(**data)
    place.save()

    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """Updates a Place object based on its place_id"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    data = request.get_json()

    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for attr, val in data.items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(place, attr, val)

    place.save()

    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """searches for a place"""
    data = request.get_json()
    if data is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    amenity_objects = [storage.get('Amenity', amenity_id)
                       for amenity_id in amenities
                       if storage.get('Amenity', amenity_id)]

    if not states and not cities:
        places = storage.all('Place').values()
    else:
        places = []
        for state_id in states:
            state = storage.get('State', state_id)
            cities += [city.id for city in state.cities
                       if city.id not in cities]

        for city_id in cities:
            city = storage.get('City', city_id)
            places += city.places

    confirmed_places = []
    for place in places:
        if all(amenity in place.amenities for amenity in amenity_objects):
            confirmed_places.append(place.to_dict())

    return jsonify(confirmed_places)
