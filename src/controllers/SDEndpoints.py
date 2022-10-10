from concurrent.futures import thread
from flask_restx import Resource
from src.services.StableDiffusion import stableDiffusion
from src.services.Server import server
from flask import Response, request
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
        resolution = "512x512"
        style = 100

        if "ar" in args: resolution = args["ar"]
        if "style" in args: style = args["style"]

        __add = JobDB(promtp,current_user.id,resolution)
        server.db.session.add(__add)
        server.db.session.commit()
        response = Queue()
        thread = Thread(target=stableDiffusion.generate, args=(args["prompt"],__add.id,response,resolution,style,))
        thread.start()
        thread.join()
        result = response.get()
        with open(f'./images/{result.image_name}', "rb") as f:
            data12 = f.read()
        return Response(response=data12, status=200, mimetype="image/png", headers={"image_id": result.image_id})
        #return result
    
api.add_resource(SDManagment, '', endpoint='StableDiffusion manager')