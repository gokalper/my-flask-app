from ma import ma
from models.theme import ThemeModel


class ThemeSchema(ma.ModelSchema):
    class Meta:
        model = ThemeModel
        dump_only = ('id',)
