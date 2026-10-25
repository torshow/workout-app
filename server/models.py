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