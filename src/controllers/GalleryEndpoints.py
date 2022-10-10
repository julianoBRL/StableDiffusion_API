from flask_restx import Resource
from src.objects.ImageModel import ImageDB
from src.objects.JobModel import JobDB
from src.objects.UserModel import UsersDB
from src.services.Server import server
from flask import Response, jsonify, request
from flask_jwt_extended import jwt_required
import io
from PIL import Image
from time import time
from slugify import slugify

app, api = server.app, server.api
api = api.namespace('Gallery', description='Gallery managment')

class GalleryManagment(Resource):
    
    @jwt_required()
    @api.doc('GET user profile')
    @api.response(200, "Images")
    @api.response(401, "Authorization key missing!")
    def get(self):
        resource = request.args.get("image")
        with open(f'./images/{resource}', "rb") as f:
            data12 = f.read()
        return Response(response=data12, status=200, mimetype="image/png")
    
    
class GalleryUpscale(Resource):
    
    @jwt_required()
    @api.doc('GET user profile')
    @api.response(200, "Images")
    @api.response(401, "Authorization key missing!")
    def get(self):
        image_id = int(request.args.get("image_id"))
        grid_opt = int(request.args.get("grid_opt"))
        image = ImageDB.query.filter_by(id=image_id).first()
        im = Image.open(f'./images/{image.uri}')
        
        if "grid" not in image.uri.split('_'):
            return Response(response="not a grid image" ,status=401)
                
        img_out = None
        if grid_opt==1: img_out=im.crop((0, 0, image.ar_width, image.ar_height))
        if grid_opt==2: img_out=im.crop((image.ar_width, 0, image.ar_width*2, image.ar_height))
        if grid_opt==3: img_out=im.crop((0, image.ar_height, image.ar_width, image.ar_height*2))
        if grid_opt==4: img_out=im.crop((image.ar_width, image.ar_height, image.ar_width*2, image.ar_height*2))
        if grid_opt>4 or grid_opt<1:
            return Response(status=401)
        
        image_name = f'{time()}_{slugify(image.prompt[:100])}_grid_{grid_opt}.png'
        
        img_byte_arr = io.BytesIO()
        img_out.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        __image_id = ImageDB(image_name,image.prompt,image_name,image.job_id,int(image.ar_width),int(image.ar_width))
        server.db.session.add(__image_id)
        server.db.session.commit()
        return Response(response=img_byte_arr, status=200, mimetype="image/png")
    
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
api.add_resource(GalleryUpscale, '/upscale', endpoint='image upscaler')