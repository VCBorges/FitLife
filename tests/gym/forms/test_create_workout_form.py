from app.gym.forms import CreateWorkoutForm


def test_to_be_valid_with_empty_exercises():
    form = CreateWorkoutForm(
        data={
            'name': 'test',
            'description': 'test',
        }
    )
    assert form.is_valid() is True
