from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    fresh_jwt_required
)
from models.playground import PlaygroundModel

# TODO: Read playground list from playground_list table
playground_list = ['food_truck', 'play_house', 'swing', 'bubble',
                   'chalk', 'cape', 'ball_hoop', 'bbq_grill', 'food_toy',
                   'spray_bottle', 'stilt', 'construction_toy', 'jumbo_lego',
                   'sand_box', 'riding_toy', 'see_saw', 'slide_structure',
                   'splash_structure', 'sensory_table', 'binocular']

class Playground(Resource):
    parser = reqparse.RequestParser()
    for playground in playground_list:
        parser.add_argument(playground,
                            type=bool,
                            required=False
                            )

    @jwt_required
    def get(self, on_date, child_id):
        playground = PlaygroundModel.find_by_child_id(on_date, child_id)
        if playground:
            return playground.json()
        return {'message': 'Playground toys not found'}, 404

    # FIXME: Check if the child_id exists before creating the item.
    @fresh_jwt_required
    def post(self, on_date, child_id):
        if PlaygroundModel.find_by_child_id(on_date, child_id):
            return {'message': "A playground toy for child '{}' already exists.".format(child_id)}, 400

        data = Playground.parser.parse_args()
        playground = PlaygroundModel(on_date, child_id, **data)

        try:
            playground.save_to_db()
        except:
            return {"message": "An error occurred inserting the Playground toys."}, 500

        return playground.json(), 201 # created

    @jwt_required
    def delete(self, on_date, child_id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        playground = PlaygroundModel.find_by_child_id(on_date, child_id)
        if playground:
            playground.delete_from_db()
            return({'message': 'Playground Toys Deleted'}), 202    # deleted

        return({'message': 'Playground Toys not found'}), 404

    # FIXME: Check if the child_id exists before creating the playground toys.
    @jwt_required
    def put(self, on_date, child_id):
        data = Playground.parser.parse_args()

        playground = PlaygroundModel.find_by_child_id(on_date, child_id)

        if playground is None:
            playground = PlaygroundModel(on_date, child_id, **data)
        else:
            playground.food_truck = data['food_truck']
            playground.play_house = data['play_house']
            playground.swing = data['swing']
            playground.bubble = data['bubble']
            playground.chalk = data['chalk']
            playground.cape = data['cape']
            playground.ball_hoop = data['ball_hoop']
            playground.bbq_grill = data['bbq_grill']
            playground.food_toy = data['food_toy']
            playground.spray_bottle = data['spray_bottle']
            playground.stilt = data['stilt']
            playground.construction_toy = data['construction_toy']
            playground.jumbo_lego = data['jumbo_lego']
            playground.sand_box = data['sand_box']
            playground.riding_toy = data['riding_toy']
            playground.see_saw = data['see_saw']
            playground.slide_structure = data['slide_structure']
            playground.splash_structure = data['splash_structure']
            playground.sensory_table = data['sensory_table']
            playground.binocular = data['binocular']

        playground.save_to_db()

        return playground.json()


class PlaygroundList(Resource):

    @jwt_required
    def get(self):
        playground_toys = [playground.json() for playground in PlaygroundModel.find_all()]
        return {'playground_toys': playground_toys}, 200
