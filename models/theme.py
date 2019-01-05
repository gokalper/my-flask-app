from db import db
from datetime import datetime


class ThemeModel(db.Model):
    __tablename__ = 'theme'

    id = db.Column(db.Integer, primary_key=True)
    week = db.Column(db.Integer)
    week_focus = db.Column(db.String)
    month = db.Column(db.Integer)
    month_theme = db.Column(db.String)
    year = db.Column(db.Integer)

    def __init__(self, year, week, week_focus, month, month_theme):
        self.week = week
        self.week_focus = week_focus
        self.month = month
        self.month_theme = month_theme
        self.year = year

    def json(self):
        return {
                'week': self.week,
                'week_focus': self.week_focus,
                'month': self.month,
                'month_theme': self.month_theme,
                'year': self.year
                }

    @classmethod
    def find_by_week(cls, year, week):
        return cls.query.filter_by(year=year, week=week).first() # SELECT * FROM __tablename__ where child_id = child_id

    @classmethod
    def find_theme_by_year(cls, year):
        return cls.query.filter_by(year=year)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()