from ma import ma
from models.mood import MoodModel


class MoodSchema(ma.ModelSchema):
    class Meta:
        model = MoodModel
        dump_only = ('id',)
        include_fk = True   # include foreign keys in the dump