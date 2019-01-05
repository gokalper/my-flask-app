from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from models.interaction import InteractionModel

# TODO: Read interaction list from interaction_list table
interaction_list = ['kind', 'playful', 'sharing', 'caring', 'rough', 'hitting']


class Interaction(Resource):
    parser = reqparse.RequestParser()
    for interaction in interaction_list:
        parser.add_argument(interaction,
                            type=bool,
                            required=False
                            )

    @jwt_required
    def get(self, on_date, child_id):
        interaction = InteractionModel.find_by_child_id(on_date, child_id)
        if interaction:
            return interaction.json()
        return {'message': 'Interaction not found'}, 404

    # FIXME: Check if the child_id exists before creating the interaction.
    @fresh_jwt_required
    def post(self, on_date, child_id):
        if InteractionModel.find_by_child_id(on_date, child_id):
            return {'message': "A interaction for child '{}' already exists.".format(child_id)}, 400

        data = Interaction.parser.parse_args()
        interaction = InteractionModel(on_date, child_id, **data)  # expands to interaction['variable1'], interaction['variable2'], etc

        try:
            interaction.save_to_db()
        except:
            return {"message": "An error occurred inserting the Interaction."}, 500

        return interaction.json(), 201 # created

    @jwt_required
    def delete(self, on_date, child_id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        interaction = InteractionModel.find_by_child_id(on_date, child_id)
        if interaction:
            interaction.delete_from_db()
            return({'message': 'Interaction Deleted'}), 202    # deleted

        return({'message': 'Interaction not found'}), 404

    # FIXME: Check if the child_id exists before creating the interaction.
    @jwt_required
    def put(self, on_date, child_id):
        data = Interaction.parser.parse_args()

        interaction = InteractionModel.find_by_child_id(on_date, child_id)

        if interaction is None:
            interaction = InteractionModel(on_date, child_id, **data)  # expands to mood['variable1'], mood['variable2'], etc
        else:
            interaction.kind = data['kind']
            interaction.playful = data['playful']
            interaction.sharing = data['sharing']
            interaction.caring = data['caring']
            interaction.rough = data['rough']
            interaction.hitting = data['hitting']

        interaction.save_to_db()

        return interaction.json()


class InteractionList(Resource):

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        interactions = [interaction.json() for interaction in InteractionModel.find_all()]
        if user_id:
            return {'interactions': interactions}, 200
        return {'message': 'please log in.'}, 200

