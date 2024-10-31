from typing import Any
from zoneinfo import ZoneInfo

from django.core.paginator import Paginator
from django.db.models import CharField, F, Prefetch, Value
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast, Concat, Trunc
from django.db.models.query import QuerySet

from apps.core.constants import Language
from apps.core.ui import SelectOptionsSchema, model_select_input_options
from apps.core.utils import formatted_date
from apps.gym import dtos, models


def muscles_select_input_options(
    *,
    language: Language = Language.EN,
    lookups: dtos.MusclesLookups = dtos.MusclesLookups(),
    order_by: list[str] | None = None,
) -> list[SelectOptionsSchema]:
    queryset = models.MuscleGroups.objects.filter(**lookups.as_dict())
    if order_by:
        queryset = queryset.order_by(*order_by)
    return model_select_input_options(
        queryset=queryset,
        value_field='id',
        text_field=f'name__{language}',
    )


def exercises_select_input_options(
    *,
    language: Language = Language.EN,
    lookups: dtos.ExercisesLookups = dtos.ExercisesLookups(),
    order_by: list[str] | None = None,
) -> list[SelectOptionsSchema]:
    queryset = (
        models.Exercises.objects.select_related(
            'primary_muscle',
            'equipment',
        )
        .filter(**lookups.as_dict())
        .values('id')
        .annotate(
            name_language=KeyTextTransform(
                language,
                'name',
            ),
            primary_muscle_language=KeyTextTransform(
                language,
                'primary_muscle__name',
            ),
            text_field=Concat(
                'name_language',
                Value(' ('),
                'primary_muscle_language',
                Value(')'),
                output_field=CharField(),
            ),
            primary_muscle_id=Cast(
                F('primary_muscle_id'),
                output_field=CharField(),
            ),
            equipment_id=Cast(
                F('equipment_id'),
                output_field=CharField(),
            ),
        )
        .order_by(*order_by or [])
    )
    return model_select_input_options(
        queryset=queryset,
        value_field='id',
        text_field='text_field',
        extra_expressions={
            'muscle_id': F('primary_muscle_id'),
            'equipment_id': F('equipment_id'),
        },
    )


def equipments_select_input_options(
    *,
    language: Language = Language.EN,
    lookups: dtos.EquipmentsLookups = dtos.EquipmentsLookups(),
    order_by: list[str] | None = None,
) -> list[SelectOptionsSchema]:
    queryset = models.Equipments.objects.filter(**lookups.as_dict()).order_by(
        *order_by or []
    )
    return model_select_input_options(
        queryset=queryset,
        value_field='id',
        text_field=f'name__{language}',
    )


def workout_exercises_form_card(
    *,
    workout: models.Workouts,
    language: Language,
) -> QuerySet[str, str | int]:
    """
    Returns a value QuerySet with the fields to be used in workout exercises
    form card

    Parameters
    ----------
    - workout (models.Workouts):
        A workout instance.
    - language (Language):
        The language to be used in the query.

    Returns
    -------
    QuerySet[str, str | int]: A QuerySet with the fields mentioned above.
    """
    queryset = (
        workout.workout_exercises.select_related(
            'exercise',
            'exercise__primary_muscle',
        )
        .values('id')
        .annotate(
            exercise_name=KeyTextTransform(
                language,
                'exercise__name',
            ),
            muscle_name=KeyTextTransform(
                language,
                'exercise__primary_muscle__name',
            ),
            name=Concat(
                'exercise_name',
                Value(' ('),
                'muscle_name',
                Value(')'),
                output_field=CharField(),
            ),
            workout_exercise_id=Cast(
                F('id'),
                output_field=CharField(),
            ),
            exercise_id=Cast(
                F('exercise__id'),
                output_field=CharField(),
            ),
        )
        .order_by('created_at')
        .values(
            'workout_exercise_id',
            'exercise_id',
            'name',
            'notes',
            'sets',
            'repetitions',
            'weight',
            'rest_period',
        )
    )
    return list(queryset)


