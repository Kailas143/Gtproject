from django.urls import path 
from . import views 

app_name='rod'

urlpatterns = [
    path('product/',views.semi_product_api.as_view(),name='semi_product'),
    path('product/list/',views.semi_products_list.as_view(),name='semi_products_list'),
    path('product/price/',views.semi_products_plist.as_view(),name='semi_products_list'),
    path('raw/',views.raw_post.as_view(),name='semi_products_list'),
    path('raw/list/',views.raw_post_list.as_view(),name='semi_products_list'),
    path('cutting/',views.cutting_API.as_view(),name='cutting_API')
]
