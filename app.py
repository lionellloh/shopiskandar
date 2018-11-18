from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import requests
import json
import os
import time
import cv2
import base64
import pickle
import copy
from skimage.io import imread


print("Loading Dataframe from pickle object")
df = pickle.load(open("dataframe.pickle","rb"))
print(list(df.columns.values))
print("Dataframe loaded")

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


# Given a base64 string, return a file name
def convert_b64_to_file(image_string):
    filename = "test_images/" + str(time.time()) + ".jpg"
    image_string = bytes(image_string.replace("data:image/jpeg;base64,",""), 'utf-8')
    image_raw = base64_decode_image(image_string)

    with open(filename, "wb") as fh:
        fh.write(image_raw)

    return filename


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
    print(request.json)
    image_string = request.json["image"]
    filter = request.json["filter"]


    print("filter is {}".format(filter))
    print("image is {}".format(image_string))


    filename = convert_b64_to_file(image_string)

    response_fashion = post_fashion(filename)
    response_face = post_face(filename)

    colours, styles = parse_fashion(response_fashion)
    age, gender = parse_face(response_face)
    matches = parse_dataframe(df, filter, age, gender, colours, styles)

    return jsonify({"response": matches})



# Post to recognitive's fashion api
def post_fashion(filename):
    # filename = {'filename': open("test_images/bryan.jpeg", 'rb')}
    #filename = {'filename': open("test_images/{}".format(filename), 'rb')}
    filename = {'filename': open(filename, 'rb')}
    r = requests.post(FASHION_API, files=filename, data=data)
    r = str(r.content)[2:-3]
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

    content = json.loads(r)
    return content


# Parse python dictionary from the face api to return age and gender
def parse_face(face_result):
    try:
        gender = face_result["faces"][0]["gender"]["value"]
        age = face_result["faces"][0]["age"]

    except:
        return None, None

    return age, gender


# The closer the age inferred, the stronger the recommendation
def compute_age_score(age, age_query):
    if age_query == "Unknown" or age == "Unknown":
        return 0

    try:
        return 1- abs((int(age_query) - int(age)) * 0.1)

    except:
        return 0

# If same gender add 2 to the score, if different add -2. To ensure same gender recommendations
def compute_gender_score(gender, gender_query):
    if gender == "Unknown" or "gender_query" == "Unknown":
        return 0

    if gender == gender_query:
        return 2

    else:
        return -2

def compute_match_score(library, article, filter):

    constant = 0.6

    if filter == "Colour":
        constant = 1

    print(library)
    print(article)
    print(set(library) & set(article))
    return len(set(library) & set(article)) * 1.5


def parse_dataframe(df_orig, filter, age, gender, colours, styles):
    df = copy.deepcopy(df_orig)
    df["age_score"] = df["Age"].apply(lambda x: compute_age_score(x, int(age)))
    df["gender_score"] = df["Gender"].apply(lambda x: compute_gender_score(x, gender))

    if filter == 'color':
        df["match_score"] = df["Colour"].apply(lambda x: compute_match_score((x), colours))

    elif filter == 'style':
        df["match_score"] = df["Style"].apply(lambda x: compute_match_score((x), styles))

    df["total_score"] = df["age_score"] + df["match_score"] + df["gender_score"]

    top_nine = df.sort_values(by=["total_score"], ascending=False)[:9]

    return top_nine.to_dict(orient="records")


@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == '__main__':
    app.run("0.0.0.0", debug = True)
    #app.run("0.0.0.0")
