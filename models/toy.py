from db import db
from datetime import datetime

class ToyModel(db.Model):
    __tablename__ = 'toy'
    id = db.Column(db.Integer, primary_key=True)
    on_date = db.Column(db.String(9))  # JAN012019
    animal = db.Column(db.Boolean)
    block_lego = db.Column(db.Boolean)
    music_dancing = db.Column(db.Boolean)
    play_set = db.Column(db.Boolean)
    puppet_doll = db.Column(db.Boolean)
    transportation = db.Column(db.Boolean)
    abc_mouse = db.Column(db.Boolean)
    puzzle = db.Column(db.Boolean)
    paint = db.Column(db.Boolean)
    play_dough = db.Column(db.Boolean)
    dry_erase = db.Column(db.Boolean)
    sensory_table = db.Column(db.Boolean)
    dress_up = db.Column(db.Boolean)
    tlc_market = db.Column(db.Boolean)
    play_food = db.Column(db.Boolean)
    indoor_slide = db.Column(db.Boolean)
    indoor_structure = db.Column(db.Boolean)
    hoop = db.Column(db.Boolean)
    board_game = db.Column(db.Boolean)
    marker_crayon = db.Column(db.Boolean)
    chalk_board = db.Column(db.Boolean)
    scissor_glue = db.Column(db.Boolean)
    light_table = db.Column(db.Boolean)


    # Normally linked with joins in SQL but alchemy does it for us
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))  # define foreign key to link items to store
    child = db.relationship('ChildModel')

    def __init__(self, on_date, child_id, animal, block_lego, music_dancing, play_set, puppet_doll, transportation, abc_mouse, puzzle, paint, play_dough, dry_erase, sensory_table, dress_up, tlc_market, play_food, indoor_slide, indoor_structure, hoop, board_game, marker_crayon, chalk_board, scissor_glue, light_table):
        self.on_date = on_date
        self.child_id = child_id
        self.animal = animal
        self.block_lego = block_lego
        self.music_dancing = music_dancing
        self.play_set = play_set
        self.puppet_doll = puppet_doll
        self.transportation = transportation
        self.abc_mouse = abc_mouse
        self.puzzle = puzzle
        self.paint = paint
        self.play_dough = play_dough
        self.dry_erase = dry_erase
        self.sensory_table = sensory_table
        self.dress_up = dress_up
        self.tlc_market = tlc_market
        self.play_food = play_food
        self.indoor_slide = indoor_slide
        self.indoor_structure = indoor_structure
        self.hoop = hoop
        self.board_game = board_game
        self.marker_crayon = marker_crayon
        self.chalk_board = chalk_board
        self.scissor_glue = scissor_glue
        self.light_table = light_table


    def json(self):
        return {
                'toy_id': self.id,
                'on_date': self.on_date,
                'child_id': self.child_id,
                'animal': self.animal,
                'block_lego': self.block_lego,
                'music_dancing': self.music_dancing,
                'play_set': self.play_set,
                'puppet_doll': self.puppet_doll,
                'transportation': self.transportation,
                'abc_mouse': self.abc_mouse,
                'puzzle': self.puzzle,
                'paint': self.paint,
                'play_dough': self.play_dough,
                'dry_erase': self.dry_erase,
                'sensory_table': self.sensory_table,
                'dress_up': self.dress_up,
                'tlc_market': self.tlc_market,
                'play_food': self.play_food,
                'indoor_slide': self.indoor_slide,
                'indoor_structure': self.indoor_structure,
                'hoop': self.hoop,
                'board_game': self.board_game,
                'marker_crayon': self.marker_crayon,
                'chalk_board': self.chalk_board,
                'scissor_glue': self.scissor_glue,
                'light_table': self.light_table,
                }

    @classmethod
    def find_by_child_id(cls, on_date, child_id):
        return cls.query.filter_by(on_date=on_date, child_id=child_id).first() # SELECT * FROM __tablename__ where child_id = child_id

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()