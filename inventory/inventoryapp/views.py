from datetime import datetime

import django_filters
from dal import autocomplete
from dal.widgets import Select
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import request
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import UpdateView, DeleteView, CreateView
from django_extensions import auth
from django_filters import DateFromToRangeFilter, DateRangeFilter, ChoiceFilter, ModelChoiceFilter
from django_filters.fields import ModelChoiceField
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from .forms import StockUpdateForm, StockCreateForm
from .tables import StockTable
# Create your views here.
from .models import Stock, Item, Store


def userstores(request):
    if request is None:
        return Store.objects.none()
    if not request.user.is_authenticated:
        return Store.objects.none()
    q = Store.objects.filter(code__in=list(request.user.groups.all().values_list('id', flat=True)))
    return q


class StockFilter(django_filters.FilterSet):
    InputDate = DateRangeFilter(label='Ημ/νία δημιουργίας')
    Store = ModelChoiceFilter(queryset=userstores,
                              required=False, label='Κατάστημα', empty_label=None)

    class Meta:
        model = Stock
        fields = {'Item__searchfield': ['contains'], 'Item__code': ['contains'], 'Store': ['exact'], 'InputDate': []}

    def __init__(self, *args, **kwargs):
        super(StockFilter, self).__init__(*args, **kwargs)
        if self.request.user.is_superuser:
            self.filters['Store'].extra['empty_label'] = '--------'
        else:
            self.filters['Store'].extra['empty_label'] = None
        self.filters['Item__searchfield__contains'].field.label = 'w_search'
        self.filters['Item__code__contains'].field.label = 'Κωδικός είδους'


class StockIndexView(LoginRequiredMixin, SingleTableMixin, FilterView):
    template_name = 'inventoryapp/stock_list.html'
    model = Stock
    table_class = StockTable
    filterset_class = StockFilter

    def get_queryset(self):
        super(StockIndexView, self).get_queryset()
        q = Stock.objects.filter(Store__code__in=list(self.request.user.groups.all().values_list('id', flat=True)))
        return q


class StockDetailView(LoginRequiredMixin, UpdateView):
    model = Stock
    form_class = StockUpdateForm
    template_name = "stock_detail.html"

    def get_success_url(self):
        view_name = 'stockdetail'
        # No need for reverse_lazy here, because it's called inside the method
        return reverse(view_name, kwargs={'pk': self.object.id})

    def get_form(self, *args, **kwargs):
        form = super(StockDetailView, self).get_form(*args, **kwargs)
        form.fields['Store'].queryset = Store.objects.filter(code__in=list(self.request.user.groups.all().values_list('id', flat=True)))
        form.fields['LocationCode'].required = False
        return form


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
        kwargs['initial'] = {'InputUser': self.request.user.id, 'InputDate': datetime.now(), 'LocationCode': 'Άνευ'}
        return kwargs

    def get_form(self, *args, **kwargs):
        form = super(StockCreateView, self).get_form(*args, **kwargs)
        form.fields['Store'].queryset = Store.objects.filter(code__in=list(self.request.user.groups.all().values_list('id', flat=True)))
        form.fields['LocationCode'].required = False
        return form

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            if 'submitandnew' in request.POST:
                return redirect('stockcreate')
            else:
                return redirect('index')
        return render(request, 'inventoryapp/stock_form.html', {'form': form})


class ItemAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Item.objects.none()

        qs = Item.objects.all()

        if self.q:
            qs = qs.filter(searchfield__icontains=self.q)

        return qs


def logout(request):
    auth.logout(request)
    return redirect('index')
