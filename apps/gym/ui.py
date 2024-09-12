from django.db.models import CharField, F, Value
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast, Concat

from apps.core.constants import Language
from apps.core.ui import SelectOptionsSchema, model_select_input_options
from apps.gym import dtos, models


def muscles_select_input_options(
    *,
    language: Language = Language.EN,
    lookups: dtos.MusclesLookups = dtos.MusclesLookups(),
    order_by: list[str] | None = None,
) -> list[SelectOptionsSchema]:
    queryset = models.MuscleGroups.objects.filter(**lookups.to_dict())
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
        .filter(**lookups.to_dict())
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
    queryset = models.Equipments.objects.filter(**lookups.to_dict())
    if order_by:
        queryset = queryset.order_by(*order_by)
    return model_select_input_options(
        queryset=queryset,
        value_field='id',
        text_field=f'name__{language}',
    )


def workout_exercises_card_form(
    *,
    workout: models.Workouts,
    language: Language,
    # lookups: dtos.WorkoutExercisesLookups = dtos.WorkoutExercisesLookups(),
) -> list[dict[str, str]]:
    queryset = (
        workout.workout_exercises.select_related('exercise')
        .values('id')
        .annotate(
            name=KeyTextTransform(
                language,
                'exercise__name',
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
    return queryset
