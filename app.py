import os

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import  JWTManager
from flask_restful.utils import cors
from flask_cors import CORS, cross_origin


from resources.user import UserRegister, User
from auth import AUTH, HelloWorld
from resources.address import Address, GetAddress, EffectAdress
from db import db

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)



@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    ret = {
        "msg": "User {} not found".format(identity)
    }
    return ret, 404


api.add_resource(HelloWorld, '/')
api.add_resource(AUTH, '/auth')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<string:phone_number>')
api.add_resource(Address, '/address')
api.add_resource(GetAddress, '/getaddress/<string:phone_number>')
api.add_resource(EffectAdress, '/effectaddress/<int:_id>')

if __name__ == '__main__':
    from db import db

    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run()
