from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    fresh_jwt_required
)
from models.mood import MoodModel

# TODO: Read mood list from mood_list table
mood_list = ['happy', 'helpful', 'silly', 'vocal', 'quiet', 'fussy', 'cranky', 'sad']

class Mood(Resource):
    parser = reqparse.RequestParser()
    for mood in mood_list:
        parser.add_argument(mood,
                            type=bool,
                            required=False
                            )

    @jwt_required
    def get(self, on_date, child_id):
        mood = MoodModel.find_by_child_id(on_date, child_id)
        if mood:
            return mood.json()
        return {'message': 'Mood not found'}, 404

    # FIXME: Check if the child_id exists before creating the item.
    @fresh_jwt_required
    def post(self, on_date, child_id):
        if MoodModel.find_by_child_id(on_date, child_id):
            return {'message': "A mood for child '{}' already exists.".format(child_id)}, 400

        data = Mood.parser.parse_args()
        mood = MoodModel(on_date, child_id, **data)  # expands to mood['variable1'], mood['variable2'], etc

        try:
            mood.save_to_db()
        except:
            return {"message": "An error occurred inserting the Mood."}, 500

        return mood.json(), 201 # created

    @jwt_required
    def delete(self, on_date, child_id):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        mood = MoodModel.find_by_child_id(on_date, child_id)
        if mood:
            mood.delete_from_db()
            return({'message': 'Mood Deleted'}), 202    # deleted

        return({'message': 'Mood not found'}), 404

    # FIXME: Check if the child_id exists before creating the item.
    @jwt_required
    def put(self, on_date, child_id):
        data = Mood.parser.parse_args()

        mood = MoodModel.find_by_child_id(on_date, child_id)

        if mood is None:
            mood = MoodModel(on_date, child_id, **data)  # expands to mood['variable1'], mood['variable2'], etc
        else:
            mood.happy = data['happy']
            mood.helpful = data['helpful']
            mood.silly = data['silly']
            mood.vocal = data['vocal']
            mood.quiet = data['quiet']
            mood.fussy = data['fussy']
            mood.cranky = data['cranky']
            mood.sad = data['sad']

        mood.save_to_db()

        return mood.json()


class MoodList(Resource):

    @jwt_required
    def get(self):
        moods = [mood.json() for mood in MoodModel.find_all()]
        return {'moods': moods}, 200
