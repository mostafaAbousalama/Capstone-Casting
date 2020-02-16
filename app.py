import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import dateutil.parser
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


def date_valid(date_str):
    try:
        validate_date_string = dateutil.parser.parse(date_str)
        # if the dateutil.parser.parse can successfully parse the input date
        # then the next line will run and return True
        return True
    except ValueError:
        # if the dateutil.parser.parse can fails to parse the input date
        return False


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_all_actors(payload):
        selection = Actor.query.all()
        actors = [actor.format() for actor in selection]
        # Abort if there are no actors in the database.
        if len(actors) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'actors': actors
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        try:
            # Get new actor data from request.
            body = request.get_json()
            new_name = body.get('name', None)
            new_age = body.get('age', None)
            new_gender = body.get('gender', None)
            # Validate that all fields are present, if not, abort.
            if (new_name is None) or (new_age is None) or (new_gender is None):
                return abort(422)
            # Validate that the gender is the proper format, if not, abort.
            if (new_gender.upper() != 'M') and (new_gender.upper() != 'F'):
                return abort(422)
            # Format and create the actor object.
            actor = Actor(
                name=new_name, age=new_age, gender=new_gender.upper()
                )
            actor.insert()
            return jsonify({
                'success': True,
                "actor": actor.format()
                })
        except AuthError:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def modify_actor(payload, actor_id):
        try:
            # Find the actor with the given id, if they don't exist abort.
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            # Retrieve the updated actor data.
            body = request.get_json()
            new_name = body.get('name', None)
            new_age = body.get('age', None)
            new_gender = body.get('gender', None)

            # Update the actor with the new values.
            if new_name is not None:
                actor.name = new_name
            if new_age is not None:
                actor.age = new_age
            if new_gender is not None:
                if (new_gender.upper() != 'M') and (new_gender.upper() != 'F'):
                    return abort(422)
                actor.gender = new_gender.upper()
            actor.update()
            return jsonify({"success": True, "actor": actor.format()})
        except AuthError:
            abort(422)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        try:
            # Find the actor with the given id, if they don't exist abort.
            actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            actor.delete()
            return jsonify({"success": True, "delete": actor_id})
        except AuthError:
            abort(422)

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_all_movies(payload):
        selection = Movie.query.all()
        movies = [movie.format() for movie in selection]
        # Abort if there are no movies in the database.
        if len(movies) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'movies': movies
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        try:
            # Get new movie data from request.
            body = request.get_json()
            new_title = body.get('title', None)
            new_release_date = body.get('release_date', None)
            # Validate that all fields are present, if not, abort.
            if (new_title is None) or (new_release_date is None):
                return abort(422)
            # Validate that the inputed date is properly format, if not, abort.
            if not date_valid(new_release_date):
                return abort(422)
            # Format and create the movie object.
            movie = Movie(title=new_title, release_date=new_release_date)

            # Otherwise, create a row in the database for the movie.
            movie.insert()
            return jsonify({
                'success': True,
                "movie": movie.format()
                })
        except AuthError:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def modify_movie(payload, movie_id):
        try:
            # Find the movie with the given id, if it doesn't exist abort.
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            # Retrieve the updated movie data.
            body = request.get_json()
            new_title = body.get('title', None)
            new_release_date = body.get('release_date', None)

            # Update the movie with the new values.
            if new_title is not None:
                movie.title = new_title
            if new_release_date is not None:
                if not date_valid(new_release_date):
                    abort(422)
                movie.release_date = new_release_date
            movie.update()
            return jsonify({"success": True, "movie": movie.format()})
        except AuthError:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        try:
            # Find the movie with the given id, if it doesn't exist abort.
            movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
            if movie is None:
                abort(404)

            movie.delete()
            return jsonify({"success": True, "delete": movie_id})
        except AuthError:
            abort(422)

    # Error handling

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }), 401

    @app.errorhandler(404)
    def not_found(error):
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
    def handle_invalid_usage(error):
        return jsonify({
            "success": False,
            "error": error.error,
            "message": error.status_code
        }), error.error

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
