from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views
from .views import ItemAutocomplete

urlpatterns = [
    path('', views.StockIndexView.as_view(), name='index'),
    path('<int:pk>/', views.StockDetailView.as_view(), name='stockdetail'),
    path('<int:pk>/delete', views.StockDeleteView.as_view(), name='stockdelete'),
    path('item-autocomplete/$', login_required(ItemAutocomplete.as_view()), name='item-autocomplete'),
    path('create', views.StockCreateView.as_view(), name='stockcreate'),
    #path('<int:question_id>/results/', views.results, name='results'),
    #path('<int:question_id>/vote/', views.vote, name='vote'),
]