from flask import Flask, request
from flask import Blueprint
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api
from flask import make_response
from json import dumps
from flask_jsonpify import jsonify
from flask import send_file, url_for

from resources.gallery import Image, Gallery

app = Flask(__name__, static_folder='public/collages')
api_bp = Blueprint('api', __name__)
api = Api(api_bp)
app.register_blueprint(api_bp, url_prefix='/api')

# app.static_url_path='/public/collages'

# # set the absolute path to the static folder
# app.static_folder=app.root_path + app.static_url_path

# print(app.static_url_path)
print(app.root_path)

CORS(app)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

api.add_resource(Image, '/gallery/<image_name>') # Route_1
api.add_resource(Gallery, '/gallery') # Route_1



if __name__ == '__main__':
    app.run(port=5002)
