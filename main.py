from flask import Flask
from flask.cli import FlaskGroup
from app import flask_app
from app.plugins import db

import serverless_wsgi

app = Flask(__name__)

app = flask_app

def handler(event, context):
    return serverless_wsgi.handle_request(app, event, context)