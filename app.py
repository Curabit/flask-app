from flask import Flask, render_template

app = Flask(__name__)

# home route
@app.route("/", methods=['GET'])
def index():
    render_template('app.html')

if __name__ == '__main__':
    app.run(debug=True)