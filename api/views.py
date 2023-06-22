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
    entities = Entities.objects.filter(stock_id=stock_id, food__category_id=category_id).values('id', 'food_id','food__name','date_of_consumption','quantity')
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
            'date_of_purchase',
            'stock__id'
        )
        food_info = Entities.objects.filter(food__id=food_id).values('food__name', 'food__picture','food__category__name').distinct()
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
        
from .hash import Fhash
    
def update_entity_quantity(request, entity_id, quantity):
    entity = Entities.objects.get(id=entity_id)
    entity.quantity = quantity
    entity.save()
    return JsonResponse(data={"status":200,"message": "Entity updated successfully"}, status=200, safe=False)

def create_user(request, username, fname, lname, dob, email, password):
    query = User.objects.create(
        username=username,
        fname=fname,
        lname=lname,
        dob=dob,
        email=email,
        hashed_password=Fhash(password)
    )
    query.save()
    return HttpResponse("User created successfully")

def search_product_among_stocks(request, query, user_id):
    entities = Entities.objects.filter(
        Q(food__name__icontains=query) & (Q(stock__owner=user_id) | Q(stock__can_access=user_id))
    ).values(
        'food__name',
        'food__id',
        'food__picture',
    ).distinct()
    return JsonResponse({'entities': list(entities)})

def rename_stock(request, stock_id, new_name):
    stock = Stock.objects.get(id=stock_id)
    stock.name = new_name
    stock.save()
    return JsonResponse(data={"status":200,"message": "Stock renamed successfully"}, status=200, safe=False)

def set_stock_default(request, stock_id, is_default):
    if is_default == "true":
        is_default = True
    if is_default == "false":
        is_default = False
    stock = Stock.objects.get(id=stock_id)
    stock.is_default = is_default
    stock.save()
    return JsonResponse(data={"status":200,"message": "Stock set as default successfully"}, status=200, safe=False)

def delete_stock(request, stock_id):
    stock = Stock.objects.get(id=stock_id)
    stock.delete()
    return JsonResponse(data={"status":200,"message": "Stock deleted successfully"}, status=200, safe=False)

def get_users_accessing_stock(request, stock_id):
    users = Stock.objects.get(id=stock_id).can_access.values()
    return JsonResponse({'users': list(users)})

def remove_user_access_to_stock(request, stock_id, user_id):
    stock = Stock.objects.get(id=stock_id)
    stock.can_access.remove(user_id)
    return JsonResponse(data={"status":200,"message": "User removed successfully"}, status=200, safe=False)

def add_user_access_to_stock(request, stock_id, user_id):
    stock = Stock.objects.get(id=stock_id)
    stock.can_access.add(user_id)
    return JsonResponse(data={"status":200,"message": "User added successfully"}, status=200, safe=False)

def search_for_users(request, query, stock_id):
    users = User.objects.filter(username__icontains=query).exclude(id__in=Stock.objects.get(id=stock_id).can_access.values_list('id', flat=True)).values()
    return JsonResponse({'users': list(users)})