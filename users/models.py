from django.db import models
from django.contrib.auth.models import AbstractUser # 30-06 ...
from django.core.exceptions import ValidationError # from pydantic import ValidationError
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


USER_MIN_AGE = 9

def check_birth_date(value: date):
    delta_years = relativedelta(date.today(), value).years
    if delta_years < USER_MIN_AGE:
        raise ValidationError(
            '%(value)s - too yang!',
            params={'value': value},
        )


class Location(models.Model):
    name = models.CharField(max_length=40)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.name

#class User(models.Model):
class User(AbstractUser):# 30-06 ...
    MEMBER = "member"
    MODERATOR ="moderator"
    ADMIN = "admin" # ... 30-06
    ROLES = [
        ("member", "Пользователь"),
        ("moderator", "Модератор"),
        ("admin", "Админ"),
    ]
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=20, db_index=True, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=9, choices=ROLES, default="member")
    age = models.PositiveIntegerField(null=True)
    locations = models.ManyToManyField(Location)
    birth_date = models.DateField(validators=[check_birth_date], null=True) # 2-07
    email = models.EmailField(unique=True, null=True) # 2-07

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

    def __str__(self):
        return self.username
