from datetime import datetime

import django_filters
from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import UpdateView, DeleteView, CreateView
from django_extensions import auth
from django_filters import DateFromToRangeFilter, DateRangeFilter
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from .forms import StockUpdateForm, StockCreateForm
from .tables import StockTable
# Create your views here.
from .models import Stock, Item


class StockFilter(django_filters.FilterSet):
    InputDate = DateRangeFilter()

    class Meta:
        model = Stock
        fields = {'Item__code': ['contains'], 'LocationCode': ['contains'], 'Store': ['exact'], 'InputDate':[]}


class StockIndexView(LoginRequiredMixin, SingleTableMixin, FilterView):
    template_name = 'inventoryapp/stock_list.html'
    model = Stock
    table_class = StockTable
    filterset_class = StockFilter


class StockDetailView(LoginRequiredMixin, UpdateView):
    model = Stock
    form_class = StockUpdateForm
    template_name = "stock_detail.html"

    def get_success_url(self):
        view_name = 'inventoryapp\stockdetail'
        # No need for reverse_lazy here, because it's called inside the method
        return reverse(view_name, kwargs={'pk': self.object.id})


class StockDeleteView(LoginRequiredMixin, DeleteView):
    model = Stock
    template_name = "inventoryapp\stock_confirm_delete.html"
    success_url = reverse_lazy('index')


class StockCreateView(LoginRequiredMixin, CreateView):
    model = Stock
    form_class = StockCreateForm
    success_url = reverse_lazy('index')

    def get_form_kwargs(self):
        kwargs = super(StockCreateView, self).get_form_kwargs()
        kwargs['initial'] = {'InputUser': self.request.user.id, 'InputDate': datetime.now()}
        return kwargs


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