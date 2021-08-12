from flask import render_template
from app import app, db

# @app.errorhandler(404)
# def error_404(error):
#     return render_template('error.html', e=error, fname="assets/404.svg"), 404

# @app.errorhandler(500)
# def error_500(error):
#     return render_template('error.html', e=error, fname="assets/500.svg"), 500

# @app.errorhandler(Exception)
# def some_error(Exception):
#     print(Exception)
#     return render_template('error.html', e=Exception, fname="assets/gen.svg"), 500