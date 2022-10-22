from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api
from config import mysql_uri
from db import db


app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_uri
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False


@app.before_first_request
def create_tables():
    db.init_app(app)
    db.create_all()


@app.route('/')
def index():
    return jsonify({
        "status": "ok",
        "message": "Hello World!"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
