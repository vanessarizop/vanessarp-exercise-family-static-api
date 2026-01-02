"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from enum import member
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the jackson family object
jackson_family = FamilyStructure("Jackson")


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200


@app.route('/members', methods=['POST'])
def add_member():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'msg': 'The request body is null'}), 400
    jackson_family.add_member(body)
    return jsonify(body), 200


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = jackson_family.delete_member(id)
    if member == None:
        return jsonify({'msg': 'member not found'}), 404
    return jsonify(member), 200

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id): 
    member = jackson_family.get_member(id)
    if member == None:
        return jsonify({'msg': 'member not found'}), 404
    return jsonify(member), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
