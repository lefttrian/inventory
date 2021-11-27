import django_filters
from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.views.generic import UpdateView
from django_extensions import auth
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from .forms import StockUpdateForm
from .tables import StockTable
# Create your views here.
from .models import Stock, Item


class StockFilter(django_filters.FilterSet):
    class Meta:
        model = Stock
        fields = {'Item__code': ['contains'], 'LocationCode': ['contains'], 'Store': ['exact']}


class StockIndexView(LoginRequiredMixin,generic.ListView, SingleTableMixin, FilterView):
    template_name = 'inventoryapp/stock_list.html'
    model = Stock
    table_class = StockTable
    filterset_class = StockFilter

    def get_queryset(self):
        """Return the last five published questions."""
        return Stock.objects.order_by('-InputDate')


class StockDetailView(LoginRequiredMixin, UpdateView):
    model = Stock
    form_class = StockUpdateForm
    template_name = "stock_detail.html"

    def get_success_url(self):
        view_name = 'stockdetail'
        # No need for reverse_lazy here, because it's called inside the method
        return reverse(view_name, kwargs={'pk': self.object.id})


class ItemAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Item.objects.none()

        qs = Item.objects.all()

        if self.q:
            qs = qs.filter(code__istartswith=self.q)

        return qs


def logout(request):
    auth.logout(request)
    return redirect('index')