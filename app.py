from flask import Flask, jsonify, request, abort
import requests
import json
import os

app = Flask(__name__)

# Constant variables
ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

FASHION_API = "https://fashion.recoqnitics.com/analyze"
FACE_API = "https://face.recoqnitics.com/analyze"

data = {'access_key': ACCESS_KEY,'secret_key': SECRET_KEY}


@app.route('/find_similar', methods= ['post'])
def find_similar():
    # If nothing is sent
    if not request.json:
        abort(400)

    # Arguments from frontend
    image_string = request.json["image"]
    filter = request.json["filter"]

    filename="bryan.jpeg"
    response = post_data(filename)

    return jsonify(response)

def post_data(filename):
    # filename = {'filename': open("test_images/bryan.jpeg", 'rb')}
    filename = {'filename': open("test_images/{}".format(filename), 'rb')}
    r = requests.post(FASHION_API, files=filename, data=data)
    content = json.loads(r.content)
    return content


if __name__ == '__main__':
    app.run(debug = True)
