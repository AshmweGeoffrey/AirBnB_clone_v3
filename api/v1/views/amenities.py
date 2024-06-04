#!/usr/bin/python3
"""Amenity view module"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = [amenity.to_dict()
                 for amenity in storage.all("Amenity").values()]

    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an amenity based on its amenity_id"""
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity based on its amenity_id"""
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return (jsonify({}))


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates an amenity"""
    data = request.get_json()

    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)

    amenity = Amenity(**data)
    amenity.save()

    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates an amenity based on its amenity_id"""
    amenity = storage.get("Amenity", amenity_id)

    if amenity is None:
        abort(404)

    data = request.get_json()

    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for attr, val in data.items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attr, val)

    amenity.save()

    return jsonify(amenity.to_dict())
