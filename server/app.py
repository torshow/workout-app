from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Workout
from schemas import workout_schema, workouts_schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


def error(message, status):
    return make_response(jsonify({'error': message}), status)


def get_or_404(model, id):
    return db.session.get(model, id)


@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = get_or_404(Workout, id)
    if not workout:
        return error('Workout not found', 404)
    return make_response(jsonify(workout_schema.dump(workout)), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)