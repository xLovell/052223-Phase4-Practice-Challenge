from app import app
from models import db, Episode, Guest, Appearance
from random import randint
from faker import Faker


class TestApp:
    '''Flask application in app.py'''

    def test_gets_episodes(self):
        '''retrieves episodes with GET requests to /episodes.'''

        with app.app_context():
            Episode.query.delete()
            db.session.commit()

            e1 = Episode(date='1/1/2000', number=randint(1000, 2000))
            e2 = Episode(date='1/1/2000', number=randint(1000, 2000))
            db.session.add_all([e1, e2])
            db.session.commit()

            response = app.test_client().get('/episodes')
            episodes = Episode.query.all()

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json

            assert [episode['id'] for episode in response] == [
                episode.id for episode in episodes]
            assert [episode['date'] for episode in response] == [
                episode.date for episode in episodes]
            assert [episode['number'] for episode in response] == [
                episode.number for episode in episodes]
            for episode in response:
                assert 'appearances' not in episodes

    def test_gets_episode_by_id(self):
        '''retrieves one episode using its ID with GET request to /episodes/<int:id>.'''

        with app.app_context():
            e = Episode(date='1/2/2000', number=randint(1000, 2000))
            db.session.add(e)
            db.session.commit()

            response = app.test_client().get(f'/episodes/{e.id}')

            assert response.status_code == 200
            assert response.content_type == 'application/json'
            response = response.json

            assert response['id'] == e.id
            assert response['date'] == e.date
            assert response['number'] == e.number
            assert response['appearances']

    def test_returns_404_if_no_episode_to_get(self):
        '''returns an error message and 404 status code with GET request to /episodes/<int:id> by a non-existent ID.'''

        with app.app_context():
            response = app.test_client().get('/episodes/0')
            assert response.status_code == 404
            assert response.content_type == 'application/json'
            assert response.json.get('error') == 'Episode not found'
            assert response.status_code == 404

    def test_deletes_episode(self):
        '''deletes one episode using its ID with DELETE request to /episodes/<int:id>.'''

        with app.app_context():
            episode = Episode(date='1/3/2000', number=3)
            db.session.add(episode)
            db.session.commit()

            response = app.test_client().delete(f'/episodes/{episode.id}')

            assert response.status_code == 204

            result = Episode.query.filter(
                Episode.id == episode.id).one_or_none()
            assert result is None

    def test_returns_404_if_no_episode_to_delete(self):
        '''returns an error message and 404 status code with DELETE request to /episodes/<int:id> by a non-existent ID.'''

        with app.app_context():
            response = app.test_client().get('/episodes/0')
            assert response.status_code == 404
            assert response.json.get('error') == "Episode not found"

    def test_gets_guests(self):
        '''retrieves guests with GET requests to /guests.'''

        with app.app_context():
            fake = Faker()
            guest1 = Guest(name=fake.name(), occupation=fake.sentence())
            guest2 = Guest(name=fake.name(), occupation=fake.sentence())

            db.session.add_all([guest1, guest2])
            db.session.commit()

            response = app.test_client().get('/guests').json
            guests = Guest.query.all()
            assert [guest['id']
                    for guest in response] == [guest.id for guest in guests]
            assert [guest['name']
                    for guest in response] == [guest.name for guest in guests]
            assert [guest['occupation'] for guest in response] == [
                guest.occupation for guest in guests]
            for guest in response:
                assert 'appearances' not in guest

    def test_creates_appearance(self):
        '''creates appearances with POST requests to /appearances.'''

        with app.app_context():

            fake = Faker()
            e1 = Episode(date='1/1/2000', number=randint(1000, 2000))
            g1 = Guest(name=fake.name(),
                       occupation=fake.sentence())
            db.session.add_all([e1, g1])
            db.session.commit()

            response = app.test_client().post(
                '/appearances',
                json={
                    'rating': 1,
                    'episode_id': e1.id,
                    'guest_id': g1.id,
                }
            )

            assert response.status_code == 201
            assert response.content_type == 'application/json'
            response = response.json
            assert response['rating'] == 1
            assert response['episode_id'] == e1.id
            assert response['guest_id'] == g1.id
            assert response['episode']
            assert response['guest']

            appearance = Appearance.query.filter(
                Appearance.id == response['id']).one_or_none()
            assert appearance.rating == 1
            assert appearance.episode == e1
            assert appearance.guest == g1
