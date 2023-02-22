from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel
from apps.restaurants.models import (Ingredient)

User = get_user_model()


class UserAllergen(TimeStampedUUIDModel):
    user = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, related_name="myallergens"
    )
    allergen = models.ManyToManyField(Ingredient, related_name="userallergens")

    class Meta:
        verbose_name = _("User Allergen")
        verbose_name_plural = _("User Allergens")
