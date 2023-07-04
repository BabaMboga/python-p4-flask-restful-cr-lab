#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder = SerializerMixin.json_encoder
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify(plants)

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get(plant_id)
        if plant is None:
            response = {'error': 'Plant not found'}
            return make_response(jsonify(response), 404)
        return jsonify(plant)

    def post(self):
        data = request.get_json()
        plant = Plant(name=data['name'], image=data['image'], price=data['price'])
        db.session.add(plant)
        db.session.commit()
        return jsonify(plant), 201

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')

        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
