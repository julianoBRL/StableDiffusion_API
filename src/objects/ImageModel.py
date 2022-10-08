from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from src.services.Server import server
from flask_restx import fields

app, api = server.app, server.api
db = SQLAlchemy(server.app)

class ImageDB(db.Model, SerializerMixin):
    
    __tablename__ = "images"
    
    serialize_only = ('id', 'name', 'uri', 'created_at', 'prompt')
    
    id = db.Column('image_id', db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(100))
    prompt = db.Column(db.String(100))
    uri = db.Column(db.String(50), unique = True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    created_by = db.Column(db.Integer)
   
    def __init__(self, name, prompt, uri, created_by):
        self.name = name
        self.prompt = prompt
        self.uri = uri
        self.created_by = created_by

ImageModel = api.model('Image', {
    'prompt': fields.String(required=True, description='prompt used to generate the image')
})

db.create_all()
db.session.commit()