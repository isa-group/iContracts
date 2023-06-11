import os
from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint
from api.predictor.views import predictor
from mongoengine import *
from flask_cors import CORS
from utils.CustomJsonEncoder import CustomJSONEncoder


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

client = connect(host=os.environ.get('MONGODB_URI'))

# Settings
CORS(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "iContracts application"
    },
)


@app.get('/')
def hello_world():
    return 'Hello, this is the API Rest for iContracts!'


app.register_blueprint(swaggerui_blueprint)
app.register_blueprint(predictor, url_prefix='/api/v1')

if __name__ == "__main__":
    app.run()
