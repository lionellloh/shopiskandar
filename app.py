from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import requests
import json
import os
import time
import cv2
import base64
import pickle

print("Loading Dataframe from pickle object")

print("")
app = Flask(__name__)
CORS(app)

# Constant variables
ACCESS_KEY = os.environ['ACCESS_KEY']
SECRET_KEY = os.environ['SECRET_KEY']

FASHION_API = "https://fashion.recoqnitics.com/analyze"
FACE_API = "https://face.recoqnitics.com/analyze"

data = {'access_key': ACCESS_KEY,'secret_key': SECRET_KEY}

def base64_decode_image(data):
    try:
        image_data = bytes(data, 'utf-8')
    except Exception as e:
        print(e)
        image_data = data
    try:
        image_raw = base64.decodebytes(image_data)
    except Exception as e:
        missing_padding = len(image_data) % 4
        if missing_padding != 0:
            image_data += b'=' * (4 - missing_padding)
        image_raw = base64.decodebytes(image_data)
    return image_raw

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
        abort(404)

    # Arguments from frontend
    image_string = request.json["image"]
    filter = request.json[""]
    filename = convert_b64_to_file(image_string)

    response_fashion = post_fashion(filename)
    response_face = post_face(filename)




    return jsonify(output)

    # return jsonify(result = request.json)

# Post to recognitive's fashion api
def post_fashion(filename):
    # filename = {'filename': open("test_images/bryan.jpeg", 'rb')}
    #filename = {'filename': open("test_images/{}".format(filename), 'rb')}
    filename = {'filename': open(filename, 'rb')}
    r = requests.post(FASHION_API, files=filename, data=data)
    r = str(r.content)[2:-3]
    print(r)
    content = json.loads(r)
    return content

# Parse python dictionary to return a list of colours and a list of styles
def parse_fashion(fashion_result):
    try:
        colours = [small_dict["colorGeneralCategory"] for small_dict in fashion_result['person']["colors"]]
        styles = [small_dict["styleName"] for small_dict in fashion_result['person']["styles"]]

    except:
        return None, None

    return colours, styles

# Post to recognitive's face api
def post_face(filename):
    # filename = {'filename': open("test_images/bryan.jpeg", 'rb')}
    #filename = {'filename': open("test_images/{}".format(filename), 'rb')}
    filename = {'filename': open(filename, 'rb')}
    r = requests.post(FACE_API, files=filename, data=data)
    r = str(r.content)[2:-3]
    print(r)
    content = json.loads(r)
    return content


# Parse python dictionary from the face api to return age and gender
def parse_face(face_result):
    try:
        gender = face_result["faces"][0]["gender"]["value"]
        age = face_result["faces"][0]["age"]

    except:
        return None None

    return age, gender


# Given a base64 string, return a file name
def convert_b64_to_file(image_string):
    filename = str(time.time) + ".jpg"
    image_raw = base64_decode_image(image_string)
    image = imread(image_raw)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    cv2.imwrite(filename, image)

    return filename

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
