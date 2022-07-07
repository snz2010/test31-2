import factory
from ads.models import Category, Ad
from users.models import User

# 2-07
class NameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad
    name = factory.Faker("name")
# 2-07
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
    slug = factory.Faker("color")
# 2-07
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker("name")
# 2-07
class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad
    name = "name_12345"#factory.SubFactory(NameFactory)
    category = factory.SubFactory(CategoryFactory)
    author = factory.SubFactory(UserFactory)
    price = 10