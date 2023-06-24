from django.db import models
from django.contrib.auth.models import User

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
    is_default = models.BooleanField(null=True,blank=True,default=False)
    
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