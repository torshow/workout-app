from marshmallow import Schema, fields


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True)
    sets = fields.Int(allow_none=True)
    duration_seconds = fields.Int(allow_none=True)

    workout = fields.Nested('WorkoutSchema',
                            only=('id', 'date', 'duration_minutes'),
                            dump_only=True)
    exercise = fields.Nested('ExerciseSchema',
                             only=('id', 'name', 'category', 'equipment_needed'),
                             dump_only=True)


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)

    workout_exercises = fields.Nested('WorkoutExerciseSchema', many=True,
                                      exclude=('exercise',), dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(allow_none=True)

    workout_exercises = fields.Nested('WorkoutExerciseSchema', many=True,
                                      exclude=('workout',), dump_only=True)


workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=('workout_exercises',))
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=('workout_exercises',))
workout_exercise_schema = WorkoutExerciseSchema(exclude=('workout', 'exercise'))