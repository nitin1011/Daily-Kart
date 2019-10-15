from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_kart, name='view-kart'),
    path('<int:id>', views.update_kart, name='update-kart'),
]