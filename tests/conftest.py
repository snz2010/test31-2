# 2-07
from pytest_factoryboy import register
from tests.factories import UserFactory, CategoryFactory, AdFactory

pytest_plugins = "tests.fixtures"

register(UserFactory)
register(CategoryFactory)
register(AdFactory)