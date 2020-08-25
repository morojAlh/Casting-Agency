
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

auth_casting_assistant = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhvdXlNME01Q3VRWEdWV0x3ZHhtViJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LW1oLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjQyYzAyN2IyMzAzMDAwNjcwNTM5ZmIiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNTk4MzkxNDM3LCJleHAiOjE1OTg0Nzc4MzcsImF6cCI6IkI4SXZVRXo0eDAzWkxkZ0pnRXpLZGdXeWZRYnNLNTlPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiXX0.Q09K-FtYjI3bb4AJgzH3nkb5pNdSkYb9hVVK3Dckfm4ZDvGemoQflVOIWEFDVw_13h0hLRhz4nujMPqH-iWVLmp9XdH9uso8cpujsPw3VYqxVaDfOMwEsWI-K6npxqNZ207LnIeGi7VXbjkoLzkyreewzMoO6EKg9n0FEk2AEkfHX-jr8ifDbf1oiH0yIpKZjXoBIJcxmm1sIx4TM3bpwN6qr5yzm_AIM_hvND2yz8oMtDVAKgBmqv7ncJhu7LOjzTiRTgYEmGcoa5CMKQBIcOuXoGU3tOGr6mpM4bcAGCXmivuorXOQO0-PpHX0QXgnn1vfF3gxEXGzZm-dYfcHpQ'
}
# eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhvdXlNME01Q3VRWEdWV0x3ZHhtViJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LW1oLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjQyYzAwMTQ3NjY4MzAwNjdlYjFiMjIiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNTk4MzA3NDM4LCJleHAiOjE1OTgzMTQ2MzgsImF6cCI6IkI4SXZVRXo0eDAzWkxkZ0pnRXpLZGdXeWZRYnNLNTlPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.vKZ2dRdweuzcGT4L6nmY_QTyLWSBvF05_yEjf3zMMVW2n40amPUHDmSuU9UtB9G7RXjHskFc2uVHI2BZu8lgu9UL_ksIMhp5JgTbDtMjCTsF2mmKj4nqHZTTIQ95DsoFonV9HJ5o5maw06CMo5QcHyJ3hj2aE3DUQ9bMcETwcg1OepWY-gI22u-cXN-gSyrReh3foMudc5wBjDieXKztF1lCO9Bc5Weq8eAXrmsm2z3x7PwNuRHyXDTnvgVqjgoNSnYwYiS9D0dpIrYY5SaiXETnXCzJJ0NyYKqosOTzgXMM5ynFTCUIMe9_NbBNmFV42AlBiG6JmPYNtyoodyt-RQ
auth_casting_director = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhvdXlNME01Q3VRWEdWV0x3ZHhtViJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LW1oLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjQyYzAwMTQ3NjY4MzAwNjdlYjFiMjIiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNTk4MzkxMzc4LCJleHAiOjE1OTg0Nzc3NzgsImF6cCI6IkI4SXZVRXo0eDAzWkxkZ0pnRXpLZGdXeWZRYnNLNTlPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.VLnzti0Gt-FLDWfi48JHEzyUF4q3OmyeRh3nCg9bhVTxYkYUFu5V9IOqw7lSw-0w0vewKUwk6Z-qjwWhP5bMgYWikZDR4midLlZIF_qAz9Rzrjg1fG6x_bipkqK-Zc22GcNNDBK9B7HOZDfR5FQqtzjUAGtL7WZaV1d0UPr9dvuOZHLhuQIyPrl4MfmT40IxPtbn8jmAsVZt2nW05SqRm6u2E-yH0uXVRw4jcoDwE2hjvqtzlCX5rjum8hjelw03Unv5iVFa-eUEzv5EgiVrh_X0adm8fpoifRmJlOSWx5YbjMtyQKZy8nkYPZdWneM-oF8zMKlmBrJNzfBQuYgrJg'
}

