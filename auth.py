from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import (create_access_token,
                                jwt_refresh_token_required, create_refresh_token,
                                get_jwt_identity
                                )
from datetime import timedelta
from models.user import UserModel
from flask_restful.utils import cors

class HelloWorld(Resource):
    @cors.crossdomain(origin='*')
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        print(current_user)
        new_token = create_access_token(identity=current_user, fresh=False)
        ret = {'access_token': new_token}
        return ret, 200


class AUTH(Resource):
    @cors.crossdomain(origin='*')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone_number', type=str, help='Rate to charge for this resource')
        parser.add_argument('password', type=str, help='Rate to charge for this resource')
        data = parser.parse_args()

        if not data['phone_number']:
            return {"msg": "Missing username parameter"}, 400
        if not data['password']:
            return {"msg": "Missing password parameter"}, 400
        user = UserModel.find_by_phone_number(data['phone_number'])
        if data['password'] != user.password:
            return {"msg": "Bad username or password"}, 401
        expires = timedelta(minutes=30)
        access_token = create_access_token(identity=user.json(), expires_delta=expires)
        refresh_token = create_refresh_token(identity=user.json())
        return {'access_token': access_token, 'refresh_token': refresh_token}, 200
