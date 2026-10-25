#!/usr/bin/env python3
from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print('Clearing old data...')
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print('Creating exercises...')
    squat = Exercise(name='Squat', category='strength', equipment_needed=True)
    pushup = Exercise(name='Push-up', category='strength', equipment_needed=False)
    plank = Exercise(name='Plank', category='core', equipment_needed=False)
    running = Exercise(name='Running', category='cardio', equipment_needed=False)
    db.session.add_all([squat, pushup, plank, running])

    print('Creating workouts...')
    leg_day = Workout(date=date(2026, 10, 20), duration_minutes=45, notes='Focus on form')
    full_body = Workout(date=date(2026, 10, 22), duration_minutes=60, notes='Light weights')
    cardio = Workout(date=date(2026, 10, 23), duration_minutes=30)
    db.session.add_all([leg_day, full_body, cardio])
    db.session.commit()

    print('Linking exercises to workouts...')
    links = [
        WorkoutExercise(workout=leg_day, exercise=squat, reps=10, sets=4),
        WorkoutExercise(workout=leg_day, exercise=plank, duration_seconds=60),
        WorkoutExercise(workout=full_body, exercise=pushup, reps=15, sets=3),
        WorkoutExercise(workout=full_body, exercise=squat, reps=12, sets=3),
        WorkoutExercise(workout=full_body, exercise=plank, duration_seconds=90),
        WorkoutExercise(workout=cardio, exercise=running, duration_seconds=1200),
    ]
    db.session.add_all(links)
    db.session.commit()
    print('Done seeding!')