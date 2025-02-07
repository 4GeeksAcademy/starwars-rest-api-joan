"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users,Planets,Films,People,Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_get_users():
    user_list = Users.query.all()
    response_body = {
        "content": user_list
    }
    return jsonify(response_body), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def handle_get_user(user_id):
    user = Users.query.get(user_id)
    response_body = {
        "content": user
    }
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def handle_get_planets():
    planet_list = Planets.query.all()
    response_body = {
        "content": planet_list
    }
    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    response_body = {
        "content": planet
    }
    return jsonify(response_body), 200

@app.route('/films', methods=['GET'])
def handle_get_films():
    film_list = Films.query.all()
    response_body = {
        "content": film_list
    }
    return jsonify(response_body), 200

@app.route('/films/<int:film_id>', methods=['GET'])
def handle_get_film(film_id):
    film = Films.query.get(film_id)
    response_body = {
        "content": film
    }
    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def handle_get_people():
    people_list = People.query.all()
    response_body = {
        "content": people_list
    }
    return jsonify(response_body), 200

@app.route('/people/<int:person_id>', methods=['GET'])
def handle_get_person(person_id):
    person = People.query.get(person_id)
    response_body = {
        "content": person
    }
    return jsonify(response_body), 200


@app.route("/favorites", methods=["GET"])
def get_favorites():
    User_id = 1
    favorites = Favorites.query.filter_by(User_id=User_id).all()
    return jsonify(favorites), 200

@app.route('/favorites/<int:favorite_id>', methods=['GET'])
def handle_get_favorite(favorite_id):
    favorite = Favorites.query.get(favorite_id)
    response_body = {
        "content": favorite
    }
    return jsonify(response_body), 200

@app.route("/favorites", methods=["POST"])
def add_favorite():
    data = request.get_json(force=True)
    required_fields = {"type", "external_ID", "name"}

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    User_id = 1

    new_fav = Favorites(
        external_ID=data["external_ID"],
        type=data["type"],
        name=data["name"],
        User_id=User_id
    )
    db.session.add(new_fav)
    db.session.commit()
    return jsonify(new_fav), 201

@app.route("/favorites/<int:ID>", methods=["DELETE"])
def delete_favorite(ID):
    favorite = Favorites.query.get(ID)
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted successfully"}), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
