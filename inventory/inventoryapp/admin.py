from django.contrib import admin
from .models import  Stock,Item, Store

# Register your models here.

admin.site.register(Item)
admin.site.register(Store)

class StockAdmin(admin.ModelAdmin):
    raw_id_fields = ("Item",)
    search_fields = ['ItemCode']


admin.site.register(Stock, StockAdmin)