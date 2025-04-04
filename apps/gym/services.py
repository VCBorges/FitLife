from django.db import transaction
from django.utils import timezone

from apps.core.utils import clean_model, update_model_fields
from apps.gym import models, typed
from apps.users.models import Users


class WorkoutService:
    @transaction.atomic
    def create_workout(
        self,
        *,
        creator: Users,
        title: str,
        user: Users | None = None,
        description: str | None = None,
        exercises: list[typed.CreateWorkoutExerciseSchema] | None = None,
    ) -> models.Workout:
        workout = models.Workout(
            creator=creator,
            user=user or creator,
            title=title,
            description=description,
        )
        clean_model(workout)
        workout.save()
        if exercises:
            self._create_workout_exercises(
                workout=workout,
                exercises=exercises,
            )
        return workout

    def _create_workout_exercises(
        self,
        *,
        workout: models.Workout,
        exercises: list[typed.CreateWorkoutExerciseSchema],
    ) -> list[models.Exercise]:
        instances = [
            models.WorkoutExercise(
                user=workout.user,
                workout=workout,
                **exercise,
            )
            for exercise in exercises
        ]
        clean_model(*instances)
        models.WorkoutExercise.objects.bulk_create(instances)

    @transaction.atomic
    def update_workout(
        self,
        *,
        workout: models.Workout,
        title: str,
        description: str | None = None,
        exercises: typed.ExercisesUpdateWorkout | None = None,
    ) -> models.Workout:
        workout.title = title
        workout.description = description
        clean_model(workout)
        workout.save(
            update_fields=[
                'title',
                'description',
            ]
        )
        if exercises:
            if exercises['to_create']:
                self._create_workout_exercises(
                    workout=workout,
                    exercises=exercises['to_create'],
                )

            if exercises['to_update']:
                self._update_exercise(exercises['to_update'])

            if exercises['to_delete']:
                self._delete_exercise(exercises['to_delete'])

        return workout

    def _update_exercise(
        self,
        exercises: list[typed.ExercisesUpdateWorkout],
    ) -> None:
        instances = []
        for exercise in exercises:
            exercise_instance = exercise.pop('workout_exercise')
            update_model_fields(
                model=exercise_instance,
                data=exercise,
            )
            instances.append(exercise_instance)
        clean_model(*instances)
        models.WorkoutExercise.objects.bulk_update(
            instances,
            fields=[
                'sets',
                'repetitions',
                'weight',
                'rest_period',
            ],
        )

    def _delete_exercise(self, exercises: list[dict[str, models.WorkoutExercise]]):
        models.WorkoutExercise.objects.filter(
            id__in=[exercise['workout_exercise'].pk for exercise in exercises]
        ).delete()

    @transaction.atomic
    def delete_workout(self, workout: models.Workout) -> int:
        exercises = workout.workout_exercises.all()
        exercises.delete()
        return workout.delete()

    @transaction.atomic
    def complete_workout(
        self,
        *,
        user: Users,
        workout: models.Workout,
        exercises: list[typed.CompleteWorkoutExerciseSchema],
    ) -> models.WorkoutHistory:
        workout_history = models.WorkoutHistory(
            user=user,
            workout=workout,
            title=workout.title,
            description=workout.description,
            completed_at=timezone.now(),
            creator=workout.creator,
        )
        clean_model(workout_history)
        workout_history.save()
        exercises_instances = [
            models.WorkoutHistoryExercises(
                user=user,
                workout_history=workout_history,
                exercise=exercise['workout_exercise'].exercise,
                is_done=exercise['is_done'],
                sets=exercise['repetitions'],
                repetitions=exercise['repetitions'],
                weight=exercise['weight'],
                rest_period=exercise['rest_period'],
            )
            for exercise in exercises
        ]
        clean_model(*exercises_instances)
        models.WorkoutHistoryExercises.objects.bulk_create(exercises_instances)
        return workout_history

    @transaction.atomic
    def uncomplete_workout(self, workout_history: models.WorkoutHistory) -> None:
        exercises = workout_history.exercises.all()
        exercises.delete()
        workout_history.delete()

    @transaction.atomic
    def clone_workout(
        self,
        *,
        user: Users,
        workout: models.Workout,
    ) -> models.Workout:
        workout_clone = self.create_workout(
            user=user,
            title=workout.title,
            description=workout.description,
            creator=workout.creator,
            exercises=[
                {
                    'exercise': workout_exercise.exercise,
                    'sets': workout_exercise.sets,
                    'repetitions': workout_exercise.repetitions,
                    'weight': workout_exercise.weight,
                    'rest_period': workout_exercise.rest_period,
                }
                for workout_exercise in workout.workout_exercises.all()
            ],
        )
        return workout_clone
