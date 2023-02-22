from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedUUIDModel

User = get_user_model()


class Restaurant(TimeStampedUUIDModel):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="restaurants"
    )
    name = models.CharField(
        verbose_name=_("Restaurant Name"), null=False, max_length=200
    )
    address = models.CharField(
        verbose_name=_("Restaurant Address"), null=False, max_length=150
    )

    class Meta:
        verbose_name = _("Restaurant")
        verbose_name_plural = _("Restaurants")

    def __str__(self):
        return self.name


class Menu(TimeStampedUUIDModel):
    restaurant = models.OneToOneField(
        Restaurant, on_delete=models.CASCADE, related_name="restaurantmenu"
    )
    title = models.CharField(verbose_name=_("Menu Title"), max_length=250, blank=False)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        super(Menu, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")

    def __str__(self):
        return f"{self.restaurant}'s menu"


class MenuCategory(TimeStampedUUIDModel):
    menu = models.ForeignKey(
        Menu, related_name="menucategory", on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name=_("Category Name"), max_length=100, null=True, blank=True
    )

    class Meta:
        verbose_name = _("Menu Category")
        verbose_name_plural = _("Menu Categories")

    def __str__(self):
        return self.name


class Ingredient(TimeStampedUUIDModel):
    name = models.CharField(verbose_name=_("Ingredient Name"), max_length=100)

    class Meta:
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")

    def __str__(self):
        return self.name


class MenuItem(TimeStampedUUIDModel):
    name = models.CharField(verbose_name=_("Dish Name"), max_length=100)
    description = models.TextField(
        verbose_name=_("Description"), default="say something about your dish"
    )
    category = models.ManyToManyField(MenuCategory, related_name="menuitemcategory")
    ingredient = models.ManyToManyField(Ingredient, related_name="menuitemingredients")
    price = models.IntegerField(verbose_name=_("Dish Price"))

    def save(self, *args, **kwargs):
        self.description = str.capitalize(self.description)
        super(MenuItem, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Menu Item")
        verbose_name_plural = _("Menu Items")

    def __str__(self):
        return self.name
