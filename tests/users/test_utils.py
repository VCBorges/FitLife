from src.users import utils
from src.users.models import Users


def test_get_user_model_to_return_user_model():
    user_model = utils.get_user_model()
    assert user_model == Users
