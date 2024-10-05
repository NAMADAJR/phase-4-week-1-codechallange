#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

db.init_app(app)  # Initialize the db before using it with migrate
migrate = Migrate(app, db)  # Now we can use migrate

api = Api(app)

# Route for getting all heroes
class HeroList(Resource):
    def get(self):
        heroes = Hero.query.all()
        return jsonify([{
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        } for hero in heroes])  # Updated to return only necessary fields

# Route for getting a hero by id
class HeroDetail(Resource):
    def get(self, id):
        hero = db.session.get(Hero, id)  # Updated line
        if not hero:
            return {"error": "Hero not found"}, 404
        return jsonify(hero.to_dict())

# Route for getting all powers
class PowerList(Resource):
    def get(self):
        powers = Power.query.all()
        return jsonify([power.to_dict() for power in powers])

# Route for getting a power by id
class PowerDetail(Resource):
    def get(self, id):
        power = db.session.get(Power, id)  # Updated line
        if not power:
            return {"error": "Power not found"}, 404
        return jsonify(power.to_dict())

    def patch(self, id):
        power = db.session.get(Power, id)  # Updated line
        if not power:
            return {"error": "Power not found"}, 404
        
        data = request.get_json()
        if 'description' in data:
            if len(data['description']) < 20:
                return {"errors": ["validation errors"]}, 400  # Change this line
            power.description = data['description']
            db.session.commit()
            return jsonify(power.to_dict())
        return {"errors": ["No valid fields provided"]}, 400

# Route for creating a new HeroPower
class HeroPowerList(Resource):
    def post(self):
        data = request.get_json()
        strength = data.get('strength')
        power_id = data.get('power_id')
        hero_id = data.get('hero_id')

        # Check if the power and hero exist
        hero = db.session.get(Hero, hero_id)  # Updated line
        if not hero:
            return {"errors": ["Hero not found"]}, 404
        
        power = db.session.get(Power, power_id)  # Updated line
        if not power:
            return {"errors": ["Power not found"]}, 404

        if strength not in ['Strong', 'Weak', 'Average']:
            return {"errors": ["validation errors"]}, 400  # Change this line

        # Check if the HeroPower already exists
        existing_hero_power = HeroPower.query.filter_by(hero_id=hero_id, power_id=power_id).first()
        if existing_hero_power:
            return {"errors": ["This hero already has this power."]}, 400
        
        new_hero_power = HeroPower(
            strength=strength,
            power_id=power_id,
            hero_id=hero_id
        )
        db.session.add(new_hero_power)
        db.session.commit()

        return jsonify({
            "id": new_hero_power.id,
            "hero_id": hero.id,
            "power_id": power.id,
            "strength": strength,
            "hero": hero.to_dict(),
            "power": power.to_dict()
        }), 201

# Registering routes
api.add_resource(HeroList, '/heroes')
api.add_resource(HeroDetail, '/heroes/<int:id>')
api.add_resource(PowerList, '/powers')
api.add_resource(PowerDetail, '/powers/<int:id>')
api.add_resource(HeroPowerList, '/hero_powers')

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

if __name__ == '__main__':
    app.run(port=5555, debug=True)
