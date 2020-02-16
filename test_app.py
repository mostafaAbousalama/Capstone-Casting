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

p = "postgres"
l = "localhost:5432"
dbp = "{}://{}:{}@{}/{}"

all_permissions_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5rSXlSVFpHTkVOQk1qTTBOelkwTjBWQk5UZ3hRME5FTVVNME9FVTVORVl4UTBaRFFUa3dRUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1mbTk0ejNiZi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0OTBhOTA3ZWY5YjEwZjA0ZmU5MGFjIiwiYXVkIjoiY29mZmVlU2hvcEFQSUlEIiwiaWF0IjoxNTgxODQ4NTIwLCJleHAiOjE1ODE5MzQ5MjAsImF6cCI6IkNNeWNlc3ZyeXc4UXhnM0hYSzNNTEZCb011N2R6QmxDIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6W119.vQDahhuDZ8cCM2mF2X6SRnePOtCGFfvo2KxgrDpMwQpJvAHRb2yYFh5I926ETLkKpJ4rvJjyjdyUPyNkrkHnIKN7eg3JuCcHS8t-7fb9wQjH-_Eyk_n7UF5CVL0sf-3ZKTsEX4MqLrmZSv6UCYZmqEDEmgCv1pUNbDZFgbjBpNwxQBjbNpIzcy4UQawTsotel0jY9fpLFfLiBEPFN_Yb7_R4bAGz1JXJo9xmOxa0m8g_e0IueiH3W360QS0nU3dAmJcyFyZELruwNxYRoQDoDFLC5f-c6BveOA_SJK1lCC1N2T67MnIcjF0ai8190CdIKa0vSELRpvteZ73pceIitg'

bad_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5rSXlSVFpHTkVOQk1qTTBOelkwTjBWQk5UZ3hRME5FTVVNME9FVTVORVl4UTBaRFFUa3dRUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1mbTk0ejNiZi5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU0NjA3NWY2N2YxYmEwZWJiM2ZiY2RkIiwiYXVkIjoiY29mZmVlU2hvcEFQSUlEIiwiaWF0IjoxNTgxNzc5ODE2LCJleHAiOjE1ODE4NjYyMTYsImF6cCI6Ilp4VXkyb3RrYlJJY2NxOWE0bTduNmZTU2ZieHVRZGpWIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZHJpbmtzIiwiZ2V0OmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIiwicGF0Y2g6ZHJpbmtzIiwicG9zdDpkcmlua3MiXX0.1SEk-RXIcSKP-mqDO66Mp0fAOLM4pIaNnTzn22hzmkxMCDibE_HdG0a0H_C4k1vvKPjYKRK4y17ruI9f_Is_MIwVTQcBK72Qgrf_aQhpW2MzPJ1qxjrpkATJZE7zkgOYAQU4jk6ze9_LGU9BealdkM1D3hQqlFyOns6nvHJyY2YpqtURLMAxBJBM8EThtOwFTUzwtxkpa1CIIYXtYY94IUmKe-edMK5fgRT_bYVybiqk4tEelWte-opLwhVswjdsC4HFuavbF31g4x6pvILLknvR-I8NHH7xYjM3Z6uWT3p0dl99im1zOfX5P3RQNw7QR0ZgOmEHZvtog1XhpIvBIQ'

class CapstoneCastingTestCase(unittest.TestCase):
    def setUp(self):
        # Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = dbp.format(p, p, p, l, self.database_name)
        setup_db(self.app, self.database_path)

        all_permissions_token = os.environ['TEST_TOKEN']
        bad_token = os.environ['BAD_TOKEN']

        self.header = {
            "Authorization": "Bearer {}".format(all_permissions_token)
        }

        self.bad_header = {
            "Authorization": "Bearer {}".format(bad_token)
        }

        # This is a sample actor to be used during the test
        # of the insertion endpoint.
        self.new_actor = {
            "name": "Brad Pitt",
            "birth_date": "December 18, 1963",
            "gender": "M"
        }

        # This is a sample movie to be used during the test
        # of the insertion endpoint.
        self.new_movie = {
            "title": "12 Angry Men",
            "release_date": "March 25, 1957"
        }

        # This is a sample actor to be used during the test
        # of the patch endpoint.
        self.updated_actor = {
            "name": "Jude Law",
            "birth_date": "December 29, 1972",
            "gender": "M"
        }

        # This is a sample movie to be used during the test
        # of the patch endpoint.
        self.updated_movie = {
            "title": "Pan",
            "release_date": "September 20, 2015"
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
        res = self.client().get('/actors', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_actors_404_fail(self):
        # bad endpoint.
        res = self.client().get('/actors1', headers=self.header)
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
        res = self.client().get('/movies', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_movies_404_fail(self):
        # bad endpoint.
        res = self.client().get('/movies1', headers=self.header)
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
        res = self.client().post('/actors', headers=self.header, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_post_new_actor_422_fail(self):
        # bad request.
        res = self.client().post('/actors', headers=self.header, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_post_new_actor_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().post('/actors', headers=self.bad_header, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_post_new_movie(self):
        # Test for the successful creation of a new movie.
        res = self.client().post('/movies', headers=self.header, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_post_new_movie_422_fail(self):
        # bad request.
        res = self.client().post('/movies', headers=self.header, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_post_new_movie_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().post('/movies', headers=self.bad_header, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_patch_actor(self):
        # Test for the successful update of an existing actor.
        res = self.client().patch('/actors/1', headers=self.header, json=self.updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actor']))

    def test_patch_actor_404_fail(self):
        # bad endpoint, not found
        res = self.client().patch('/actors/500', headers=self.header, json=self.updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_patch_actor_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().patch('/actors/5', headers=self.bad_header, json=self.updated_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_patch_movie(self):
        # Test for the successful update of an existing movie.
        res = self.client().patch('/movies/3', headers=self.header, json=self.updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movie']))

    def test_patch_movie_404_fail(self):
        # bad endpoint, not found
        res = self.client().patch('/movies/500', headers=self.header, json=self.updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_patch_movie_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().patch('/movies/6', headers=self.bad_header, json=self.updated_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_delete_actor(self):
        # Test for the successful deletion of an actor.
        res = self.client().delete('/actors/5', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actor_404_fail(self):
        # bad endpoint, not found
        res = self.client().delete('/actors/500', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().delete('/actors/1', headers=self.bad_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')

    def test_delete_movie(self):
        # Test for the successful deletion of a movie.
        res = self.client().delete('/movies/2', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movie_404_fail(self):
        # bad endpoint, not found
        res = self.client().delete('/movies/500', headers=self.header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie_401_fail(self):
        # unauthorized, permission not granted
        res = self.client().delete('/movies/2', headers=self.bad_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unauthorized')


# Make the tests conveniently executable.
if __name__ == "__main__":
    unittest.main()