auth_executive_producer = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhvdXlNME01Q3VRWEdWV0x3ZHhtViJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LW1oLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjQyYmZkMWExYjQxZjAwNjc4MjFiODkiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNTk4MzkxMjI3LCJleHAiOjE1OTgzOTg0MjcsImF6cCI6IkI4SXZVRXo0eDAzWkxkZ0pnRXpLZGdXeWZRYnNLNTlPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.VjPbPnJlqO9cvQciM1g0LUwcVx4KiK0FlZcYHmoaJrNTxxOUatr7voOlIP_bqwHMc-1JqvyXgsUUuvJ6tz0aqldy9LnLNHhrJ1C7O4zP7jTzZzmb7I3Ym3zjOdY2PYrvrBryIjuYN3rEA9cqIYgWVj7WYxPYEaFsnGKqpyqGPQ_rCf5-3hayUFr6Gh1UlrNlDTHhH1PYjeJRq2IC0OL3T8fYQ1Sk1kGS_j8W87Lxc3Q3HyAN1dUVJCWiApV5q5607qhIeDVz-1XY8wPALXiG4V_ZapXbqcX-BHboPbwR0zJq1O1Syp4XhvvVIdjEydIXYUUJUt0lm9vkNJRQ1uZdSQ'
}

class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "casting_agency_test"
        self.database_path = "postgres://postgres@localhost:5432/casting_agency_test"
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'title': 'Joker',
            'release_date': '2019-01-01'
        }

        self.new_actor = {
            'name': 'Brad Pitt',
            'age': 45,
            'gender': 'Male'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass



    # ------ test /movies endpoint ------

    # GET
    def test_get_movies(self):
        res = self.client().get('/movies', headers=auth_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_movies_if_not_authorization(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected')

    # POST 
    def test_add_movies(self):
        res = self.client().post('/movies', headers=auth_executive_producer, json=self.new_movie)
        res = self.client().post('/movies', headers=auth_executive_producer, json=self.new_movie) # for test update & delete
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_401_add_movies_if_access_denied(self):
        res = self.client().post('/movies', headers=auth_casting_director, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'access_denied')
        self.assertEqual(data['description'], 'you do not have permission')

    # PATCH
    def test_update_movies(self):
        res = self.client().patch('/movies/2', headers=auth_casting_director, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_404_update_movies_not_found(self):
        res = self.client().patch('/movies/100', headers=auth_executive_producer, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_update_movies_if_access_denied(self):
        res = self.client().patch('/movies/2', headers=auth_casting_assistant, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'access_denied')
        self.assertEqual(data['description'], 'you do not have permission')

    # DELETE
    def test_delete_movies(self):
        res = self.client().delete('/movies/1', headers=auth_executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delter_movies_not_found(self):
        res = self.client().delete('/movies/100', headers=auth_executive_producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_delete_movies_if_access_denied(self):
        res = self.client().delete('/movies/1', headers=auth_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'access_denied')
        self.assertEqual(data['description'], 'you do not have permission')

    # -----------------------------------


    # ------ test /actors endpoint ------

    # GET
    def test_get_actors(self):
        res = self.client().get('/actors', headers=auth_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_actors_if_not_authorization(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'authorization_header_missing')
        self.assertEqual(data['description'], 'Authorization header is expected')

    # POST 
    def test_add_actors(self):
        res = self.client().post('/actors', headers=auth_casting_director, json=self.new_actor)
        res = self.client().post('/actors', headers=auth_casting_director, json=self.new_actor) # for test update & delete
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_401_add_actors_if_access_denied(self):
        res = self.client().post('/actors', headers=auth_casting_assistant, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'access_denied')
        self.assertEqual(data['description'], 'you do not have permission')

    # PATCH
    def test_update_actors(self):
        res = self.client().patch('/actors/2', headers=auth_casting_director, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_404_update_actors_not_found(self):
        res = self.client().patch('/actors/100', headers=auth_casting_director, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_update_actors_if_access_denied(self):
        res = self.client().patch('/actors/2', headers=auth_casting_assistant, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'access_denied')
        self.assertEqual(data['description'], 'you do not have permission')

    # DELETE
    def test_delete_actors(self):
        res = self.client().delete('/actors/1', headers=auth_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_delter_actors_not_found(self):
        res = self.client().delete('/actors/100', headers=auth_casting_director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_delete_actors_if_access_denied(self):
        res = self.client().delete('/actors/1', headers=auth_casting_assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['code'], 'access_denied')
        self.assertEqual(data['description'], 'you do not have permission')

    # -----------------------------------

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()