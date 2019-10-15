from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('history/', views.history_view, name='history'),
    path('orders/', views.order_list, name='order-list'),
    path('detail/<int:id>/', views.order_detail, name='order-detail'),
    path('accept/<int:id>', views.accepted, name='accepted'),
    path('order/<int:id>', views.finished, name='finished'),
    path('canceled/<int:id>', views.canceled, name='canceled'),
    path('delete/<int:id>', views.delete_order, name='delete')
]