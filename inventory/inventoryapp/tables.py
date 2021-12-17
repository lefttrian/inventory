import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from .models import Stock


class StockTable(tables.Table):
    Επεξεργασία = tables.LinkColumn('stockdetail', text='Επεξεργασία', args=[A('pk')], attrs={
        'a': {'class': 'btn btn-primary'}
    }, empty_values=(), orderable=False)


    class Meta:
        model = Stock
        template_name = "stock_list_table.html"
        fields = ("Item", "LocationCode", "Store", "Quantity", 'InputDate' )