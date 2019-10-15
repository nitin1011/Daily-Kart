from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
# Create your models here.

User = get_user_model()
#product table

class Products(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    product_category = models.CharField(max_length=50)
    product_price = models.DecimalField(max_digits=20, decimal_places=2)
    product_discount = models.DecimalField(max_digits=5, decimal_places=2)
    product_image = models.ImageField(upload_to='product_img')
    product_disc = models.TextField()

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk': self.pk})
