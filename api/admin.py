from django.contrib import admin
from .models import User,  Food, Categories, Stock, Entities

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_personal', 'owner', 'name')

@admin.register(Entities)
class EntitiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'food', 'stock', 'quantity', 'date_of_consumption')
