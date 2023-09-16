from django.db import models
from django.contrib.auth.models import User, Group
    
class Food(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, related_name='foods',default=1)
    picture = models.CharField(max_length=200, blank=True)
    barcode = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Stock(models.Model):
    is_personal = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_stocks')
    can_access = models.ManyToManyField(User, related_name='accessible_stocks', blank=True)
    name = models.CharField(max_length=100)
    is_default = models.BooleanField(null=True, blank=True, default=False)
    
    def __str__(self):
        return self.name


class Entities(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='entities_related')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='entities')
    quantity = models.FloatField()
    date_of_consumption = models.DateField()
    date_of_purchase = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.food.name

class PushSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='push_subscriptions') 
    endpoint = models.CharField(max_length=500,blank=True,null=True)
    p256dh = models.CharField(max_length=500,blank=True,null=True)
    auth = models.CharField(max_length=500,blank=True,null=True)

class Push(models.Model):
    is_user_only = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pushesuser',blank=True, null=True)
    is_group = models.BooleanField(default=False)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='pushesgroup',blank=True, null=True)
    date = models.DateField(auto_now_add=True, null=True)
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=200)
    
    def __str__(self):
        return self.user.username
    
class JoinProposals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, null=True)
    is_accepted = models.BooleanField(default=False)
    date_accepted = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username + " wants to join " + self.stock.name