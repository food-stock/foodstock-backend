from django.contrib import admin
from .models import *

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
    
@admin.register(PushSubscription)
class PushSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'endpoint')
    
@admin.register(Push)
class PushAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_user_only', 'user', 'is_group', 'group', 'date', 'title', 'body')

@admin.register(JoinProposals)
class JoinProposalsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
