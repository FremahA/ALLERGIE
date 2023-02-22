from django.contrib import admin
from .models import UserAllergen

class UserAllergenAdmin(admin.ModelAdmin):
    list_display = [ "user", "uuid"]
    readonly_field = ('uuid')

admin.site.register(UserAllergen, UserAllergenAdmin)