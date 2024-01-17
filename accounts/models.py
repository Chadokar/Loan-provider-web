from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from .manager import UserManager
# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    # email = models.EmailField(
    #     max_length=255, unique=True, verbose_name=_("Email Address"))
    id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    phone_number = models.PositiveIntegerField(
        validators=[MinValueValidator(
            1000000000), MaxValueValidator(9999999999)], null=False)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(
            1), MaxValueValidator(9999999999)], null=False)

    monthly_salary = models.PositiveIntegerField(
        verbose_name=_("Monthly Salary"), null=False)
    approved_limit = models.PositiveIntegerField(
        verbose_name=_("Monthly Salary"), null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "id"
    REQUIRED_FIELDS = ['first_name', 'last_name',
                       'age', 'monthly_salary', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.first_name+' '+self.last_name

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
