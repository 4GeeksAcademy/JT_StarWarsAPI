from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True, default=False)

    def __repr__(self):
        return '<User %r>' % self.email

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

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.name,
        }   

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    info = db.Column(db.String)
    climate = db.Column(db.String)
    diameter = db.Column(db.String)
    gravity = db.Column(db.String)
    terrain = db.Column(db.String)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.name,
        }

class FavoritePeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    people_id = db.Column(db.Integer, db.ForeignKey(People.id))

    def __repr__(self):
        return '<FavoritePeople %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "people": self.people_id,
        }
    
class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    planet_id = db.Column(db.Integer, db.ForeignKey(Planet.id))

    def __repr__(self):
        return '<FavoritePlanet %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "planet": self.planet_id,
        }
    
