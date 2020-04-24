from flask import Blueprint, request, jsonify
import requests
import os

api = Blueprint('api', __name__)

@api.route('/', methods=['POST'])
def convert_to_image():
    if request.method == 'POST':
        data = request.get_json()
        uri = data["uri"]
        response = requests.get(uri)
        with open('soundfile.mp3', 'wb') as f:
            f.write(response.content)
        return "Download successful", 200