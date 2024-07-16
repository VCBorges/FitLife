from app.gym import models
from app.gym.transfer import workouts as workout_transfer


def test_workout_create_dto_get_field_names_to_all_fields_be_in_workout_model_fields():
    fields = workout_transfer.WorkoutCreateDTO.get_field_names()

    assert all(models.Workouts._meta.get_field(field) for field in fields)


def test_workout_update_dto_get_field_names_to_all_fields_be_in_workout_model_fields():
    fields = workout_transfer.WorkoutUpdateDTO.get_field_names()

    assert all(models.Workouts._meta.get_field(field) for field in fields)


def test_workout_exercise_create_dto_get_field_names_to_all_fields_be_in_workout_exercise_model_fields():
    fields = workout_transfer.WorkoutExerciseCreateDTO.get_field_names()

    assert all(models.WorkoutExercises._meta.get_field(field) for field in fields)


def test_workout_exercise_update_dto_get_field_names_to_all_fields_be_in_workout_exercise_model_fields():
    fields = workout_transfer.WorkoutExerciseUpdateDTO.get_field_names()

    assert all(models.WorkoutExercises._meta.get_field(field) for field in fields)
