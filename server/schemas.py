from marshmallow import (Schema, fields, validate, validates,
                         validates_schema, ValidationError)


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))

    workout = fields.Nested('WorkoutSchema',
                            only=('id', 'date', 'duration_minutes'),
                            dump_only=True)
    exercise = fields.Nested('ExerciseSchema',
                             only=('id', 'name', 'category', 'equipment_needed'),
                             dump_only=True)

    @validates_schema
    def check_effort(self, data, **kwargs):
        """Every entry needs reps and sets, or a duration (or both)."""
        has_reps_sets = data.get('reps') is not None and data.get('sets') is not None
        has_duration = data.get('duration_seconds') is not None
        if not (has_reps_sets or has_duration):
            raise ValidationError(
                'Provide reps and sets, or duration_seconds (or both).')


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    category = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    equipment_needed = fields.Bool(load_default=False)

    workout_exercises = fields.Nested('WorkoutExerciseSchema', many=True,
                                      exclude=('exercise',), dump_only=True)

    @validates('name')
    def validate_name(self, value):
        if not value.strip():
            raise ValidationError('Name cannot be blank.')


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True, validate=validate.Length(max=500))

    workout_exercises = fields.Nested('WorkoutExerciseSchema', many=True,
                                      exclude=('workout',), dump_only=True)


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=('workout_exercises',))
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=('workout_exercises',))
workout_exercise_schema = WorkoutExerciseSchema(exclude=('workout', 'exercise'))