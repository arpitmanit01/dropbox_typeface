from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from blueprints import files_namespace

app = Flask(__name__)

CORS(app)

api = Api(app, version='1.0', title='DropBox_API', description='DropBox API for Typeface Interview')

api.add_namespace(files_namespace)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8080, debug=True)
    except Exception as e:
        app.run(host='localhost', port=8080, debug=True)
