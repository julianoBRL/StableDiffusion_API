from flask_restx import Resource
from src.objects.ImageModel import ImageDB
from src.objects.JobModel import JobDB
from src.objects.UserModel import UsersDB
from src.services.Server import server
from flask import Response, jsonify, request
from flask_jwt_extended import jwt_required

app, api = server.app, server.api
api = api.namespace('Gallery', description='Gallery managment')

class GalleryManagment(Resource):
    
    @jwt_required()
    @api.doc('GET user profile')
    @api.response(200, "Images")
    @api.response(401, "Authorization key missing!")
    def get(self):
        resource = request.args.get("image")
        print("ia_viewer")
        with open(f'./images/{resource}', "rb") as f:
            data12 = f.read()
        return Response(response=data12, status=200, mimetype="image/png")
    
class GalleryGetAll(Resource):
    
    @jwt_required()
    @api.doc('GET user profile')
    @api.response(200, "List with all images")
    @api.response(401, "Authorization key missing!")
    def get(self):
        allImages = server.db.session.query(
            ImageDB
        ).filter(
            UsersDB.id == JobDB.created_by,
        ).filter(
            JobDB.id == ImageDB.created_by,
        ).all()
        list_images= []
        for img in allImages:
            list_images.append(img.to_dict())
        return jsonify(list_images)
    
api.add_resource(GalleryManagment, '', endpoint='galery manager')
api.add_resource(GalleryGetAll, '/all', endpoint='complete galley')