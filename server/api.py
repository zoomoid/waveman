from flask import Blueprint, request
import os

folder = "~/Git/wave-man/uploaded"
extensions = set(['wav', 'mp3'])

api = Blueprint('api', __name__)

#util methods

#checks if filename is valid and the file extension is allowed
def check_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

@api.route('/image', methods=['POST'])
def convert_image():
