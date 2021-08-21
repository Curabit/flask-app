from app import app
from werkzeug.exceptions import HTTPException, InternalServerError
import os
from flask import url_for
import traceback

@app.route('/')
@app.route('/index')
def index():
    return ""

@app.route('/dashboard')
def dashboard():
    # raise InternalServerError