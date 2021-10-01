from django.urls import path
from . views import StockAPI,Stock_list,Stock_list_history

app_name='store'

urlpatterns = [
    path('',StockAPI.as_view(),name='stockapi'),
    path('stock/',Stock_list.as_view(),name='Stock_list'),
    path('history/',Stock_list_history.as_view(),name='Stock_list_history'),

]
