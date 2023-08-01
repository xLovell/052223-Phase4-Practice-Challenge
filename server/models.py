from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    number = db.Column(db.Integer)

    appearances = db.relationship("Appearance", cascade="all, delete", backref="episode")
    
    serialize_rules = ("-appearances.episode",)

    def __repr__(self):
        return f'<Episode number: {self.number}>'
    

class Guest(db.Model, SerializerMixin):
    __tablename__ = 'guests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    occupation = db.Column(db.String)

    appearances = db.relationship("Appearance", cascade="all, delete", backref="guest")
    
    serialize_rules = ("-appearances.guest",)

    def __repr__(self):
        return f'<Guest: {self.name}>'
    

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)

    episode_id = db.Column(db.Integer, db.ForeignKey("episodes.id"))
    guest_id = db.Column(db.Integer, db.ForeignKey("guests.id"))
    
    serialize_rules = ("-episode.appearances", "-guest.appearances")
    
    @validates('rating')
    def validate_rating(self, key, rating):
        if not 1 <= rating <5:
            raise ValueError('Invalid rating.')
        return rating
    
    def __repr__(self):
        return f'<Rating: {self.rating}>'
    
# add any models you may need.
