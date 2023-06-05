from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True, default=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    info = db.Column(db.String)
    birth_year = db.Column(db.String)
    eye_color = db.Column(db.String)
    hair_color = db.Column(db.String)
    height = db.Column(db.String)
    mass = db.Column(db.String)
    skin_color = db.Column(db.String)

    def serialize_name(self):
        return {
            "id": self.id,
            "name": self.name,
        }   
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "info": self.info,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color
        }   

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    info = db.Column(db.String)
    climate = db.Column(db.String)
    diameter = db.Column(db.String)
    gravity = db.Column(db.String)
    terrain = db.Column(db.String)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "info": self.info,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "terrain": self.terrain,
        }
    
    def serialize_name(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class FavoritePeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    people_id = db.Column(db.Integer, db.ForeignKey(People.id))

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "people": self.people_id,
        }
    
class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    planet_id = db.Column(db.Integer, db.ForeignKey(Planet.id))

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "planet": self.planet_id,
        }
    
