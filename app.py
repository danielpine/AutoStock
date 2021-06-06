from flask import (Flask, Response, escape, jsonify,
                   redirect, request, session, url_for)
app = Flask(__name__, static_url_path='')
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stock.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
