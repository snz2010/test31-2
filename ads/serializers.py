from rest_framework import serializers
from ads.models import Ad, Category, Selection

# 3-07
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# 2-07
class NameLenValid:
    def __call__(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Name is less then 10 chars")

# 2-07
class NotTrueValidator:
    def __call__(self, value):
        if value:
            raise serializers.ValidationError("New Ad cant be create")

# 2-07
class AdCreateSerializers(serializers.ModelSerializer):
    is_published = serializers.BooleanField(validators=[NotTrueValidator()])
    name = serializers.CharField(validators=[NameLenValid()])
    class Meta:
        model = Ad
        fields = '__all__'

class AdSerializer(serializers.ModelSerializer):
    author = serializers.CharField() # можно убрать?
    category = serializers.CharField() # можно убрать?
    class Meta:
        model = Ad                                                 # по умолчанию ВЫВОДИТ ИНДЕКС!
        fields = ["id", "name", "price", "description", "author", "category"]



# 2-07
class AdDetailSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='first_name',
        read_only=True,
    )

    class Meta:
        model = Ad                                                 # ВЫВОДИТ ИНДЕКС!
        fields = '__all__'

# 3-07
class SelectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = ["id", "name"]
# 07-07
class SelectionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'
# 07-07
class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'