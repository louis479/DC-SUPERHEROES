from flask import Flask, jsonify, request
from extensions import db, migrate
from models import Hero, Power, HeroPower

#here you Initialize  your Flask app & Configure SQLite database
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///superhero.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app) # Initialize database
migrate.init_app(app, db) # Set up the Flask-Migrate for handling database migrations

# Define the home route
@app.route("/")
def home():
    return {"message": "Welcome to the Superheroes API!"}

# Routes that assist you in your postman
@app.route("/heroes", methods=["GET"])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{ "id": hero.id, "name": hero.name, "super_name": hero.super_name } for hero in heroes])

@app.route("/heroes/<int:id>", methods=["GET"])
def get_hero(id):
    hero = Hero.query.get(id)
    if hero:
        return jsonify({ "id": hero.id, "name": hero.name, "super_name": hero.super_name })
    return jsonify({"error": "Hero not found"}), 404

@app.route("/powers", methods=["GET"])
def get_powers():
    powers = Power.query.all()
    return jsonify([{ "id": power.id, "name": power.name, "description": power.description } for power in powers])

@app.route("/powers/<int:id>", methods=["GET"])
def get_power(id):
    power = Power.query.get(id)
    if power:
        return jsonify({"id": power.id, "name": power.name, "description": power.description})
    return jsonify({"error": "Power not found"}), 404

@app.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.json
    if "description" in data and len(data["description"]) >= 20:
        power.description = data["description"]
        db.session.commit()
        return jsonify({"id": power.id, "name": power.name, "description": power.description})
    
    return jsonify({"errors": ["Validation error"]}), 400

# Here is the point in the code in which hero & power relationship merge
@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    data = request.json
    hero = Hero.query.get(data["hero_id"])
    power = Power.query.get(data["power_id"])

    if not hero or not power:
        return jsonify({"errors": ["Invalid hero or power ID"]}), 400

    if data["strength"] not in ["Strong", "Weak", "Average"]:
        return jsonify({"errors": ["Invalid strength value"]}), 400

    hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=data["strength"])
    db.session.add(hero_power)
    db.session.commit()

    return jsonify({
        "id": hero_power.id,
        "hero_id": hero.id,
        "power_id": power.id,
        "strength": hero_power.strength
    })
# Import the models to ensure they are registered with SQLAlchemy
# from extension_app import db  # Import database instance from the extension module to prevent circular error between models and app
# from flask_sqlalchemy import SQLAlchemy      
# db = SQLAlchemy()                               


# This ensures that the models are imported correctly
from models import Hero, Power, HeroPower

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)