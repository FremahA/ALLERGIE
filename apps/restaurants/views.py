import logging

import django_filters
from django.db.models import query
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .exceptions import RestaurantNotFound
from .models import Restaurant, Ingredient, Menu, MenuCategory, MenuItem
from .serializers import (RestaurantSerializer, MenuCategorySerializer, MenuItemSerializer, 
                          IngredientSerializer, RestaurantCreateSerializer, MenuSerializer)

logger = logging.getLogger(__name__)


class MenuFilter(django_filters.FilterSet):
    ingredient = django_filters.Filter(
        field_name="ingredient", lookup_expr="in"
    )

    class meta:
        model = MenuItem
        fields = ["ingredient"]


class ListAllRestaurantsAPIView(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all().order_by("-created_at")
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = ["name"]
    ordering_fields = ["created_at"]


class ListAllMenuItemsAPIView(generics.ListAPIView):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all().order_by("category")
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_class = MenuFilter
    search_fields = ["category", "name", "ingredient"]


class UserRestaurantsAPIView(generics.ListAPIView):
    serializer_class = RestaurantSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
        
    search_fields = ["name", "address"]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        user = self.request.user
        queryset = Restaurant.objects.filter(user=user).order_by("-created_at")
        return queryset


class MenuView(generics.ListAPIView):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()


class MenuCategoryView(generics.ListAPIView):
    serializer_class = MenuCategorySerializer
    queryset = MenuCategory.objects.all()


class IngredientView(generics.ListAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


@api_view(["PUT"])
@permission_classes([permissions.IsAuthenticated])
def update_restaurant_api_view(request, uuid):
    try:
        restaurant = Restaurant.objects.get(uuid=uuid)
    except Restaurant.DoesNotExist:
        raise RestaurantNotFound

    user = request.user
    if restaurant.user != user:
        return Response(
            {"error": "You can't update or edit a restaurant that does not belong to you."},
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == "PUT":
        data = request.data
        serializer = RestaurantSerializer(restaurant, data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@permission_classes([permissions.IsAuthenticated])
@api_view(["POST"])
def create_restaurant_api_view(request):
    user = request.user
    data = request.data
    data["user"] = request.user.id
    serializer = RestaurantCreateSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        logger.info(
            f"New restaurant {serializer.data.get('name')} created by {user.username}"
        )
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([permissions.IsAuthenticated])
def delete_restaurant_api_view(request, uuid):
    try:
        restaurant = Restaurant.objects.get(uuid=uuid)
    except Restaurant.DoesNotExist:
        raise RestaurantNotFound

    user = request.user
    if restaurant.user != user:
        return Response(
            {"error": "You can't delete a restaurant that doesn't belong to you."},
            status=status.HTTP_403_FORBIDDEN,
        )

    if request.method == "DELETE":
        delete_operation = restaurant.delete()
        data = {}
        if delete_operation:
            data["success"] = "Deletion was successful"
        else:
            data["failure"] = "Deletion failed"
        return Response(data=data)
        
class RestaurantSearchAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RestaurantCreateSerializer

    def post(self, request):
        queryset = Restaurant.objects.all()
        data = self.request.data

        name = data["name"]
        queryset = queryset.filter(name__icontains=name)

        address = data["address"]
        queryset = queryset.filter(address__icontains=address)

        serializer = RestaurantSerializer(queryset, many=True)

        return Response(serializer.data)