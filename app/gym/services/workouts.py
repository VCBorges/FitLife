from app.gym import models


def add_exercise_to_workout(
    workout: models.Workouts,
    exercise: models.Exercises,
    repetitions: int,
    sets: int,
    rest_period: int,
    commit: bool = True,
) -> models.WorkoutExercises:
    workout_exercise = models.WorkoutExercises(
        workout=workout,
        exercise=exercise,
        repetitions=repetitions,
        sets=sets,
        rest_period=rest_period,
    )
    if commit:
        workout_exercise.save()
    return workout_exercise
