from django.urls import path

from . import views

app_name='store'

urlpatterns = [
    path('stock/',views.StockAPI.as_view(),name='StockAPI'),
    path('stock/list/',views.Stock_list.as_view(),name='Stock_list'),
    path('stock/year/',views.Stock_Year_Report.as_view(),name='Stock_list'),
    path('stock/raw/<int:rid>/',views.stock_raw_materials.as_view()),

    # path('login',views.LoginAPI.as_view(),name="LoginAPI"),
    # path('register/',views.RegisterAPI.as_view(),name="RegisterAPI"),
   
    path('stock/history/',views.Stock_HistoryAPI.as_view(),name='Stock_historyApi')
  

]
