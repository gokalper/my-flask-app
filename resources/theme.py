from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    fresh_jwt_required
)
from models.theme import ThemeModel


class Theme(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("week_focus",
                        type=str,
                        required=False
                        )
    parser.add_argument("month",
                        type=int,
                        required=False
                        )
    parser.add_argument("month_theme",
                        type=str,
                        required=False
                        )

    @jwt_required
    def get(self, year, week):
        theme = ThemeModel.find_by_week(year, week)
        if theme:
            return theme.json()
        return {'message': 'Theme for week {} not found'.format(week)}, 404

    @fresh_jwt_required
    def post(self, year, week):
        if ThemeModel.find_by_week(year, week):
            return {'message': "A theme for week '{}' already exists.".format(week)}, 400

        data = Theme.parser.parse_args()
        theme = ThemeModel(year, week, **data)

        try:
            theme.save_to_db()
        except:
            return {"message": "An error occurred inserting the Theme."}, 500

        return theme.json(), 201 # created

    @jwt_required
    def delete(self, year, week):
        claims = get_jwt_claims()

        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        theme = ThemeModel.find_by_week(year, week)
        if theme:
            theme.delete_from_db()
            return({'message': 'Theme Deleted'}), 202    # deleted

        return({'message': 'Theme for week {} not found'.format(week)}), 404

    @jwt_required
    def put(self, year, week):
        data = Theme.parser.parse_args()

        theme = ThemeModel.find_by_week(year, week)

        if theme is None:
            theme = ThemeModel(year, week, **data)
        else:
            theme.week_focus = data['week_focus']
            theme.month = data['month']
            theme.month_theme = data['month_theme']

        theme.save_to_db()

        return theme.json()


class ThemeList(Resource):

    @jwt_required
    def get(self, year):
        theme_list = [theme.json() for theme in ThemeModel.find_theme_by_year(year)]
        return {'Theme List': theme_list}, 200
