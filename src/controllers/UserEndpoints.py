from sqlalchemy.exc import IntegrityError
from flask_restx import Resource
from src.services.Server import server
from src.objects.UserModel import UsersDB, UserModel
from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt

app, api = server.app, server.api
api = api.namespace('User', description='User managment')

# region midlewares

@server.jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@server.jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UsersDB.query.filter_by(id=identity).one_or_none()

# endregion

# region endpoints

class UserRegister(Resource):

    @api.doc('Register user')
    @api.response(201, "User created!")
    @api.response(400, "Missing fields")
    @api.expect(UserModel)
    def post(self):
        try:
            server.db.session.add(UsersDB(api.payload['username'],api.payload['password']))
            server.db.session.commit()
            return None, 201
        except KeyError:
            return None, 400
        except IntegrityError:
            return None, 400

class UserLogin(Resource):

    @api.doc('Login user')
    @api.expect(UserModel)
    @api.response(400, "Missing fields")
    @api.response(404, "User not found")
    @api.response(200, "Authenticated")
    def post(self):
        try:
            user = UsersDB.query.filter_by(username=api.payload['username'], password=api.payload['password']).first()
            access_token = create_access_token(identity=user)
            return jsonify(access_token=access_token)
        except KeyError:
            return None, 400
        except AttributeError:
            return None, 404

class UserLogoff(Resource):
    
    @jwt_required()
    @api.doc('Logoff user')
    @api.response(200, "User logedoff!")
    def get(self):
        jti = get_jwt()["jti"]
        #jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        return jsonify(msg="Access token revoked")

class UserManagment(Resource):
    
    @jwt_required()
    @api.doc('GET user profile')
    @api.response(200, "User profile!")
    @api.response(401, "Authorization key missing!")
    def get(self):
        return jsonify(
            id=current_user.id,
            username=current_user.username,
        )

# endregion

api.add_resource(UserRegister, '/register', endpoint='user_register')
api.add_resource(UserLogin, '/login', endpoint='user_login')
#api.add_resource(UserLogoff, '/logoff', endpoint='user_logoff')
#api.add_resource(UserManagment, '/manage', endpoint='user_manage')
