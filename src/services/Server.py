from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

SQLALCHEMY_DATABASE_URI = "sqlite:///../../project.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = True
JWT_SECRET_KEY = '8NsezV2QBd'

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

class Server():
    
    def __init__(self,):
        self.app = Flask(__name__)
        self.app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
        self.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
        self.app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
        self.db = SQLAlchemy(self.app)
        self.jwt = JWTManager(self.app)
        self.api = Api(
            self.app,
            title='StableDiffusion API', 
            version='1.0', 
            description='StableDiffusion API',
            prefix='/api/v1/sd',
            authorizations=authorizations,
            security='apikey'
        )
        
    def run(self,):
        self.app.run(debug=True,host='0.0.0.0',port=9000,threaded=True)
        
server = Server()
