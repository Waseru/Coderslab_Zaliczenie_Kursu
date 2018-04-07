from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()

    def __str__(self):
        return self.name

class ProductPart(models.Model):
    part_number = models.CharField(max_length=12, unique=True)
    product_name = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField()
    expire_date = models.DateField()

class Order(models.Model):
    user = models.ForeignKey(User, related_name='user')
    product = models.ManyToManyField(Product)

#django wie który user jest zalogowany i przenosi go w requestie więc tworząc model