from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask('app')

SWAGGER_URL = '/api/docs'  
API_URL = '/static/swagger.json'  

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL,
    config={  
        'app_name': "iContracts application"
    },
)

app.register_blueprint(swaggerui_blueprint)

@app.get('/')
def hello_world():
    return 'Hello, this is the API Rest for iContracts!'

if __name__ == "__main__":
    app.run()