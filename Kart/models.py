from django.db import models
from products.models import Products
from django.contrib.auth import get_user_model
from order.models import Order
# Create your models here.
User = get_user_model()

class CartItem(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    kart = models.ForeignKey('Kart', null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    line_total = models.DecimalField(default=0, max_digits=50, decimal_places=2)

    def __str__(self):
        return str(self.product.id)


class Kart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    #item = models.ManyToManyField(CartItem, null=True, blank=True)
    #products = models.ManyToManyField(Products, null=True, blank=True)
    total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    item_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id)
