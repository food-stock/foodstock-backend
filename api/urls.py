from rest_framework import routers
from django.urls import path
from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'food', FoodViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'stock', StockViewSet)
router.register(r'entities', EntitiesViewSet)

urlpatterns = router.urls 
