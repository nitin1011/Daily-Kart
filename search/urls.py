from django.urls import path
#from .views import SearchProductView
from . import views
urlpatterns = [
    path('', views.search, name='search-product'),
]