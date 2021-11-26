from datetime import datetime

from django.db import models


class Item(models.Model):
    id = models.CharField(primary_key=True,max_length=50)
    code = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.code+'-'+self.description

    class Meta:
        managed = False
        ordering = ['code']
        db_table = 'inventoryapp_item'


class Store(models.Model):
    id = models.CharField(primary_key=True,max_length=50)
    code = models.CharField(max_length=25, unique=True)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.code+'-'+self.description

    class Meta:
        managed = False
        ordering = ['code']
        db_table = 'inventoryapp_store'


class Stock(models.Model):
    Item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    LocationCode = models.CharField(max_length=20)
    Quantity = models.FloatField()
    Store = models.ForeignKey(Store, on_delete=models.DO_NOTHING)
    InputDate = models.DateTimeField(null=False, default=datetime.now())
    InputUser = models.IntegerField(null=False)

    class Meta:
        unique_together = ('Item', 'LocationCode', 'Store')

    def __str__(self):
        return self.Item.__str__() + '-' + self.Store.__str__()+'-'+self.Quantity.__str__()

# Create your models here.
