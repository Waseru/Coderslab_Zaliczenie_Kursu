from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    # order = models.ForeignKey(Order, related_name='order')


    def __str__(self):
        return self.name

class ProductPart(models.Model):
    part_number = models.CharField(max_length=12, unique=True)
    product_name = models.ForeignKey(Product)
    quantity = models.PositiveIntegerField()
    expire_date = models.DateField()

    def __str__(self):
        return self.part_number

class Order(models.Model):
    user = models.ForeignKey(User, related_name='user')
    order_date = models.DateField(auto_now_add=True)
    product = models.ManyToManyField(Product, through='OrderData', related_name='product')

    def get_products(self):
        for order_object in OrderData.objects.filter(order=self):
            yield order_object.product_part
            yield order_object.order_quantity



    def __str__(self):
        return 'Order nr {}'.format(self.id)

class OrderData(models.Model):
    product = models.ForeignKey(Product)
    product_part = models.ForeignKey(ProductPart)
    order = models.ForeignKey(Order)
    order_quantity = models.IntegerField()

#django wie który user jest zalogowany i przenosi go w requestie tworząc model