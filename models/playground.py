from db import db
from datetime import datetime


class PlaygroundModel(db.Model):
    __tablename__ = 'playground'

    id = db.Column(db.Integer, primary_key=True)
    on_date = db.Column(db.String(9))  # JAN012019
    food_truck = db.Column(db.Boolean)
    play_house = db.Column(db.Boolean)
    swing = db.Column(db.Boolean)
    bubble = db.Column(db.Boolean)
    chalk = db.Column(db.Boolean)
    cape = db.Column(db.Boolean)
    ball_hoop = db.Column(db.Boolean)
    bbq_grill = db.Column(db.Boolean)
    food_toy = db.Column(db.Boolean)
    spray_bottle = db.Column(db.Boolean)
    stilt = db.Column(db.Boolean)
    construction_toy = db.Column(db.Boolean)
    jumbo_lego = db.Column(db.Boolean)
    sand_box = db.Column(db.Boolean)
    riding_toy = db.Column(db.Boolean)
    see_saw = db.Column(db.Boolean)
    slide_structure = db.Column(db.Boolean)
    splash_structure = db.Column(db.Boolean)
    sensory_table = db.Column(db.Boolean)
    binocular = db.Column(db.Boolean)

    # Normally linked with joins in SQL but alchemy does it for us
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))  # define foreign key to link items to store
    child = db.relationship('ChildModel')

    def __init__(self, on_date, child_id, food_truck, play_house, swing, bubble, chalk, cape, ball_hoop, bbq_grill, food_toy, spray_bottle, stilt, construction_toy, jumbo_lego, sand_box, riding_toy, see_saw, slide_structure, splash_structure, sensory_table, binocular):

        self.on_date = on_date
        self.child_id = child_id
        self.food_truck = food_truck
        self.play_house = play_house
        self.swing = swing
        self.bubble = bubble
        self.chalk = chalk
        self.cape = cape
        self.ball_hoop = ball_hoop
        self.bbq_grill = bbq_grill
        self.food_toy = food_toy
        self.spray_bottle = spray_bottle
        self.stilt = stilt
        self.construction_toy = construction_toy
        self.jumbo_lego = jumbo_lego
        self.sand_box = sand_box
        self.riding_toy = riding_toy
        self.see_saw = see_saw
        self.slide_structure = slide_structure
        self.splash_structure = splash_structure
        self.sensory_table = sensory_table
        self.binocular = binocular

    def json(self):
        return {
                'playground_id': self.id,
                'on_date': self.on_date,
                'child_id': self.child_id,
                'food_truck': self.food_truck,
                'play_house': self.play_house,
                'swing': self.swing,
                'bubble': self.bubble,
                'chalk': self.chalk,
                'cape': self.cape,
                'ball_hoop': self.ball_hoop,
                'bbq_grill': self.bbq_grill,
                'food_toy': self.food_toy,
                'spray_bottle': self.spray_bottle,
                'stilt': self.stilt,
                'construction_toy': self.construction_toy,
                'jumbo_lego': self.jumbo_lego,
                'sand_box': self.sand_box,
                'riding_toy': self.riding_toy,
                'see_saw': self.see_saw,
                'slide_structure': self.slide_structure,
                'splash_structure': self.splash_structure,
                'sensory_table': self.sensory_table,
                'binocular': self.binocular
                }

    @classmethod
    def find_by_child_id(cls, on_date, child_id):
        return cls.query.filter_by(on_date=on_date, child_id=child_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()