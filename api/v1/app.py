from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS
app = Flask(__name__)
app.register_blueprint(app_views, url_prefix="/api/v1")
cors = CORS(app, resources={r"/*": {"origins":"0.0.0.0"}})
@app.errorhandler(404)
def page_not_found(e):
    return {"error": "Not found"}, 404
@app.teardown_appcontext
def close_storage(exception):
    storage.close()
if __name__ == "__main__":
    localhost = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port_way = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=localhost, port=port_way, threaded=True, debug=True)