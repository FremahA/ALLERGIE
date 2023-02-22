from rest_framework import serializers

from .models import UserAllergen
from apps.restaurants.serializers import IngredientSerializer

class UserAllergenSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    allergen = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = UserAllergen
        fields = ["user", "allergen", "uuid", "id"]

    def get_user(self, obj):
        return obj.user.username

    def get_allergen(self, obj):
            return obj.allergen.ingredient.name


class UserAllergenCreateSerializer(serializers.ModelSerializer):
    allergen = IngredientSerializer(many=True)

    class Meta:
        model = UserAllergen
        fields = ["user", "allergen", "uuid", "id"]

    def update(self, instance, validated_data):
        allergen = validated_data.pop('allergen')
        instance.allergen.set(allergen)
        return instance