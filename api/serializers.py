from rest_framework import serializers
from .models import User, Food, Categories, Stock, Entities

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'fname', 'lname', 'dob', 'email']

class FoodSerializer(serializers.ModelSerializer):
    entities_related = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Food
        fields = ['id', 'name', 'description', 'entities_related']

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'name', 'description']

class StockSerializer(serializers.ModelSerializer):
    owned_stocks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    accessible_stocks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'is_personal', 'owner', 'can_access', 'name', 'owned_stocks', 'accessible_stocks']

class EntitiesSerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source='food.name', read_only=True)
    
    class Meta:
        model = Entities
        fields = ['id', 'food', 'food_name', 'stock', 'quantity', 'date_of_consumption', 'category']
