from ma import ma
from models.child import ChildModel
from models.mood import MoodModel
from schemas.mood import MoodSchema


class ChildSchema(ma.ModelSchema):
    theme = ma.Nested(MoodSchema, many=True)

    class Meta:
        model = ChildModel
        dump_only = ('id',)
        include_fk = True   # include foreign keys in the dump
