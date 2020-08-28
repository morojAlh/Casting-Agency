
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

auth_casting_assistant = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhvdXlNME01Q3VRWEdWV0x3ZHhtViJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LW1oLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjQyYzAyN2IyMzAzMDAwNjcwNTM5ZmIiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNTk4NTcyOTkyLCJleHAiOjE1OTg2NTkzOTIsImF6cCI6IkI4SXZVRXo0eDAzWkxkZ0pnRXpLZGdXeWZRYnNLNTlPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiXX0.LaOE7Nj8fRZGmNSt5d85Z49fV1bkmsKEtymr405UqF_Q6MGAI2SZKWWtWrcN1pLNEZ999pnN7MMzfpzQ6iF08kgbJYsMFrnSaK2qeZPXpOyzQjGz_NLCLT8_GeZHAFMROLIqmuARadDOs2W8JdgKDI00WNmOaBP7R4uN-Lfi0CCRtI03skcT_aArcrbHtL4sLl6OojyF08mhIuGF4L3fBZ8S2AlkuKQr8Ac7ztSQW15OFiSU8chQFLY-9ubBnBw8e8487ug4xub2uZhev9LDh1uo8cn9XWjB4eh-qRGedRmnGiT5VINH3LK0U-PI2iLy4QxOMUY_B16OYtsHIZE59w'
}
auth_casting_director = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhvdXlNME01Q3VRWEdWV0x3ZHhtViJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LW1oLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjQyYzAwMTQ3NjY4MzAwNjdlYjFiMjIiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNTk4NTczMDM0LCJleHAiOjE1OTg2NTk0MzQsImF6cCI6IkI4SXZVRXo0eDAzWkxkZ0pnRXpLZGdXeWZRYnNLNTlPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.UXz0pewG70Ak8P4ZKfyPo0VgalhENzKsBf0RsFHLirQAneM0XWJwoCfhXGUhZO3YAB_9gS982NbpaFjQBc9JcpHFZoCJc-a9JU4fj-sUzzzuCdOkPV5R2LzXj6ZG6q5N8Gs0GemecPxVJ_08P4s18KJzmyDgQEBCgGeVbM-R4XsRo_Yig3FN-FCj5Om_g560LKFgd9tUbfs6qHVF15hvGY8qkLtQyjh6KuQD_mQdlyWeJNdCpTMZ6mFYhN_tnveJkguTNbAdUn4fwGWn5nSRngYQErKfyEghYQYvfCbpFLKRH6zt_9LBAyPCtDi3UGPbP6jLa4XGU9NL4dSlE3U2rw'
}

auth_executive_producer = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjhvdXlNME01Q3VRWEdWV0x3ZHhtViJ9.eyJpc3MiOiJodHRwczovL2Nhc3RpbmctYWdlbmN5LW1oLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjQyYmZkMWExYjQxZjAwNjc4MjFiODkiLCJhdWQiOiJjYXN0aW5nYWdlbmN5IiwiaWF0IjoxNTk4NTcyNjYwLCJleHAiOjE1OTg2NTkwNjAsImF6cCI6IkI4SXZVRXo0eDAzWkxkZ0pnRXpLZGdXeWZRYnNLNTlPIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJnZXQ6YWN0b3IiLCJnZXQ6bW92aWUiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.cVC9Nb2_UqDzrIGzat4BboWo-L0nYgdsZ5sIbxDWde79pmCzHdSsHom3lLijE0s_I8JSia1BM1CaQQid3HQSvN931yR8NOZd1Ebca1gW-maemeNaJBvXDOz_dB0BaiYMW1MCBHTWcBB5kiNKCPj3oca_2kgY_Hv0rrAIkMj-9v4GwhzUnUxHYvUIt7Lp3e2lPkNz2TGaII3Hzi0UebBIic_lnD3RMl23NyEKvx2FEDVPojSVLwmM8YEiS-9VvBveuem6gM38zXFlPKHrc3aNbBAAfZTQb-KCJ6bqYU1bshT7w0djfe3jinZafOaqpY4UUMBBvArs9M2NlcgdG-CGMw'
}

class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
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