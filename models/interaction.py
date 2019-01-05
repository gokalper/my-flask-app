from db import db
from datetime import datetime


class InteractionModel(db.Model):
    __tablename__ = 'interaction'
    id = db.Column(db.Integer, primary_key=True)
    on_date = db.Column(db.String(9))  # JAN012019
    kind = db.Column(db.Boolean)
    playful = db.Column(db.Boolean)
    sharing = db.Column(db.Boolean)
    caring = db.Column(db.Boolean)
    rough = db.Column(db.Boolean)
    hitting = db.Column(db.Boolean)


    # Normally linked with joins in SQL but alchemy does it for us
    child_id = db.Column(db.Integer, db.ForeignKey('child.id'))  # define foreign key to link items to store
    child = db.relationship('ChildModel')

    def __init__(self, on_date, child_id, kind, playful, sharing, caring, rough, hitting):
        self.on_date = on_date
        self.child_id = child_id
        self.kind = kind
        self.playful = playful
        self.sharing = sharing
        self.caring = caring
        self.rough = rough
        self.hitting = hitting


    def json(self):
        return {
                'interaction_id': self.id,
                'on_date': self.on_date,
                'child_id': self.child_id,
                'kind': self.kind,
                'playful': self.playful,
                'sharing': self.sharing,
                'caring': self.caring,
                'rough': self.rough,
                'hitting': self.hitting
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