from rest_framework import serializers

from .models import Restaurant, Ingredient, Menu, MenuCategory, MenuItem

class RestaurantSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    name = serializers.JSONField()

    class Meta:
        model = Restaurant
        fields = ["user", "name", "uuid" "address"]
    
    
    def get_user(self, obj):
        return obj.user.username


class RestaurantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ["user", "name", "address", "uuid"]


class MenuSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    class Meta:
        model = Menu
        fields = ["restaurant", "title", "slug"]


class MenuCategorySerializer(serializers.ModelSerializer):
    menu = MenuSerializer(read_only=True)
    class Meta:
        model = MenuCategory
        fields = ["name", "menu",]


class IngredientSerializer(serializers.ModelSerializer):
    name = serializers.JSONField()
    class Meta:
        model = Ingredient
        fields = ["name", "id"] 


class MenuItemIngredientSerializer(serializers.ModelSerializer):
    name = serializers.JSONField()
    class Meta:
        model = Ingredient
        fields = ["name"]


class MenuItemCategorySerializer(serializers.ModelSerializer):
    name = serializers.JSONField()
    class Meta:
        model = MenuCategory
        fields = ["name"]


class MenuItemSerializer(serializers.ModelSerializer):
    category = MenuItemCategorySerializer(many=True)
    ingredient = MenuItemIngredientSerializer(many=True)
    class Meta:
        model = MenuItem
        exclude = ["updated_at", "id"] 

    def get_category(self, obj):
        return obj.category.category.name

    def get_ingredient(self, obj):
        return obj.ingredient.ingredient.name