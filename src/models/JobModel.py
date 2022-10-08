from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from src.services.Server import server

app, api = server.app, server.api
db = SQLAlchemy(server.app)

class JobDB(db.Model):
    
    __tablename__ = "jobs"
    
    id = db.Column('job_id', db.Integer, primary_key = True, autoincrement=True)
    prompt = db.Column(db.String(100))
    ar = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.now())
    created_by = db.Column(db.Integer)
    
    def __init__(self, prompt, created_by, ar):
        self.prompt = prompt
        self.created_by = created_by
        self.ar = ar
        
db.create_all()
db.session.commit()