import json
import pandas as pandas
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.viewsets import ModelViewSet
from django.views.generic import CreateView
from users.serializers import UserCreateSerializer, UserSerializer, UserDetailSerializer, UserUpdateSerializer, UserDestroySerializer
from users.serializers import LocationCreateSerializer, LocationSerializer, LocationDetailSerializer, LocationUpdateSerializer, LocationDestroySerializer, LocationsSerializer
from users.models import User, Location

################################################################################
# заполнение таблицы локаций, используя данные из файла
class AddToLo(View):
    def get(self, request):
        csv_data = pandas.read_csv('users/data/location.csv', sep=",").to_dict()
        i = 0
        while max(csv_data['id'].keys()) >= i:
            Location.objects.create(
                name=csv_data["name"][i],
                lat=csv_data["lat"][i],
                lng=csv_data["lng"][i],
            )
            i += 1
        return JsonResponse("Add to table Location - Ok", safe=False, status=200)



################################################################################
# заполнение таблицы пользователей, используя данные из файла
class AddToUsr(CreateView):
    model = User
    fields = ["first_name", "last_name", "username", "password", "role", "age", "locations"]
    def get(self, request):
        csv_data = pandas.read_csv('users/data/user.csv', sep=",").to_dict()
        i = 0
        while max(csv_data['id'].keys()) >= i:
            try:
                location_obj = Location.objects.get(id=csv_data["location_id"][i])
            except Location.DoesNotExist:
                return JsonResponse("Локация не найдена!", status=404)

            print("***")
            print(dir(location_obj))
            print("***")
            new_u = User.objects.create(
                first_name=csv_data["first_name"][i],
                last_name=csv_data["last_name"][i],
                username=csv_data["username"][i],
                password=csv_data["password"][i],
                role=csv_data["role"][i],
                age=csv_data["age"][i],
            )
            new_u.locations.add(location_obj)
            i += 1
        return JsonResponse("Add to table User - Ok", safe=False, status=200)



# создание
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

# посмотр всех пользователей
class UserView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# детальный просмотр
class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

# обновление
class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

# удаление
class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDestroySerializer



# создание локации
#class LocCreateView(CreateAPIView):
class LocationViewSet(ModelViewSet): # CRUD для таблицы ЛОКАЦИЙ через ViewSet
    queryset = Location.objects.all()
    #serializer_class = LocationCreateSerializer
    serializer_class = LocationsSerializer

# посмотр всех локаций
class LocView(ListAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

# детальный
class LocDetailView(RetrieveAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationDetailSerializer

# обновление
class LocUpdateView(UpdateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationUpdateSerializer

# удаление
class LocDeleteView(DestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationDestroySerializer
