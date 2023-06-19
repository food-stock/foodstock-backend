from rest_framework import viewsets
from .models import User, Food, Categories, Stock, Entities
from .serializers import UserSerializer, FoodSerializer, CategoriesSerializer, StockSerializer, EntitiesSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer


class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class EntitiesViewSet(viewsets.ModelViewSet):
    queryset = Entities.objects.all()
    serializer_class = EntitiesSerializer
