from django.urls import path
from . import views

app_name='production'

urlpatterns = [
    path('process/',views.Main_process_API_View.as_view(),name='main_process_api'),
    path('mainprocess/',views.Main_process_list.as_view(),name='main_process'),
    path('subprocess/',views.Subprocess_list.as_view(),name='sub_process'),
    path('',views.Production_API.as_view(),name='production'),
    path('list/<int:sub_process>/',views.Production_list.as_view(),name='Production_list'),
    path('process_card/<int:product_price>/',views.process_card.as_view(),name='process_card'),
    path('subprocess/create',views.Subprocess_create_API.as_view(),name='process_card'),
    path('process_card/po<int:poid>cmp<int:cmpid>/',views.process_card_details.as_view(),name='prod_price_subprocess'),


]
