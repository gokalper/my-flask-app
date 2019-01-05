from db import db
from datetime import datetime


class MoodModel(db.Model):
    __tablename__ = 'mood'

    id = db.Column(db.Integer, primary_key=True)
    on_date = db.Column(db.String(9))  # JAN012019
    # child_id = db.Column(db.Integer)
    happy = db.Column(db.Boolean)
    helpful = db.Column(db.Boolean)
    silly = db.Column(db.Boolean)
    vocal = db.Column(db.Boolean)
    quiet = db.Column(db.Boolean)
    fussy = db.Column(db.Boolean)
    cranky = db.Column(db.Boolean)
    sad = db.Column(db.Boolean)

    # Normally linked with joins in SQL but alchemy does it for us
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))  # define foreign key to link items to store
    child = db.relationship('ChildModel')

    def __init__(self, on_date, child_id, happy , helpful, silly, vocal, quiet, fussy, cranky, sad):
        self.on_date = on_date
        self.child_id = child_id
        self.happy = happy
        self.helpful = helpful
        self.silly = silly
        self.vocal = vocal
        self.quiet =quiet
        self.fussy = fussy
        self.cranky = cranky
        self.sad =sad

    def json(self):
        return {
                'mood_id': self.id,
                'on_date': self.on_date,
                'child_id': self.child_id,
                'happy': self.happy,
                'helpful': self.helpful,
                'silly': self.silly,
                'vocal': self.vocal,
                'quiet': self.quiet,
                'fussy': self.fussy,
                'cranky': self.cranky,
                'sad': self.sad
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