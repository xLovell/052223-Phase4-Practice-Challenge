#!/usr/bin/env python3

from models import db, Episode, Guest, Appearance
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/episodes', methods=['GET'])
def episodes():
    episodes = []
    for episode in Episode.query.all():
        episodes.append(episode.to_dict(rules=('-appearances',)))
    return make_response(episodes, 200)

@app.route('/episodes/<int:id>', methods=['GET', 'DELETE'])
def episodes_by_id(id):
    episode = Episode.query.filter(Episode.id == id).first()

    if episode == None:
        return make_response({"error": "Episode not found"}, 404)
    else:
        if request.method == 'GET':
            return make_response(episode.to_dict(), 200)
        elif request.method == 'DELETE':
            db.session.delete(episode)
            db.session.commit()
            return make_response({}, 204)

@app.route('/guests', methods=['GET'])
def guests():
    guests = []
    for guest in Guest.query.all():
        guests.append(guest.to_dict(rules=('-appearances',)))
    return make_response(guests, 200)

@app.route('/appearances', methods=['POST'])
def appearances():
    try:
        appearance = Appearance(
            rating = request.get_json()['rating'],
            episode_id = request.get_json()['episode_id'],
            guest_id = request.get_json()['guest_id']
        )
        db.session.add(appearance)
        db.session.commit()

        return make_response(appearance.to_dict(), 201)
    except ValueError:
        return make_response({"errors": ["validation errors"]}, 400)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
