from datetime import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field, Layout, Button, ButtonHolder, Row, Column
from dal import autocomplete
from django import forms
from django.template.context_processors import request
from django.urls import reverse, reverse_lazy

from .models import Stock, Store, Item


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields ='__all__'
        widgets = {
            'Item': autocomplete.ModelSelect2(url='item-autocomplete', attrs={'data-container-css-class': '',
                                                                              'data-minimum-input-length': 3,})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.fields['Item'].widget.attrs.update({'autofocus': 'true'})
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(Column(Field('Item'), css_class='form-group col-md-6 mb-0'),css_class='form-row'),
            Row(Column(Field('LocationCode', readonly=True, required=False, blank=True, default=' '),css_class='read-only form-group col-md-6 mb-0'),css_class='form-row'),
            Row(Column(Field('Store'),css_class='form-group col-md-6 mb-0'),css_class='form-row'),
            Row(Column(Field('Quantity'),css_class='form-group col-md-6 mb-0'),css_class='form-row'),
            Row(Column(Field('InputDate', readonly=True),css_class='read-only form-group col-md-6 mb-0'),css_class='form-row'),
            Row(Column(Field('InputUser', readonly=True),css_class='read-only form-group col-md-6 mb-0'),css_class='form-row'),
            ButtonHolder(Submit('submit', 'Ενημέρωση'), Submit('delete', 'Διαγραφή', css_class='btn btn-danger'))
        )


class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields ='__all__'
        widgets = {
            'Item': autocomplete.ModelSelect2(url='item-autocomplete',  attrs={'data-container-css-class': '',
                                                                              'data-minimum-input-length': 3,})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(Row(Column(Field('Item'), css_class='form-group col-md-6 mb-0'),css_class='form-row'),
                                    Row(Column(Field('LocationCode', readonly=True, required=False, blank=True, default=' '), css_class='read-only form-group col-md-6 mb-0'),css_class='form-row'),
                                    Row(Column(Field('Store'),css_class='form-group col-md-6 mb-0'),css_class='form-row'),
                                    Row(Column(Field('Quantity'),css_class='form-group col-md-6 mb-0'),css_class='form-row'),
                                    Row(Column(Field('InputDate', readonly=True, type="hidden"),css_class='read-only form-group col-md-6 mb-0'),css_class='form-row'),
                                    Row(Column(Field('InputUser', readonly=True, type="hidden"),css_class='read-only form-group col-md-6 mb-0'),css_class='form-row'),
                                    ButtonHolder(Submit('submit', 'Αποθήκευση', css_class='btn btn-success', readonly=False),
                                     Submit('submitandnew', 'Αποθήκευση και προσθήκη νέου', css_class='btn btn-success')),
        )
        self.fields['Quantity'].widget.attrs.update({'autofocus': 'true'})


class StockSearchForm(forms.Form):
    store = forms.ModelChoiceField(queryset=None, required=False)
    item = forms.CharField(label='Barcode')
    loc = forms.CharField(label='Θέση', required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Row(
                Column(Field('item'), css_class='form-group'),
                css_class='form-row'
            ), Row(
                Column(Field('store'), css_class='form-group'),
                css_class='form-row'
            ), Row(
                Column(Field('loc'), css_class='form-group'),
                css_class='form-row'
            ), Submit('submit', 'Αναζήτηση'))
        self.fields['item'].widget.attrs.update({'autofocus': True})
        self.fields['store'].queryset = Store.objects.filter(code__in=list(self.user.groups.all().values_list('id', flat=True)))
        self.fields['loc'].initial = 'Άνευ'
        self.fields['loc'].disabled = True
        self.fields['store'].empty_label = None


class StockPDAUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields ='__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

        self.helper.form_method = 'post'
        #self.helper.form_action = reverse('update_stock')
        self.helper.layout = Layout(
            Field('Item', readonly=True, css_class='read-only'), Field('LocationCode', readonly=True, default=' ', css_class='read-only'), Field('Store', readonly=True, css_class='read-only'),
            Field('Quantity'), Field('InputDate', readonly=True, css_class='read-only'), Field('InputUser', readonly=True, css_class='read-only'),
            ButtonHolder(Submit('submit', 'Αποθήκευση και προσθήκη νέου')))
        self.fields['Item'].queryset = Item.objects.filter(id=kwargs['instance'].Item_id)
        self.fields['Quantity'].widget.attrs.update({'autofocus': 'true'})


class StockPDACreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('Item', readonly=True, css_class='read-only'), Field('LocationCode', readonly=True, css_class='read-only'),
            Field('Store', readonly=True, css_class='read-only'),
            Field('Quantity'), Field('InputDate', readonly=True, type="hidden", css_class='read-only'),
            Field('InputUser', readonly=True, type="hidden", css_class='read-only'),
            ButtonHolder(Submit('submitandnew', 'Αποθήκευση και προσθήκη νέου', css_class='btn btn-success')))
        self.fields['Quantity'].widget.attrs.update({'autofocus': 'true'})
        self.fields['Item'].empty_label = None
