"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import bcrypt
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users,Planets,Films,People,Favorites
from flask_jwt_extended import create_access_token, get_csrf_token, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies, get_jwt_identity
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#JWT
app.config["JWT_SECRET_KEY"] = ("super-secret")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_CSRF_IN_COOKIES"] = True
app.config["JWT_COOKIE_SECURE"] = True
 

jwt = JWTManager(app)

MIGRATE = Migrate(app, db)
db.init_app(app)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, supports_credentials=True)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(force=True)
    email = data.get("email")
    password = data.get("password")

    required_fields = ["email", "password"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    existing_user = db.session.query(Users).filter(Users.email == email).first()
    if existing_user:
        return jsonify({"error": "Username or Email already registered"}), 400

    hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    new_user = Users(email=email, password=hashedPassword)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def get_login():
    data = request.get_json(force=True)

    email = data["email"]
    password = data["password"]

    required_fields = ["email", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    user = Users.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found"}), 400

    is_password_valid = bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8'))

    if not is_password_valid:
        return jsonify({"error": "Password not correct"}), 400

    access_token = create_access_token(identity=str(user.id))
    csrf_token = get_csrf_token(access_token)
    response = jsonify({
        "msg": "login successful",
        "user": {
            "id": user.id,
            "email": user.email,
        },
        "csrf_token": csrf_token
        })

    set_access_cookies(response, access_token)

    return response


@app.route("/logout", methods=["POST"])
@jwt_required()
def logout_with_cookies():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

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
