from flask import Flask
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)
CORS(app)

fb_app = firebase_admin.initialize_app(credentials.Certificate("./.env/creds.json"))

from routes import *

if __name__ == '__main__':
    app.run(debug=True)