def workouts_list(
    *,
    lookups: dtos.UserWorkoutLookups,
    language: Language,
    page_number: int = 1,
    page_size: int = 50,
    order_by: list[str] | None = None,
) -> dict[str, Any]:
    exercises_qs = (
        models.WorkoutExercises.objects.select_related(
            'exercise',
            'exercise__primary_muscle',
        )
        .annotate(
            exercise_name=KeyTextTransform(
                language,
                'exercise__name',
            ),
            muscle_name=KeyTextTransform(
                language,
                'exercise__primary_muscle__name',
            ),
            name=Concat(
                'exercise_name',
                Value(' ('),
                'muscle_name',
                Value(')'),
                output_field=CharField(),
            ),
        )
        .only(
            'exercise__id',
            'exercise__primary_muscle__id',
            'workout__id',
            'sets',
            'repetitions',
            'weight',
        )
    )
    workouts_qs = (
        models.Workouts.objects.prefetch_related(
            Prefetch(
                'workout_exercises',
                queryset=exercises_qs,
            )
        )
        .filter(
            **lookups.as_dict(),
        )
        .order_by(*order_by or ['-created_at'])
        .only(
            'id',
            'title',
        )
    )
    paginator = Paginator(workouts_qs, page_size)
    result_page = paginator.get_page(page_number)
    page_qs: QuerySet[models.Workouts] = result_page.object_list
    ret = dtos.PaginatedData(
        total_pages=paginator.num_pages,
        current_page=page_number,
        total_size=paginator.count,
        page_size=paginator.per_page,
        data=[
            {
                'id': str(workout.pk),
                'title': workout.title,
                'exercises': [
                    {
                        'id': str(exercise.pk),
                        'name': exercise.name,
                        'repetitions': exercise.repetitions,
                        'sets': exercise.sets,
                        'weight': exercise.weight,
                    }
                    for exercise in workout.workout_exercises.all()
                ],
            }
            for workout in page_qs
        ],
    )
    return ret.as_dict()


def workout_history_list(
    *,
    lookups: dtos.UserWorkoutHistoryLookups,
    language: Language,
    page_number: int = 1,
    page_size: int = 50,
    order_by: list[str] | None = None,
) -> dict[str, Any]:
    print(f'{lookups.as_dict() = }')
    exercises_qs = (
        models.WorkoutHistoryExercises.objects.select_related(
            'exercise',
            'exercise__primary_muscle',
        )
        .annotate(
            exercise_name=KeyTextTransform(
                language,
                'exercise__name',
            ),
            muscle_name=KeyTextTransform(
                language,
                'exercise__primary_muscle__name',
            ),
            name=Concat(
                'exercise_name',
                Value(' ('),
                'muscle_name',
                Value(')'),
                output_field=CharField(),
            ),
        )
        .only(
            'exercise__id',
            'exercise__primary_muscle__id',
            'workout_history__id',
            'sets',
            'repetitions',
            'weight',
            'is_done',
            'rest_period',
        )
    )
    workouts_qs = (
        models.WorkoutHistory.objects.prefetch_related(
            Prefetch(
                'workout_history_exercises',
                queryset=exercises_qs,
            )
        )
        .filter(
            **lookups.as_dict(),
        )
        .order_by(*order_by or ['-created_at'])
        .only(
            'id',
            'title',
            'completed_at',
        )
        .annotate(
            local_completed_at=Trunc(
                'completed_at',
                kind='minute',  # or 'minute', 'hour', 'day' depending on your needs
                tzinfo=ZoneInfo('America/Sao_Paulo'),
            )
        )
    )
    paginator = Paginator(workouts_qs, page_size)
    result_page = paginator.get_page(page_number)
    page_qs: QuerySet[models.WorkoutHistory] = result_page.object_list
    ret = dtos.PaginatedData(
        total_pages=paginator.num_pages,
        current_page=page_number,
        total_size=paginator.count,
        page_size=paginator.per_page,
        data=[
            {
                'id': str(workout.pk),
                'title': workout.title,
                'completed_at': formatted_date(workout.local_completed_at),
                'exercises': [
                    {
                        'id': str(exercise.pk),
                        'name': exercise.name,
                        'repetitions': exercise.repetitions,
                        'sets': exercise.sets,
                        'weight': exercise.weight,
                        'is_done': exercise.is_done,
                        'rest_period': exercise.rest_period,
                    }
                    for exercise in workout.workout_history_exercises.all()
                ],
            }
            for workout in page_qs
        ],
    )
    return ret.as_dict()


def workout_history_select_filter_options() -> list[SelectOptionsSchema]:
    queryset = (
        models.WorkoutHistory.objects.values(
            'title',
        )
        .order_by('title')
        .distinct()
    )
    return model_select_input_options(
        queryset=queryset,
        value_field='title',
        text_field='title',
    )
