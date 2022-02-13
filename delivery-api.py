from flask import Flask, Response
from flask_restful import Api
from datetime import datetime
from collections import OrderedDict
import json
import operator

app = Flask(__name__)
api = Api(app)

@app.route('/')
def welcome():
    return "<p>Welcome to the delivery API</p>"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')