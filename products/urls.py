from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('product/<int:pk>', views.product_detail, name='product-detail'),
    path('product/new', views.add_product, name='product-create'),
    path('product/all', views.all_product, name='product-all'),
    path('product/edit/<int:pk>', views.edit_product, name='edit-product'),
    path('product/delete/<int:pk>', views.delete_product, name='delete-product'),
    path('privacy', views.privacy, name='privacy'),
    path('terms', views.terms, name='terms'),
]