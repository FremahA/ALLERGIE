from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListAllRestaurantsAPIView.as_view(), name="all-restaurants"),
    path("userrestaurants/", views.UserRestaurantsAPIView.as_view(), name="user-restaurants"),
    path("menus/", views.MenuView.as_view(), name="all-menus"),
    path("ingredients/", views.IngredientView.as_view(), name="all-ingredients"),
    path("menucategories/", views.MenuCategoryView.as_view(), name="all-menu-categories"),
    path("dishes/", views.ListAllMenuItemsAPIView.as_view(), name="all-dishes"),
    path("search/", views.RestaurantSearchAPIView.as_view(), name="restaurant-search"),
    path("newrestaurant/", views.create_restaurant_api_view, name="restaurant-create"),
    path("<uuid:uuid>/", views.update_restaurant_api_view, name="update-restaurant"),
    path("<slug:slug>/", views.delete_restaurant_api_view, name="delete-restaurant"),
]