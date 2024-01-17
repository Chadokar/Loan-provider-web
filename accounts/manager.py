from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Please enter a valid email address"))

    def create_user(self, id, first_name, last_name, password, age, monthly_salary, phone_number, **extra_fields):
        # if email:
        #     email = self.normalize_email(email)
        #     self.email_validator(email)
        # else:
        #     raise ValidationError(
        #         {"email": _("An email address is required")})

        if not first_name:
            raise ValidationError(
                {"first_name": _("First name is required")})
        if not last_name:
            raise ValidationError(
                {"last_name": _("Last name is required")})
        if not age:
            raise ValidationError({"age": _("Age is required")})
        if not monthly_salary:
            raise ValidationError(
                {"monthly_salary": _("Monthly Salary is required")})
        if not phone_number:
            raise ValidationError(
                {"phone_number": _("Phone Number is required")})

        user = self.model(id=id, first_name=first_name,
                          last_name=last_name, age=age, monthly_salary=monthly_salary, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id, first_name, last_name, password,  age, monthly_salary, phone_number, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is staff must be true for admin user"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("is superuser must be true for admin user"))

        user = self.create_user(
            id, first_name, last_name, password, age, monthly_salary, phone_number, **extra_fields
        )

        user.save(using=self._db)

        return user
