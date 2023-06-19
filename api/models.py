from django.db import models


class User(models.Model):
    username = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    dob = models.DateField()
    email = models.EmailField()
    hashed_password = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.username

class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey('Categories', on_delete=models.CASCADE, related_name='foods',default=1)
    picture = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.name


class Categories(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class Stock(models.Model):
    is_personal = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_stocks')
    can_access = models.ManyToManyField(User, related_name='accessible_stocks', blank=True)
    name = models.CharField(max_length=100)
    
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