# Create your models here.
import datetime
from users.models import User
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator



class Category(models.Model):
    slug = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(5)]) # 1-07
    name = models.CharField(max_length=20, db_index=True)
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
    def __str__(self):
        return self.name


class Ad(models.Model):
    STATUS = [
        ("true", "опубликовано"),
        ("false", "не опубликовано")
    ]
    #name = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=20, unique=True, validators=[MinLengthValidator(10)], null=True) # 1-07
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    price = models.PositiveIntegerField(validators=[MinValueValidator(0)]) # 1-07
    description = models.TextField(max_length=1000, null=True, blank=True)
    #is_published = models.CharField(max_length=5, choices=STATUS, default="false")
    is_published = models.BooleanField(default=False) # 1-07
    image = models.ImageField(upload_to="ads/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    #created = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
    def __str__(self):
        return self.name

    # 22-06
    @property
    def username(self):
        return self.author.username if self.author else None



class Selection(models.Model): # 30-06 ...
    name = models.CharField(max_length=20, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField('Ad') # почему - в кавычках????                07-07-22
    class Meta:
        verbose_name = "Выборка"
        verbose_name_plural = "Выборки"
    def __str__(self):
        return self.name