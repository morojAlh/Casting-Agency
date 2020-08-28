import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  # db_drop_and_create_all()


  # ----- Movies -----
  # GET
  @app.route('/movies')
  @requires_auth('get:movie')
  def retrieve_movies(token):
    all_movies = Movie.query.order_by(Movie.id).all()

    movies = []
    for movie in all_movies:
        movies.append(movie.format())

    return jsonify({
      'success': True,
      'movies': movies
    })


  # DELETE
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movie')
  def delete_movie(token,movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)

    movie.delete()

    movies = []
    for movie in Movie.query.order_by(Movie.id).all():
      movies.append(movie.format())

    return jsonify({
      'success': True,
      'movies': movies
    })


  # POST
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movie')
  def create_movie(token):
    body = request.get_json()
    movie = Movie(
      title=body.get('title', None),
      release_date=body.get('release_date', None)
    )
    movie.insert()

    return jsonify({
      'success': True,
      'movie': movie.format(),
    })


  # UPDATE
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movie')
  def update_movie(token, movie_id):
    body = request.get_json()
    
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
      abort(404)

    movie.title = body.get('title')
    movie.release_date = body.get('release_date')

    movie.update()

    return jsonify({
      'success': True,
      'movie': movie.format()
    })



  # ----- Actors -----
  # GET
  @app.route('/actors')
  @requires_auth('get:actor')
  def retrieve_actors(token):
    all_actors = Actor.query.order_by(Actor.id).all()

    actors = []
    for actor in all_actors:
        actors.append(actor.format())
  
    return jsonify({
      'success': True,
      'actors': actors
    })


  # DELETE
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actor')
  def delete_actor(token, actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)

    actor.delete()

    actors = []
    for actor in Actor.query.order_by(Actor.id).all():
        actors.append(actor.format())

    return jsonify({
      'success': True,
      'actors': actors
    })


  # POST
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actor')
  def create_actor(token):
    body = request.get_json()
    
    actor = Actor(
      name=body.get('name', None),
      age=body.get('age', None),
      gender=body.get('gender', None)
    )

    actor.insert()

    return jsonify({
      'success': True,
      'actor': actor.format()
    })


  # UPDATE 
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actor')
  def update_actor(token, actor_id):
    body = request.get_json()

    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
      abort(404)

    actor.name = body.get('name')
    actor.age = body.get('age')
    actor.gender = body.get('gender')

    actor.update()

    return jsonify({
      'success': True,
      'actor': actor.format()
    })



  @app.errorhandler(400)
  def unprocessable(error):
    return jsonify({
          "success": False, 
          "error": 400,
          "message": "bad request"
      }), 400

  @app.errorhandler(404)
  def unprocessable(error):
      return jsonify({
          "success": False, 
          "error": 404,
          "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
          "success": False, 
          "error": 422,
          "message": "unprocessable"
      }), 422


  @app.errorhandler(AuthError)
  def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


  return app

app = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)