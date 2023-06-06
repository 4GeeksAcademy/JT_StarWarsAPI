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
from models import db, User, People, Planet, FavoritePeople, FavoritePlanet
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

# my enpoints here

@app.route('/user', methods=['GET'])
def get_user():

    users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), users))
    return jsonify(all_users), 200 

@app.route('/user', methods=['POST'])
def create_user():
    request_body_user = request.get_json()

    new_user = User(email=request_body_user["email"], password=request_body_user["password"])
    db.session.add(new_user)
    db.session.commit()

    return jsonify(request_body_user), 200 

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):

    user1 = User.query.get(user_id)
    if user1 is None:
        raise APIException("User not found", status_code=404)
    db.session.delete(user1)
    db.session.commit()

    return jsonify("ok"), 200 


@app.route('/people', methods=['GET'])
def get_people():

    people = People.query.all()
    all_people = list(map(lambda x: x.serialize_name(), people))
    return jsonify(all_people), 200 


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_detail(people_id):

    person = People.query.get(people_id)
    if person:
        person_detail = person.serialize()
        return jsonify(person_detail), 200
    else:
        return jsonify({"message": "Person not found"}), 404


@app.route('/planet', methods=['GET'])
def get_planet():

    planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize_name(), planets))
    return jsonify(all_planets), 200 


@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_planet_detail(planet_id):

    planet1 = Planet.query.get(planet_id)
    if planet1:
        planet_detail = planet1.serialize()
        return jsonify(planet_detail), 200
    else:
        return jsonify({"message": "Planet not found"}), 404
    

@app.route('/favoritePeople', methods=['POST'])
def create_favpeople():
    request_fav_people = request.get_json()

    new_fav_people = FavoritePeople(user_id=request_fav_people["user"], people_id=request_fav_people["people"])
    db.session.add(new_fav_people)
    db.session.commit()

    return jsonify(request_fav_people), 200 

@app.route('/favoritePeople', methods=['GET'])
def get_favpeople():

    fav_people = FavoritePeople.query.all()
    all_favpeople = list(map(lambda x: x.serialize(), fav_people))
    return jsonify(all_favpeople), 200 

@app.route('/<int:user_id>/favoritePeople', methods=['GET'])
def get_user_favpeople(user_id):

    userfav_people = FavoritePeople.query.filter_by(user_id=user_id).all()

    if not userfav_people:
        return {"message": "Este user no ha marcado ningún personaje favorito"}, 404
   
    serialized_favorite_people = [{
        "ID": favorite.people_id,
        "Character's name": People.query.get(favorite.people_id).name
    } for favorite in userfav_people]

    return {'Personajes favoritos del usuario': serialized_favorite_people}, 200


@app.route('/favoritePlanet', methods=['POST'])
def create_favplanet():
    request_fav_planet = request.get_json()

    new_fav_planet = FavoritePlanet(user_id=request_fav_planet["user"], planet_id=request_fav_planet["planet"])
    db.session.add(new_fav_planet)
    db.session.commit()

    return jsonify(request_fav_planet), 200 


@app.route('/favoritePlanet', methods=['GET'])
def get_favplanet():

    fav_planets = FavoritePlanet.query.all()
    all_favplanets = list(map(lambda x: x.serialize(), fav_planets))
    return jsonify(all_favplanets), 200 


@app.route('/<int:user_id>/favoritePlanets', methods=['GET'])
def get_user_favplanets(user_id):

    userfav_planets = FavoritePlanet.query.filter_by(user_id=user_id).all()

    if not userfav_planets:
        return {"message": "Este user no ha marcado ningún planeta favorito"}, 404
   
    serialized_favorite_planet = [{
        "ID": favorite.planet_id,
        "Planet name": Planet.query.get(favorite.planet_id).name
    } for favorite in userfav_planets]

    return {"Planetas favoritos del usuario": serialized_favorite_planet}, 200


@app.route('/user/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def post_user_favplanet(user_id, planet_id):

    user = User.query.get(user_id)
    if not user:
        return {"error": "El usuario no existe"}, 404
    
    planet = Planet.query.get(planet_id)
    if not planet:
        return {"error": "El planeta no existe"}, 404
    
    new_fav_planet = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(new_fav_planet)
    db.session.commit()
    
    return {"message": "Planet agregado como favorito existosamente"}

@app.route('/user/<int:user_id>/people/<int:people_id>', methods=['POST'])
def post_user_favpeople(user_id, people_id):

    user = User.query.get(user_id)
    if not user:
        return {"error": "El usuario no existe"}, 404
    
    people = People.query.get(people_id)
    if not people:
        return {"error": "El personaje no existe"}, 404
    
    new_fav_people = FavoritePeople(user_id=user_id, people_id=people_id)
    db.session.add(new_fav_people)
    db.session.commit()
    
    return {"message": "Personaje agregado como favorito existosamente"}


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
