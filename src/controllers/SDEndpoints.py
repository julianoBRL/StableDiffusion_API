from concurrent.futures import thread
from flask_restx import Resource
from src.services.StableDiffusion import stableDiffusion
from src.services.Server import server
from flask import request
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from src.objects.JobModel import JobDB
from threading import Thread
from queue import Queue

app, api = server.app, server.api
api = api.namespace('StableDiffusion', description='StableDiffusion managment')

class SDManagment(Resource):
    
    @jwt_required()
    @api.doc('Generate new image')
    @api.response(401, "Authorization key missing!")
    def get(self):
        args = request.args
        
        promtp = args["prompt"]
        resolution = args["ar"] if not None else "512x512"
        style = args["style"]
        
        __add = JobDB(promtp,current_user.id,resolution)
        server.db.session.add(__add)
        server.db.session.commit()
        response = Queue()
        thread = Thread(target=stableDiffusion.generate, args=(args["prompt"],__add.id,response,resolution,), daemon=True)
        thread.start()
        thread.join()
        result = response.get()
        return result
    
api.add_resource(SDManagment, '', endpoint='StableDiffusion manager')