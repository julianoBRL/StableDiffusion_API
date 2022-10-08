from datetime import datetime
from src.services.Server import server
from flask_restx import fields

app, api = server.app, server.api

SDPromptModel = api.model('SRPrompt', {
    'prompt': fields.String(required=True, description='prompt used to generate the image'),
    'ar': fields.String(required=False, description='espect ratio')
})
