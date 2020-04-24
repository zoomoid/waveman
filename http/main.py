from flask import request, jsonify, Flask
import requests
import os
import uuid
from ..src.waveman import WaveMan

app = Flask(__name__)

"""
Expects a POST request with data 
"""
@app.route('/wavify', methods=['POST'])
def wavify():
    if request.method == 'POST':
        data = request.get_json()
        uri = data["uri"]
        response = requests.get(uri)
        filename = str(uuid.uuid4())[0:8]
        with open(f"{filename}.mp3", 'wb') as f:
            f.write(response.content)
            f.close()
        svg = WaveMan(f"{filename}.mp3").to_string()
        os.unlink(f"{filename}.mp3") # cleanup afterwards
        return svg, 200


if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0') # We need to listen on gateway for docker to tunnel correctly