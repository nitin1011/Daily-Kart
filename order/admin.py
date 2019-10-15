from django.contrib import admin
from .models import Order, History, HistoryItem
# Register your models here.


admin.site.register(Order)
admin.site.register(History)
admin.site.register(HistoryItem)