from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from api.urls import router as api_router
from api.views import *

router = routers.DefaultRouter()
router.registry.extend(api_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('get_categories_for_stock/<int:stock_id>/', get_categories_for_stock),
    path('stocks/user/<int:user_id>/', get_accessible_stocks_for_user),
    path('get_entities_for_stock_and_category/<int:stock_id>/<int:category_id>/', get_entities_for_stock_and_category),
    path('get_entity_by_id/<int:food_id>/<int:user_id>/', get_entity_by_id),
    path('search/<str:query>/', search),
    path('search_stocks_with_access/<str:query>/<int:user_id>/', search_stocks_with_access),
    path('create_entity/<int:stock_id>/<int:food_id>/<int:quantity>/<str:date_of_consumption>/', create_entity),
    path('update_entity_quantity/<int:entity_id>/<int:quantity>/', update_entity_quantity),
    path('search_product_among_stocks/<str:query>/<int:user_id>/', search_product_among_stocks),
    path('rename_stock/<int:stock_id>/<str:new_name>/', rename_stock),
    path('set_stock_default/<int:stock_id>/<str:is_default>/', set_stock_default),
    path('set_stock_personal/<int:stock_id>/<str:is_personal>/', set_stock_personal),
    path('delete_stock/<int:stock_id>/', delete_stock),
    path('get_users_accessing_stock/<int:stock_id>/', get_users_accessing_stock),
    path('remove_user_access_to_stock/<int:stock_id>/<int:user_id>/', remove_user_access_to_stock),
    path('add_user_access_to_stock/<int:stock_id>/<int:user_id>/', add_user_access_to_stock),
    path('search_for_users/<str:query>/<int:stock_id>/', search_for_users),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register_user)
]
