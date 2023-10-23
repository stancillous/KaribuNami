from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/home', strict_slashes = False)
def home_page():
    return jsonify('Welcome to Karibu Nami Website!!!')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)