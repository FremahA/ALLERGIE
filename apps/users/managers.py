from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("You must provide a valid email address"))

    def create_user(self, restaurant_name, email, password, **extra_fields):
        if not restaurant_name:
            raise ValueError(_("Users must submit restaurant name"))
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Base User Account: An email address is required"))

        user = self.model(
            restaurant_name=restaurant_name,
            email=email,
            **extra_fields
        )

        user.setpassword(password)
        user.save(using=self.db)
        return user
