"""
URL configuration for foodstockdjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from rest_framework import routers, serializers, viewsets
from django.contrib import admin
from api.urls import router as api_router
from api.views import *

router = routers.DefaultRouter()
router.registry.extend(api_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('get_categories_for_stock/<int:stock_id>', get_categories_for_stock),
    path('stocks/user/<int:user_id>/', get_accessible_stocks_for_user),   
    path('get_entities_for_stock_and_category/<int:stock_id>/<int:category_id>', get_entities_for_stock_and_category),
    path('get_entity_by_id/<int:food_id>/<int:user_id>', get_entity_by_id),
    path('search/<str:query>', search),
    path('search_stocks_with_access/<str:query>/<int:user_id>', search_stocks_with_access),
    path('create_entity/<stock_id>/<food_id>/<quantity>/<date_of_consumption>', create_entity),
    path('update_entity_quantity/<int:entity_id>/<quantity>', update_entity_quantity),
    path('create_user/<username>/<fname>/<lname>/<dob>/<email>/<password>', create_user),
]
