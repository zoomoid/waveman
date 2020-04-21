from flask import Blueprint, request, jsonify
import os

folder = "~/Git/wave-man/uploaded"
extensions = set(['wav', 'mp3'])

api = Blueprint('api', __name__)

#error handler
class Error(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        res = dict(self.payload or ())
        res['message'] = self.message
        return res

# util methods

# checks if filename is valid and the file extension is allowed
def check_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions


@api.route('/image', methods=['POST'])
def convert_image():
    if request.method == 'POST':
        if 'soundfile' not in request.files:
            raise Error('No file was sent', status_code=400)
        file = request.files['soundfile']
        if file.filename = '':
            raise Error('File has no name', status_code=400) # some browsers do that, when no file was selected