from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import Food, Categories, Stock, Entities, PushSubscription, Push
from .serializers import UserSerializer, FoodSerializer, CategoriesSerializer, StockSerializer, EntitiesSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Count, Q
from django.shortcuts import render
from foodstockdjango.settings import WEBPUSH_SETTINGS
from django.http import HttpResponse
from .parse import *
import json

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


## CUSTOM ENDPOINTS
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_token(request):
    user_id = request.user.id
    print("ZAAAAAAAAAAAAAAAAAAAAAAAA")
    if user_id == request.GET.get('user_id'):
        return Response({'message': 'ok'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_categories_for_stock(request, stock_id):
    category_ids = Entities.objects.filter(stock_id=stock_id).values_list('food__category_id', flat=True).distinct()
    categories = Categories.objects.filter(id__in=category_ids).values()
    return Response({'categories': list(categories)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_accessible_stocks_for_user(request, user_id):
    if user_id != request.user.id:
        return Response({'error': 'Invalid user id'})

    stocks = Stock.objects.filter(Q(owner=user_id) | Q(can_access=user_id)).annotate(entity_count=Count('entities')).order_by('-is_default', '-entity_count').values()

    return Response({'stocks': list(stocks)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_entities_for_stock_and_category(request, stock_id, category_id):
    entities = Entities.objects.filter(Q(quantity__gt=0),stock_id=stock_id, food__category_id=category_id).values('id', 'food_id','food__name','date_of_consumption','quantity')
    return Response({'entities': list(entities)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_entity_by_id(request, food_id, user_id):
    user_id = request.user.id
    try:
        entity = Entities.objects.filter(
            Q(food__id=food_id) & (Q(stock__owner=user_id) | Q(stock__can_access=user_id) & Q(quantity__gt=0) )
        ).values(
            'id',
            'stock__name',
            'date_of_consumption',
            'quantity',
            'date_of_purchase',
            'stock__id'
        )
        food_info = Entities.objects.filter(food__id=food_id).values('food__name', 'food__picture','food__category__name').distinct()
        return Response({'entity': list(entity), "food_info": list(food_info)})
    except Entities.DoesNotExist:
        return Response({'error': 'Entity does not exist'})

@api_view(['GET'])
def search(request, query):
    food = Food.objects.filter(name__icontains=query).values()
    return Response({'food': list(food)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_stocks_with_access(request, query,user_id):
    if user_id != request.user.id:
        return Response({'error': 'Invalid user id'})
    user_id = request.user.id
    stocks = Stock.objects.filter(
        Q(name__icontains=query) & (Q(owner=user_id) | Q(can_access=user_id))
    ).values()
    return Response({'stocks': list(stocks)}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_entity(request, stock_id, food_id, quantity, date_of_consumption):
    if stock_id not in Stock.objects.filter(Q(owner=request.user.id) | Q(can_access=request.user.id)).values_list('id', flat=True):
        return Response({'error': 'Unauthorized'})
    if Entities.objects.filter(stock_id=stock_id, food_id=food_id, date_of_consumption=date_of_consumption).exists():
        return Response({'error': 'Entity already exists'})
    stock = Stock.objects.get(id=stock_id)
    food = Food.objects.get(id=food_id)
    query = Entities.objects.create(
        stock=stock,
        food=food,
        quantity=quantity,
        date_of_consumption=date_of_consumption
    )
    query.save()
    return Response("Entity created successfully")

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_entity_quantity(request, entity_id, quantity):
    user_id = request.user.id
    entity = Entities.objects.get(id=entity_id)
    quantity = float(quantity)

    if entity.stock.owner.id != user_id and user_id not in entity.stock.can_access.values_list('id', flat=True):
        return Response({'error': 'Unauthorized'})

    entity.quantity = quantity
    entity.save()
    return Response("Entity updated successfully", status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_product_among_stocks(request, query, user_id):
    if user_id != request.user.id:
        return Response({'error': 'Invalid user id'})
    entities = Entities.objects.filter(
        Q(food__name__icontains=query) & (Q(stock__owner=user_id) | Q(stock__can_access=user_id) & Q(quantity__gt=0))
    ).values(
        'food__name',
        'food__id',
        'food__picture',
    ).distinct()[:5]
    return Response({'entities': list(entities)}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rename_stock(request, stock_id, new_name):
    user_id = request.user.id
    stock = Stock.objects.get(id=stock_id)

    if stock.owner.id != user_id:
        return Response({'error': 'Unauthorized'})

    stock.name = new_name
    stock.save()
    return Response("Stock renamed successfully", status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_stock_default(request, stock_id, is_default):
    user_id = request.user.id

    if is_default not in ["true", "false"]:
        return Response({'error': 'Invalid value for is_default'})

    stock = Stock.objects.get(id=stock_id)

    if stock.owner.id != user_id:
        return Response({'error': 'Unauthorized'})

    stock.is_default = is_default == "true"
    stock.save()
    return Response("Stock set as default successfully", status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_stock_personal(request,stock_id, is_personal):
    user_id = request.user.id

    if is_personal not in ["true", "false"]:
        return Response({'error': 'Invalid value for is_personal'})

    stock = Stock.objects.get(id=stock_id)

    if stock.owner.id != user_id:
        return Response({'error': 'Unauthorized'})

    if is_personal == "true":
        stock.is_personal = True
        stock.can_access.clear()
    else:
        stock.is_personal = False
    stock.save()
    return Response("Stock set as personal successfully", status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_stock(request, stock_id):
    user_id = request.user.id
    stock = Stock.objects.get(id=stock_id)

    if stock.owner.id != user_id:
        return Response({'error': 'Unauthorized'})

    stock.delete()
    return Response("Stock deleted successfully", status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_accessing_stock(request, stock_id):
    user_id = request.user.id
    stock = Stock.objects.get(id=stock_id)

    if stock.owner.id != user_id:
        return Response({'error': 'Unauthorized'})

    users = stock.can_access.values()
    users = [user for user in users if user['id'] != stock.owner.id]
    return Response({'users': list(users)}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_user_access_to_stock(request, stock_id, user_id):
    owner_id = request.user.id
    stock = Stock.objects.get(id=stock_id)

    if stock.owner.id != owner_id:
        return Response({'error': 'Unauthorized'})

    stock.can_access.remove(user_id)
    return Response("User removed successfully", status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_access_to_stock(request, stock_id, user_id):
    owner_id = request.user.id
    stock = Stock.objects.get(id=stock_id)

    if stock.owner.id != owner_id:
        return Response({'error': 'Unauthorized'})

    stock.can_access.add(user_id)
    return Response("User added successfully", status=status.HTTP_200_OK)

@api_view(['GET'])
def search_for_users(request, query, stock_id):
    users = User.objects.filter(username__icontains=query).exclude(id__in=Stock.objects.get(id=stock_id).can_access.values_list('id', flat=True)).values()
    return Response({'users': list(users)})

@api_view(['POST'])
def register_user(request):
    user = User.objects.create(
        username=request.data.get('username'),
        email=request.data.get('email'),
        first_name=request.data.get('first_name'),
        last_name=request.data.get('last_name'),
    )
    user.set_password(request.data.get('password'))
    user.save()
    stock = Stock.objects.create(
        name="Maison",
        owner = user,
        is_default = True,
        is_personal = True,
    )
    stock.save()
    user = User.objects.get(username=request.data.get('username'))
    return Response({'user_id': user.id}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_product_from_barcode(request, barcode):
    if Food.objects.filter(barcode=barcode).exists():
        food = Food.objects.get(barcode=barcode)
        return Response({'food': food.id}, status=status.HTTP_200_OK)
    else:
        url_img, title = find_image_by_barcode(barcode)
        food = Food.objects.create(
            barcode=barcode,
            title=title,
            url_img=url_img,
        )
        food.save()
        return Response({'food': food.id}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_latest_webpush(request, user_id):
    user = User.objects.get(id=user_id)
    if user_id != request.user.id:
        return Response({'error': 'Invalid user id'})
    latest_webpush = Push.objects.filter(is_user_only=True,user=user).order_by('-date').values('title', 'body', 'date')[:5]
    return Response({'push': latest_webpush}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_subscription(request):
    user = User.objects.get(id=request.user.id)
    subscription = PushSubscription.objects.create(
        user=user,
        endpoint=request.GET.get('endpoint'),
        p256dh=request.GET.get('p256dh'),
        auth=request.GET.get('auth')
    )
    subscription.save()
    return Response({'subscription': subscription.id}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_subscription(request):
    endpoint = request.GET.get('endpoint')
    print(endpoint)
    subscription = PushSubscription.objects.get(endpoint=endpoint)
    subscription.delete()
    return Response({'message':'ok'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_id(request):
    return Response({'id': request.user.id}, status=status.HTTP_200_OK)

from pywebpush import webpush, WebPushException

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_notif(request):
    suscriptions = PushSubscription.objects.all().filter(user__id=request.user.id)
    for suscription in suscriptions:
        try:
            webpush(
                subscription_info={
                    "endpoint": suscription.endpoint,
                    "keys": {
                        "p256dh": suscription.p256dh,
                        "auth": suscription.auth
                    }},
                data= json.dumps({'head': 'TestH', 'body': 'TestBody','click_data':"/login"}),
                vapid_private_key=WEBPUSH_SETTINGS['VAPID_PRIVATE_KEY'],
                vapid_claims={
                        "sub": "mailto:" + WEBPUSH_SETTINGS['VAPID_ADMIN_EMAIL'],
                    }
            )
            query = Push.objects.create(
                title="Test",
                body="Test",
                is_user_only=True,
                user=request.user,
            )
            query.save()
        except WebPushException as ex:
            print("I'm sorry, Dave, but I can't do that: {}", repr(ex))
            # Mozilla returns additional information in the body of the response.
            if ex.response and ex.response.json():
                extra = ex.response.json()
                print("Remote service replied with a {}:{}, {}",
                    extra.code,
                    extra.errno,
                    extra.message
                    )
    return Response({'message': 'ok'}, status=status.HTTP_200_OK)

def send_push_user(user_id,head,body,click_data):
    subs = PushSubscription.objects.all().filter(user__id=user_id)
    for sub in subs:
        try:
            webpush(
                subscription_info={
                    "endpoint": sub.endpoint,
                    "keys": {
                        "p256dh": sub.p256dh,
                        "auth": sub.auth
                    }},
                data= json.dumps({'head': head, 'body': body,'click_data': click_data}),
                vapid_private_key=WEBPUSH_SETTINGS['VAPID_PRIVATE_KEY'],
                vapid_claims={
                        "sub": "mailto:" + WEBPUSH_SETTINGS['VAPID_ADMIN_EMAIL'],
                    }
            )
            query = Push.objects.create(
                title=head,
                body=body,
                is_user_only=True,
                user=User.objects.get(id=user_id),
            )
            query.save()
        except WebPushException as ex:
            print("I'm sorry, Dave, but I can't do that: {}", repr(ex))
            if ex.response and ex.response.json():
                extra = ex.response.json()
                print("Remote service replied with a {}:{}, {}",extra.code,extra.errno,extra.message)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_stock(request,user_id):
    user_id = request.user.id
    if user_id != request.user.id:
        return Response({'error': 'Invalid user id'})
    stock = Stock.objects.create(
        name=request.GET.get('name'),
        owner=User.objects.get(id=user_id),
        is_default=False,
        is_personal=False,
    )
    stock.save()
    return Response({'stock': stock.id}, status=status.HTTP_200_OK)