from flask import Flask, jsonify, make_response, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from models import db, Workout, Exercise, WorkoutExercise
from schemas import (workout_schema, workouts_schema, exercise_schema,
                     exercises_schema, workout_exercise_schema)

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


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.get_json() or {})
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
    except ValidationError as e:
        return error(e.messages, 400)
    except ValueError as e:
        db.session.rollback()
        return error(str(e), 400)
    except IntegrityError:
        db.session.rollback()
        return error('Database constraint failed', 400)
    return make_response(jsonify(workout_schema.dump(workout)), 201)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = get_or_404(Workout, id)
    if not workout:
        return error('Workout not found', 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response('', 204)


@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = get_or_404(Exercise, id)
    if not exercise:
        return error('Exercise not found', 404)
    return make_response(jsonify(exercise_schema.dump(exercise)), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json() or {})
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
    except ValidationError as e:
        return error(e.messages, 400)
    except ValueError as e:
        db.session.rollback()
        return error(str(e), 400)
    except IntegrityError:
        db.session.rollback()
        return error('An exercise with that name already exists', 400)
    return make_response(jsonify(exercise_schema.dump(exercise)), 201)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = get_or_404(Exercise, id)
    if not exercise:
        return error('Exercise not found', 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response('', 204)


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
           methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    if not get_or_404(Workout, workout_id):
        return error('Workout not found', 404)
    if not get_or_404(Exercise, exercise_id):
        return error('Exercise not found', 404)

    try:
        data = workout_exercise_schema.load(request.get_json() or {})
        we = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, **data)
        db.session.add(we)
        db.session.commit()
    except ValidationError as e:
        return error(e.messages, 400)
    except ValueError as e:
        db.session.rollback()
        return error(str(e), 400)
    except IntegrityError:
        db.session.rollback()
        return error('That exercise is already in this workout', 400)
    return make_response(jsonify(workout_exercise_schema.dump(we)), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
