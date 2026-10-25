from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates


db = SQLAlchemy()
 
 
class Exercise(db.Model):
    __tablename__ = 'exercises'
 
    __table_args__ = (
        CheckConstraint('length(name) > 0', name='ck_exercise_name_not_empty'),
        UniqueConstraint('name', name='uq_exercise_name'),
    )
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)


    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise',
        cascade='all, delete-orphan')
    workouts = association_proxy('workout_exercises', 'workout')

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError('Exercise name cannot be blank.')
        return value.strip()
 
    @validates('category')
    def validate_category(self, key, value):
        if not value or not value.strip():
            raise ValueError('Exercise category cannot be blank.')
        return value.strip().lower()
 
    def __repr__(self):
        return f'<Exercise {self.id}: {self.name}>'
 
 
class Workout(db.Model):
    __tablename__ = 'workouts'
 

    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='ck_workout_duration_positive'),
    )
 
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
 
    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout',
        cascade='all, delete-orphan')
    exercises = association_proxy('workout_exercises', 'exercise')