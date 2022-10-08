from flask_sqlalchemy import SQLAlchemy
from src.services.Server import server
from flask_restx import fields 

app, api = server.app, server.api
db = SQLAlchemy(server.app)

class UsersDB(db.Model):
    
    __tablename__ = "users"
    
    id = db.Column('user_id', db.Integer, primary_key = True, autoincrement=True)
    username = db.Column(db.String(100), unique = True)
    password = db.Column(db.String(50))
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
UserModel = api.model('User', {
    'username': fields.String(required=True, description='User username'),
    'password': fields.String(required=True, description='User password')
})

db.create_all()
db.session.commit()