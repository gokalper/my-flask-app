from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    fresh_jwt_required
)
from models.toy import ToyModel

# TODO: Read toy list from toy_list table
toy_list = ['animal', 'block_lego', 'music_dancing', 'play_set',
            'puppet_doll', 'transportation', 'abc_mouse',
            'puzzle', 'paint', 'play_dough', 'dry_erase',
            'sensory_table', 'dress_up', 'tlc_market',
            'play_food', 'indoor_slide', 'indoor_structure',
            'hoop', 'board_game', 'marker_crayon', 'chalk_board',
            'scissor_glue', 'light_table']


class Toy(Resource):
    parser = reqparse.RequestParser()
    for toy in toy_list:
        parser.add_argument(toy,
                            type=bool,
                            required=False
                            )

    @jwt_required
    def get(self, on_date, child_id):
        toy = ToyModel.find_by_child_id(on_date, child_id)
        if toy:
            return toy.json()
        return {'message': 'Toy not found'}, 404

    # FIXME: Check if the child_id exists before creating the toy.
    @fresh_jwt_required
    def post(self, on_date, child_id):
        if ToyModel.find_by_child_id(on_date, child_id):
            return {'message': "A toy for child '{}' already exists.".format(child_id)}, 400

        data = Toy.parser.parse_args()
        toy = ToyModel(on_date, child_id, **data)  # expands to toy['variable1'], toy['variable2'], etc

        try:
            toy.save_to_db()
        except:
            return {"message": "An error occurred inserting the toy."}, 500

        return toy.json(), 201 # created

    @jwt_required
    def delete(self, on_date, child_id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        toy = ToyModel.find_by_child_id(on_date, child_id)
        if toy:
            toy.delete_from_db()
            return({'message': 'Toy Deleted'}), 202    # deleted

        return({'message': 'Toy not found'}), 404

    # FIXME: Check if the child_id exists before creating the toy.
    @jwt_required
    def put(self, on_date, child_id):
        data = Toy.parser.parse_args()

        toy = ToyModel.find_by_child_id(on_date, child_id)

        if toy is None:
            toy = ToyModel(on_date, child_id, **data)  # expands to mood['variable1'], mood['variable2'], etc
        else:
            toy.animal = data['animal']
            toy.block_lego = data['block_lego']
            toy.music_dancing = data['music_dancing']
            toy.play_set = data['play_set']
            toy.puppet_doll = data['puppet_doll']
            toy.transportation = data['transportation']
            toy.abc_mouse = data['abc_mouse']
            toy.puzzle = data['puzzle']
            toy.paint = data['paint']
            toy.play_dough = data['play_dough']
            toy.dry_erase = data['dry_erase']
            toy.sensory_table = data['sensory_table']
            toy.dress_up = data['dress_up']
            toy.tlc_market = data['tlc_market']
            toy.play_food = data['play_food']
            toy.indoor_slide = data['indoor_slide']
            toy.indoor_structure = data['indoor_structure']
            toy.hoop = data['hoop']
            toy.board_game = data['board_game']
            toy.marker_crayon = data['marker_crayon']
            toy.chalk_board = data['chalk_board']
            toy.scissor_glue = data['scissor_glue']
            toy.light_table = data['light_table']

        toy.save_to_db()

        return toy.json()


class ToyList(Resource):

    @jwt_required
    def get(self):
        toys = [toy.json() for toy in ToyModel.find_all()]
        return {'toys': toys}, 200

