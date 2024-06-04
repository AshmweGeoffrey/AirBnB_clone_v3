#!/usr/bin/python3
"""Review view module"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.user import User
from models.place import Place


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects for a specific Place"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a review based on its review_id"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a review based on its review_id"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    review.delete()
    storage.save()

    return (jsonify({}))


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a review"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    data = request.get_json()

    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)

    user = storage.get("User", data['user_id'])

    if user is None:
        abort(404)

    if 'text' not in data:
        return make_response(jsonify({'error': 'Missing text'}), 400)

    data['place_id'] = place_id
    review = Review(**data)
    review.save()

    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """Updates a review based on its review_id"""
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for attr, val in data.items():
        if attr not in ['id', 'user_id', 'place_id',
                        'created_at', 'updated_at']:
            setattr(review, attr, val)

    review.save()

    return jsonify(review.to_dict())
