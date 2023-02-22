from django.contrib import admin

from .models import Ingredient, Menu, MenuCategory, MenuItem, Restaurant


class MenuAdmin(admin.ModelAdmin):
    readonly_fields = ("slug", "uuid")


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]


admin.site.register(Restaurant)
admin.site.register(Ingredient)
admin.site.register(MenuCategory)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
