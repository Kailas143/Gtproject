from django.urls import path

from . import views

app_name='store'

urlpatterns = [
    path('stock/',views.StockAPI.as_view(),name='StockAPI'),
    path('stock/list/',views.Stock_list.as_view(),name='Stock_list'),
  
    path('stock/history/',views.Stock_HistoryAPI.as_view(),name='Stock_historyApi')
  

]