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
from models import db, User, People, Planet
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



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
