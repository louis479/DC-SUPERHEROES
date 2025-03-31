
from flask import Flask
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)
