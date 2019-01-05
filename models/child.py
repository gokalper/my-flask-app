from db import db


class ChildModel(db.Model):

    __tablename__ = 'child'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    is_male = db.Column(db.Boolean)
    dob = db.Column(db.String(9))  #jan052018

    # Back reference the Item table
    moods = db.relationship('MoodModel', lazy='dynamic')    # list of item models many to one relationship
    interactions = db.relationship('InteractionModel', lazy='dynamic')    # list of item models many to one relationship
    toys = db.relationship('ToyModel', lazy='dynamic')    # list of item models many to one relationship
    playground_toys = db.relationship('PlaygroundModel', lazy='dynamic')


    # lazy dynamic makes it a query but doesnt execute

    def __init__(self, first_name, last_name, is_male, dob):
        self.first_name = first_name
        self.last_name = last_name
        self.is_male = is_male
        self.dob = dob

    def json(self):
        return{
            'child_id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_male': self.is_male,
            'dob': self.dob
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, first_name, last_name, dob):
        return cls.query.filter_by(first_name=first_name, last_name=last_name, dob=dob).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()