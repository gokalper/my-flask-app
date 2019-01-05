import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh, UserList
from resources.mood import Mood, MoodList
from resources.theme import Theme, ThemeList
from resources.interaction import Interaction, InteractionList
from resources.toy import Toy, ToyList
from resources.child import Child, ChildrenList
from resources.playground import Playground, PlaygroundList
from blacklist import BLACKLIST

from fileupload.upload import appUpload

heroku_db_url = os.environ.get('DATABASE_URL')
sqlite_url = 'sqlite:///data.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # flask-sqlalchemy setting
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.register_blueprint(appUpload)
# app.config['JWT_SECRET_KEY'] = 'jose' # jwt extended config 
app.secret_key = 'jose' 
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims(identity):
    if identity == 1: # read from config file rather than hard coding
        return({'is_admin': True,})
    return({'is_admin': False,})

# Returns true if jti in the blacklist, false if it is not in the blacklist
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST
    

# Token expired every 5 minutes or so, when they try again they will get this message
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401

# When Authorization string is not a JWT, and is a different string or when token is not fresh....why?
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401

# When no JWT is sent at all
@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'no_token'
    }), 401

# When a non fresh token is sent and a fresh is required...does not work as expected...why?
@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh, please login again.',
        'error': 'non_fresh_token'
    }), 401

# When a token is revoked, ie user logs out token is added to revoked token list
@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token is revoked, please login again.',
        'error': 'revoked_token'
    }), 401


api.add_resource(Theme, '/theme/<int:year>/<int:week>')
api.add_resource(Mood, '/mood/<string:on_date>/<int:child_id>')
api.add_resource(Interaction, '/interaction/<string:on_date>/<int:child_id>')
api.add_resource(Toy, '/toy/<string:on_date>/<int:child_id>')
api.add_resource(Playground, '/playground/<string:on_date>/<int:child_id>')
api.add_resource(Child, '/child/<int:child_id>')
api.add_resource(ChildrenList, '/children')
api.add_resource(ThemeList, '/theme_list/<int:year>')
api.add_resource(MoodList, '/moods')
api.add_resource(InteractionList, '/interactions')
api.add_resource(ToyList, '/toys')
api.add_resource(PlaygroundList, '/playground_toys')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserList, '/users')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(UserLogout, '/logout')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5005, debug=True)  # important to mention debug=True
