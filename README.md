# Workout Tracker API

## Description
A backend API for personal trainers to track workouts and the exercises in them.
Built with Flask, Flask-SQLAlchemy, Flask-Migrate and Marshmallow.

- A **Workout** has a date, a duration and optional notes.
- An **Exercise** is reusable (name, category, whether it needs equipment).
- A **WorkoutExercise** (join table) links an exercise to a workout and stores
  the reps, sets and/or duration for that exercise in that workout.

## Installation
```bash
git clone <your-repo-url>
cd workout-app
pipenv install
pipenv shell
cd server
export FLASK_APP=app.py
flask db upgrade head      # creates the database from the included migration
python seed.py             # adds example data (safe to re-run, it resets the data)
```
If you ever delete the `migrations/` folder, rebuild it with:
`flask db init`, `flask db migrate -m "create tables"`, `flask db upgrade head`.

## Running
```bash
cd server
flask run -p 5555
# or: python app.py
```
The API is then at http://localhost:5555

## Endpoints
| Method | Route | Description |
|--------|-------|-------------|
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | One workout with its exercises, including reps/sets/duration |
| POST | `/workouts` | Create a workout. Body: `{"date": "2026-11-01", "duration_minutes": 40, "notes": "optional"}` |
| DELETE | `/workouts/<id>` | Delete a workout and its WorkoutExercises |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | One exercise with the workouts it appears in |
| POST | `/exercises` | Create an exercise. Body: `{"name": "Lunge", "category": "strength", "equipment_needed": false}` |
| DELETE | `/exercises/<id>` | Delete an exercise and its WorkoutExercises |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout. Body: `{"reps": 10, "sets": 3}` and/or `{"duration_seconds": 60}` |

Errors return JSON like `{"error": ...}` with status 400 (bad data) or 404 (not found).

## Validations
- **Table constraints:** unique exercise name, non-empty name, workout duration > 0,
  reps/sets/duration > 0, an exercise can only be added to a workout once.
- **Model validations (`@validates`):** exercise name/category not blank, workout
  duration > 0, notes max 500 chars, reps/sets/duration > 0.
- **Schema validations (Marshmallow):** required fields, `Range` and `Length` checks,
  a `@validates` check on exercise name, and a `@validates_schema` check that every
  workout exercise has reps+sets or a duration.