from django.db import models
from products.models import Products
from django.contrib.auth import get_user_model
# Create your models here.

STATUS_CHOICES = (
    ("Notstarted", "Notstarted"),
    ("Started", "Started"),
    ("Finished", "Finished"),
    ("Canceled", "Canceled")
)

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    shop_user = models.CharField(max_length=120, blank=True, null=True)
    order_id = models.CharField(max_length=120, default="ABC", unique=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Notstarted")
    sub_total = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    delivery_charge = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    delivery_boy = models.CharField(max_length=120, blank=True, null=True)
    final_total = models.DecimalField(default=0, max_digits=100, decimal_places=2)
    datetime = models.DateTimeField()

    def __str__(self):
        return str(self.id)

class HistoryItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    history = models.ForeignKey('History', null=True, blank=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    line_total = models.DecimalField(default=0, max_digits=50, decimal_places=2)
    datetime = models.DateTimeField(auto_now=True)


class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
