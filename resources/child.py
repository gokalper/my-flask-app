from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from models.child import ChildModel

parser = reqparse.RequestParser()
parser.add_argument('first_name',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!"
                    )
parser.add_argument('last_name',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!"
                    )
parser.add_argument('is_male',
                    type=bool,
                    required=True,
                    help="This field cannot be left blank!"
                    )
parser.add_argument('dob',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!"
                    )


class Child(Resource):

    @jwt_required
    def post(self, child_id):

        data = parser.parse_args()

        if ChildModel.find_by_name(data['first_name'], data['last_name'], data['dob']):
            return {"message": "Child with that name already exists."}, 400

        child = ChildModel(**data)

        try:
            child.save_to_db()
        except:
            return {"message": "An error occurred adding the child."}, 500

        return child.json(), 201

    @classmethod
    @jwt_required
    def get(cls, child_id):
        child = ChildModel.find_by_id(child_id)
        if not child:
            return {'message': 'Child not found.'}, 404
        return child.json()

# TODO: Add admin privileges to deleting child
    @classmethod
    @jwt_required
    def delete(cls, child_id):
        child = ChildModel.find_by_id(child_id)
        if not child:
            return {'message': 'Child not found.'}, 404
        child.delete_from_db()
        return {'message': 'Child deleted.'}, 200


class ChildrenList(Resource):

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        children = [child.json() for child in ChildModel.find_all()]
        if user_id:
            return {'children': children}, 200
        return {
            'message': 'no data available unless you log in.',
            'error': 'token expired'
                }, 401


