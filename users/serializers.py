from rest_framework import serializers
from users.models import User, Location, Selection


# 2-07
class CheckRambler:
    def __call__(self, value):
        if value.endswith("rambler.ru"):
            raise serializers.ValidationError("Rambler users cant register")

class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )
    email = serializers.EmailField(validators=[CheckRambler()]) # 2-07

    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations") # 2-07
        return super().is_valid(raise_exception=raise_exception)

    class Meta:
        model = User
        fields = '__all__'
    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data["password"]) # 2-07

        for loc in self._locations:
            loc_obj, _ = Location.objects.get_or_create(name=loc)
            user.locations.add(loc_obj)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class UserDetailSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field="name"
    )
    #author = serializers.PrimaryKeyRelatedField(read_only=True) # user-> Ad ??
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "password", "role", "age", "locations"]
        #exclude
    def is_valid(self, raise_exception=False):
        self._locations = self.initial_data.pop("locations")
        return super().is_valid(raise_exception=raise_exception)
    def save(self):
        user = super().save()
        for loc in self._locations:
            loc_obj, _ = Location.objects.get_or_create(name=loc)
            user.locations.add(loc_obj)
        user.save()
        return user


class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]


# CRUD for Locations - ?
class LocationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class LocationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "name"]

class LocationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class LocationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class LocationDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id"]



# CRUD for Selections - ?
class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'

class SelectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'

class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name"]

class SelectionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'

class SelectionUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'

class SelectionDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id"]