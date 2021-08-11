from flask import render_template
from app import app, db

@app.errorhandler(Exception)
def some_error(error):
    if error.code==404:
        return render_template('error.html', e=error, fname="assets/404.svg"), 404
    elif error.code==500:
        return render_template('error.html', e=error, fname="assets/500.svg"), 500
    else:
        return render_template('error.html', e=error, fname="assets/gen.svg"), error.code