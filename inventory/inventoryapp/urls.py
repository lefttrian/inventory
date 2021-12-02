from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import RedirectView

from . import views
from .views import ItemAutocomplete

urlpatterns = [
    path('', views.StockIndexView.as_view(), name='index'),
    path('<int:pk>/', views.StockDetailView.as_view(), name='stockdetail'),
    path('<int:pk>/pdadetail', views.StockPDADetailView.as_view(), name='stockpdadetail'),
    path('<int:pk>/delete', views.StockDeleteView.as_view(), name='stockdelete'),
    path('item-autocomplete/$', login_required(ItemAutocomplete.as_view()), name='item-autocomplete'),
    path('create', views.StockCreateView.as_view(), name='stockcreate'),
    path('pdacreate', views.StockPDACreateView.as_view(), name='stockpdacreate'),
    path('searchstock', views.StockSearch, name='searchstock'),
    url(r'^$', RedirectView.as_view(url='/inventory/')),
    #path('<int:question_id>/results/', views.results, name='results'),
    #path('<int:question_id>/vote/', views.vote, name='vote'),
]