import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db

'''
CastingTestCase
    This class represents the casting test case.
'''

pg = "postgresql"
p = "postgres"
l = "localhost:5432"
dbp = "{}://{}:{}@{}/{}"


class CapstoneCastingTestCase(unittest.TestCase):
    def setUp(self):
        # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = dbp.format(pg, p, p, l, self.database_name)
        setup_db(self.app, self.database_path)

        executive_producer_token = os.environ['EXECUTIVE_PRODUCER_TOKEN']
        casting_director_token = os.environ['CASTING_DIRECTOR_TOKEN']
        casting_assistant_token = os.environ['CASTING_ASSISTANT_TOKEN']
        bad_token = os.environ['BAD_TOKEN']

        self.executive_header = {
            "Authorization": "Bearer {}".format(executive_producer_token)
        }

        self.director_header = {
            "Authorization": "Bearer {}".format(casting_director_token)
        }

        self.assistant_header = {
            "Authorization": "Bearer {}".format(casting_assistant_token)
        }

        self.bad_header = {
            "Authorization": "Bearer {}".format(bad_token)
        }

        # This is a sample actor to be used during the test
        # of the insertion endpoint.
        self.new_actor = {
            "name": "Jude Law",
            "age": 47,
            "gender": "M"
        }

        # This is a sample movie to be used during the test
        # of the insertion endpoint.
        self.new_movie = {
            "title": "Pan",
            "release_date": "September 20, 2015"
        }

        # This is a sample actor to be used during the test
        # of the patch endpoint.
        self.updated_actor = {
            "name": "John Malkovich",
            "age": 66,
            "gender": "M"
        }

        # This is a sample movie to be used during the test
        # of the patch endpoint.
        self.updated_movie = {
            "title": "12 Angry Men",
            "release_date": "March 25, 1957"
        }

        # Binds the app to the current context.
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        # Executed after reach test.
        pass

    def test_get_actors(self):
        # Test for successful retrieval of all actors.
        res = self.client().get('/actors', headers=self.executive_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_actors_404_fail(self):
        # bad endpoint.
        res = self.client().get('/actors1', headers=self.executive_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_actors_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().get('/actors', headers=self.bad_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_get_movies(self):
        # Test for successful retrieval of all movies.
        res = self.client().get('/movies', headers=self.executive_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_movies_404_fail(self):
        # bad endpoint.
        res = self.client().get('/movies1', headers=self.executive_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_movies_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().get('/movies', headers=self.bad_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_post_new_actor(self):
        # Test for the successful creation of a new actor.
        res = self.client().post(
            '/actors', headers=self.executive_header, json=self.new_actor
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_post_new_actor_422_fail(self):
        # bad request.
        res = self.client().post(
            '/actors', headers=self.executive_header, json={}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_post_new_actor_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().post(
            '/actors', headers=self.bad_header, json=self.new_actor
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_post_new_movie(self):
        # Test for the successful creation of a new movie.
        res = self.client().post(
            '/movies', headers=self.executive_header, json=self.new_movie
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_post_new_movie_422_fail(self):
        # bad request.
        res = self.client().post(
            '/movies', headers=self.executive_header, json={}
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_post_new_movie_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().post(
            '/movies', headers=self.bad_header, json=self.new_movie
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_patch_actor(self):
        # Test for the successful update of an existing actor.
        res = self.client().patch(
            '/actors/3', headers=self.executive_header, json=self.updated_actor
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_patch_actor_404_fail(self):
        # bad endpoint, not found
        res = self.client().patch(
            '/actors/500', headers=self.executive_header,
            json=self.updated_actor
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_patch_actor_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().patch(
            '/actors/3', headers=self.bad_header, json=self.updated_actor
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_patch_movie(self):
        # Test for the successful update of an existing movie.
        res = self.client().patch(
            '/movies/3', headers=self.executive_header, json=self.updated_movie
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_patch_movie_404_fail(self):
        # bad endpoint, not found
        res = self.client().patch(
            '/movies/500', headers=self.executive_header,
            json=self.updated_movie
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_patch_movie_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().patch(
            '/movies/3', headers=self.bad_header, json=self.updated_movie
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_delete_actor(self):
        # Test for the successful deletion of an actor.
        res = self.client().delete('/actors/5', headers=self.executive_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor_404_fail(self):
        # bad endpoint, not found
        res = self.client().delete(
            '/actors/500', headers=self.executive_header
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().delete('/actors/5', headers=self.bad_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_delete_movie(self):
        # Test for the successful deletion of a movie.
        res = self.client().delete('/movies/5', headers=self.executive_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_404_fail(self):
        # bad endpoint, not found
        res = self.client().delete(
            '/movies/500', headers=self.executive_header
            )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().delete('/movies/5', headers=self.bad_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')


# Make the tests conveniently executable.
if __name__ == "__main__":
    unittest.main()
