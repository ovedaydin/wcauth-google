from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import jwt_refresh_token_required, jwt_required
from flask_restful.utils import cors

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('password', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('phone_number', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('authorized_store_id', type=int, help="This field cannot be left blank!")
    parser.add_argument('role', type=str, help="This field cannot be left blank!")

    @cors.crossdomain(origin='*')
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_phone_number(data['phone_number']):
            return {"message": "A User with that phone number exists"}, 400

        user = UserModel(**data)  # **data = data['username'],data['password']
        user.save_to_db()

        return {"message": "User created"}, 201


class User(Resource):
    @classmethod
    @cors.crossdomain(origin='*')
    @jwt_refresh_token_required
    def get(cls, phone_number):
        user = UserModel.find_by_phone_number(phone_number)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @cors.crossdomain(origin='*')
    @jwt_required
    def delete(cls, phone_number):
        user = UserModel.find_by_phone_number(phone_number)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'meessage': 'User deleted'}

    parser = reqparse.RequestParser()
    parser.add_argument('authorized_store_id', type=int, required=True, help="This field cannot be left blank!")
    parser.add_argument('role', type=str, required=True, help="This field cannot be left blank!")

    @cors.crossdomain(origin='*')
    @jwt_refresh_token_required
    def put(cls, phone_number):
        data = User.parser.parse_args()
        user = UserModel.find_by_phone_number(phone_number)
        store = data['authorized_store_id']
        if not user:
            return {'message': 'User not found'}, 404
        if not store:
            return {'message': 'Store not found'}, 404
        user.authorized_store_id = data['authorized_store_id']
        user.role = data['role']
        user.save_to_db()
        return {'meessage': 'User updated'}
