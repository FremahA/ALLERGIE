import logging

from django.db.models import query

from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import  UserAllergenCreateSerializer, UserAllergenSerializer
from .models import UserAllergen

from apps.restaurants.models import MenuItem
from apps.restaurants.serializers import MenuItemSerializer

logger = logging.getLogger(__name__)


class UserAllergenViewset(viewsets.ModelViewSet):
    queryset = UserAllergen.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request):
        data = request.data
        data["user"] = request.user.id
        serializer_class = UserAllergenCreateSerializer(data=data)
        if serializer_class.is_valid():
            serializer_class.save
        return Response(serializer_class.data)
        
    def update(self, request, pk=None):
        instance = UserAllergen.objects.get(user=request.user)
        serializer_class = UserAllergenCreateSerializer(instance, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save
        return Response(serializer_class.data)

    def list(self, request):
        queryset = UserAllergen.objects.all()
        serializer_class = UserAllergenSerializer(queryset, many=True)
        return Response(serializer_class.data)


class UserFeedAPIView(generics.ListAPIView):
    serializer_class = MenuItemSerializer

    def get(self, request):
        user = request.user
        allergen = UserAllergen.objects.get(user=user).allergen.all()
        queryset = MenuItem.objects.exclude(ingredient__in=allergen)
        serializer = MenuItemSerializer(queryset, many=True)
        return Response(serializer.data)