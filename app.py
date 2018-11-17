from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

# Constant variables
ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

FASHION_API = "https://fashion.recoqnitics.com/analyze"
FACE_API = "https://face.recoqnitics.com/analyze"

data = {'access_key': ACCESS_KEY,'secret_key': SECRET_KEY}

@app.route('/', methods= ['get'])
def hello():
    output = {"url_list": ['https://shop.iskandar.ml/IMAGES/fashion_20.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_4.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_6.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_7.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_18.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_17.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_15.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_1.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_13.jpg']}

    return jsonify(output)

    # return "Welcome to the best hackathon in the world!!"


@app.route('/find_similar', methods= ['post'])
def find_similar():
    # If nothing is sent
    if not request.json:
        abort(303)

    # Arguments from frontend
#    image_string = request.json["image"]
#    filter = request.json["filter"]

    filename="bryan.jpeg"
    response_fashion = post_fashion(filename)
    response_face = post_face(filename)

    output = {"url_list": ['https://shop.iskandar.ml/IMAGES/fashion_20.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_4.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_6.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_7.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_18.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_17.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_15.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_1.jpg',
                           'https://shop.iskandar.ml/IMAGES/fashion_13.jpg']}


    return jsonify(output)

    # return jsonify(result = request.json)

# Post to recognitive's fashion api
def post_fashion(filename):
    # filename = {'filename': open("test_images/bryan.jpeg", 'rb')}
    filename = {'filename': open("test_images/{}".format(filename), 'rb')}
    r = requests.post(FASHION_API, files=filename, data=data)
    r = str(r.content)[2:-3]
    print(r)
    content = json.loads(r)
    return content

# Post to recognitive's face api
def post_face(filename):
    # filename = {'filename': open("test_images/bryan.jpeg", 'rb')}
    filename = {'filename': open("test_images/{}".format(filename), 'rb')}
    r = requests.post(FACE_API, files=filename, data=data)
    r = str(r.content)[2:-3]
    print(r)
    content = json.loads(r)
    return content

# The closer the age inferred, the stronger the recommendation
def compute_age_score(age, age_query):
    if age_query == "Unknown" or age == "Unknown":
        return 0
    return 1- abs((int(age_query) - int(age)) * 0.1)

# If same gender add 2 to the score, if different add -2. To ensure same gender recommendations
def compute_gender_score(gender, gender_query):
    if gender == "Unknown" or "gender_query" == "Unknown":
        return 0

    if gender == gender_query:
        return 2

    else:
        return -2

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
    app.run("0.0.0.0", debug = True)
    #app.run("0.0.0.0")
