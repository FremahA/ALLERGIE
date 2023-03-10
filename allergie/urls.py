from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    path("api/v1/profile/", include("apps.profiles.urls")),
    path("api/v1/restaurants/", include("apps.restaurants.urls")),
    path("api/v1/feed/", include("apps.feed.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Allergie Admin"
admin.site.site_title = "Allergie Admin Portal"
admin.site.index_title = "  Welcome to the Allergie administration"
