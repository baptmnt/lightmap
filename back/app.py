from flask import Flask, jsonify, send_file
from config import Config
# Import models BEFORE db initialization to register metadata
from models import *
from models.db import db
from api import api_bp
from flask_swagger_ui import get_swaggerui_blueprint
from pathlib import Path



import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# Initialiser l'application Flask
app = Flask(__name__)
app.config.from_object(Config)

# Initialiser SQLAlchemy
db.init_app(app)

# Register API blueprint
app.register_blueprint(api_bp)



# Routes
@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Bienvenue sur Flask avec PostgreSQL et SQLAlchemy!'})

# Route pour servir le fichier OpenAPI
@app.route('/api/v1/openapi.yaml', methods=['GET'])
def openapi_spec():
    openapi_path = Path(__file__).parent / 'docs/openapi.yaml'
    return send_file(openapi_path, mimetype='text/yaml')

# Configuration Swagger UI
SWAGGER_URL = '/api/v1/docs'  # URL for exposing Swagger UI
API_URL = '/api/v1/openapi.yaml'  # Our API url

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Lightmap API",
        'layout': 'BaseLayout',
        'deepLinking': True
    }
)

app.register_blueprint(swaggerui_blueprint)



if __name__ == '__main__':
    app.run(debug=True)
