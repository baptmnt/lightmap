from flask import Flask, jsonify
from config import Config
# Import models BEFORE db initialization to register metadata
from models import *
from models.db import db



import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# Initialiser l'application Flask
app = Flask(__name__)
app.config.from_object(Config)

# Initialiser SQLAlchemy
db.init_app(app)



# Routes
@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Bienvenue sur Flask avec PostgreSQL et SQLAlchemy!'})




if __name__ == '__main__':
    app.run(debug=True)
