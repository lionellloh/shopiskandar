from flask import Flask, jsonify, request, abort
import json

app = Flask(__name__)


@app.route('/find_similar', methods= ['post'])
def find_similar():
    # If nothing is sent
    if not request.json:
        abort(400)

    image_string = request.json["image"]
    filter = request.json["filter"]

    print(image_string)
    print(filter)

    return "Success"




if __name__ == '__main__':
    app.run(debug = True)
