from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, Layout, Button
from dal import autocomplete
from django import forms
from django.template.context_processors import request
from django.urls import reverse, reverse_lazy

from .models import Stock


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields ='__all__'
        widgets = {
            'Item': autocomplete.ModelSelect2(url='item-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-lg-2'
        # self.helper.field_class = 'col-lg-8'
        # self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        #self.helper.form_action = reverse('update_stock')
        self.helper.layout = Layout(
            Field('Item'), Field('LocationCode'), Field('Store'),
            Field('Quantity'), Field('InputDate', readonly=True), Field('InputUser', readonly=True),
            Submit('submit', 'Ενημέρωση'),
            Button('delete', 'Διαγραφή', css_class='btn btn-danger', onclick='location.href=\''+reverse_lazy('stockdelete', kwargs={'pk': kwargs['instance'].pk})+'\';')
        )


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields ='__all__'
        widgets = {
            'Item': autocomplete.ModelSelect2(url='item-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_class = 'form-horizontal'
        # self.helper.label_class = 'col-lg-2'
        # self.helper.field_class = 'col-lg-8'
        # self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        #self.helper.form_action = reverse('update_stock')
        self.helper.layout = Layout(
            Field('Item'), Field('LocationCode'), Field('Store'),
            Field('Quantity'), Field('InputDate', readonly=True), Field('InputUser', readonly=True),
            Submit('submit', 'Ενημέρωση'),
            #Button('delete', 'Διαγραφή', css_class='btn btn-danger', onclick='location.href=\''+reverse_lazy('stockdelete', kwargs={'pk': kwargs['instance'].pk})+'\';')
        )
