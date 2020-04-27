from models.address import AddressModel
from flask_restful import Resource, reqparse
from flask_restful.utils import cors
from flask_jwt_extended import jwt_refresh_token_required, jwt_required


class Address(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('country', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('city', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('province', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('line1', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('line2', type=str)
    parser.add_argument('latitude', type=str)
    parser.add_argument('longitude', type=str)
    parser.add_argument('user_phone_number', type=str, required=True, help="This field cannot be left blank!")
    parser.add_argument('address_phone_number', type=str)

    @cors.crossdomain(origin='*')
    @jwt_refresh_token_required
    def post(self):
        data = Address.parser.parse_args()
        address = AddressModel(**data)
        address.save_to_db()
        return {"message": "Address Added"}, 201


class GetAddress(Resource):
    @cors.crossdomain(origin='*')
    @jwt_refresh_token_required
    def get(cls, phone_number):
        addresses = AddressModel.find_by_phone_number(phone_number)
        return {"Addresses": [addresses[x].json() for x in range(len(addresses))]}, 201


class EffectAdress(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('country', type=str)
    parser.add_argument('city', type=str)
    parser.add_argument('province', type=str)
    parser.add_argument('line1', type=str)
    parser.add_argument('line2', type=str)
    parser.add_argument('latitude', type=str)
    parser.add_argument('longitude', type=str)
    parser.add_argument('user_phone_number', type=str)
    parser.add_argument('address_phone_number', type=str)

    @cors.crossdomain(origin='*')
    @jwt_refresh_token_required
    def delete(cls, _id):
        address = AddressModel.find_by_id(_id)
        if not address:
            return {'message': 'Address not found'}, 404
        address.delete_from_db()
        return {'message': 'Address deleted'}
