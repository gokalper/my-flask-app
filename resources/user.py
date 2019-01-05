from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be left blank!"
                          )

class UserRegister(Resource):
    TABLE_NAME = 'users'

    def post(self):
        
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        user = UserModel(**data)    # data['username'], data['password']
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class User(Resource):

    @classmethod
    @jwt_required
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        return user.json()

    @classmethod
    @jwt_required
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found.'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200

class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        #get data from parser
        data = _user_parser.parse_args()

        #find user in db
        user = UserModel.find_by_username(data['username'])

        #check password
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)    # a jwtextended function
            refresh_token = create_refresh_token(user.id)
            return{
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }, 200
        
        return {'message': 'Invalid credentials'}, 401

class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti'] #get unique id for the token andblack list that
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}, 200


class TokenRefresh(Resource):

    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access token': new_token}, 200

class UserList(Resource):

    @jwt_required
    def get(self):
        users = [user.json() for user in UserModel.find_all()]
        return {'users': users}, 200


