from extension_app import db  # Import database instance from the extension module to prevent circular error between models and app

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

# Here are the models  for Hero, Power & HeroPower
class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    super_name = db.Column(db.String, nullable=False)

class Power(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

class HeroPower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey("hero.id"), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey("power.id"), nullable=False)
    strength = db.Column(db.String, nullable=False)

