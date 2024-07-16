from datetime import datetime

from app.users.models import Users

import factory
import factory.fuzzy


class UsersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Users

    email = factory.Faker('email')
    password = factory.Faker('password')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    birth_date = factory.LazyFunction(datetime.now)
    document = factory.fuzzy.FuzzyText(length=17)
    is_active = True
