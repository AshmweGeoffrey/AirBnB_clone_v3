from api.v1.views import app_views
from models import storage
from flask import jsonify
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return {"status": "OK"}
@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    return_dict={
  "amenities": storage.count("Amenity"), 
  "cities": storage.count("City"), 
  "places": storage.count("Place"),
  "reviews": storage.count("Review"),
  "states": storage.count("State"),
  "users": storage.count("User")
}
    return jsonify(return_dict)