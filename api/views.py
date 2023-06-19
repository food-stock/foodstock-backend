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
    queryset = Entities.objects.select_related('food', 'stock').all()
    serializer_class = EntitiesSerializer


##CUSTOM ENDPOINTS
from django.http import JsonResponse, HttpResponse
from django.db.models import Q

def get_categories_for_stock(request, stock_id):
    category_ids = Entities.objects.filter(stock_id=stock_id).values_list('food__category_id', flat=True).distinct()
    categories = Categories.objects.filter(id__in=category_ids).values()
    return JsonResponse({'categories': list(categories)})

def get_accessible_stocks_for_user(request, user_id):
    print(Stock.objects.filter(Q(owner=user_id) | Q(can_access=user_id)).values().count())
    stocks = Stock.objects.filter(Q(owner=user_id) | Q(can_access=user_id)).values()
    return JsonResponse({'stocks': list(stocks)})

def get_entities_for_stock_and_category(request, stock_id, category_id):
    entities = Entities.objects.filter(stock_id=stock_id, food__category_id=category_id).values('id', 'food__name','date_of_consumption','quantity')
    return JsonResponse({'entities': list(entities)})

def get_entity_by_id(request, food_id, user_id):
    try:
        entity = Entities.objects.filter(
            Q(food__id=food_id) & (Q(stock__owner=user_id) | Q(stock__can_access=user_id))
        ).values(
            'id',
            'stock__name',
            'date_of_consumption',
            'quantity',
            'date_of_purchase'
        )
        food_info = Entities.objects.filter(food__id=food_id).values('food__name', 'food__picture', 'food__description','food__category__name').distinct()
        return JsonResponse({'entity': list(entity),"food_info":list(food_info)})
    except Entities.DoesNotExist:
        return JsonResponse({'error': 'Entity does not exist'})

def search(request, query):
    food = Food.objects.filter(name__icontains=query).values()
    return JsonResponse({'food': list(food)})

def search_stocks_with_access(request, query, user_id):
    stocks = Stock.objects.filter(
        Q(name__icontains=query) & (Q(owner=user_id) | Q(can_access=user_id))
    ).values()
    return JsonResponse({'stocks': list(stocks)})

def create_entity(request,stock_id, food_id, quantity, date_of_consumption):
    stock = Stock.objects.get(id=stock_id)
    food = Food.objects.get(id=food_id)
    category = Categories.objects.get(id=food.category_id)
    query = Entities.objects.create(
        stock=stock,
        food=food,
        quantity=quantity,
        date_of_consumption=date_of_consumption
    )
    query.save()
    return HttpResponse("Entity created successfully")
        
    