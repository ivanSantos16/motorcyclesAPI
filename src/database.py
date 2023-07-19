from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string
from sqlalchemy.orm import backref
import random

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    # bookmarks = db.relationship("Bookmark", backref="user")
    motorcycles = db.relationship("Motorcycle", backref="user")

    def __repr__(self):
        return "User>>> {self.username}"


class Motorcycle(db.Model):
    niv = db.Column(db.String(17), primary_key=True)
    brand = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    displacement = db.Column(db.Integer, nullable=False)
    power = db.Column(db.Float, nullable=False)
    torque = db.Column(db.Integer, nullable=False)
    engine_cylinders = db.Column(db.String(20), nullable=False)
    engine_stroke = db.Column(db.String(20), nullable=False)
    gearbox = db.Column(db.String(50), nullable=False)
    bore = db.Column(db.Integer, nullable=False)
    stroke = db.Column(db.Float, nullable=False)
    transmission_type = db.Column(db.String(50), nullable=False)
    front_brakes = db.Column(db.String(50), nullable=False)
    rear_brakes = db.Column(db.String(50), nullable=False)
    front_suspension = db.Column(db.String(50), nullable=False)
    rear_suspension = db.Column(db.String(50), nullable=False)
    front_tire = db.Column(db.String(50), nullable=False)
    rear_tire = db.Column(db.String(50), nullable=False)
    dry_weight = db.Column(db.Integer, nullable=False)
    wheelbase = db.Column(db.Integer, nullable=False)
    fuel_capacity = db.Column(db.Integer, nullable=False)
    fuel_system = db.Column(db.String(50), nullable=False)
    fuel_control = db.Column(db.String(50), nullable=False)
    seat_height = db.Column(db.Float, nullable=False)
    cooling_system = db.Column(db.String(200), nullable=False)
    color_options = db.Column(db.String(200), nullable=False)

    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=False, unique=True)
    visits = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime(), default=datetime.now())

    def generate_short_url(self):
        characters = string.digits + string.ascii_letters
        piked_chars = "".join(random.choices(characters, k=3))

        link = self.query.filter_by(short_url=piked_chars).first()

        if link:
            self.generate_short_url()
        else:
            return piked_chars

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.short_url = self.generate_short_url()

    def __repr__(self):
        return "Motorcycles >>> {self.brand} {self.model} {self.year}"
