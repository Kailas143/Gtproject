from django.urls import path

from . import views

app_name='dispatch'

urlpatterns = [
    path('materials/',views.Dispatch_MaterialsAPI.as_view(),name='Dispatch_MaterialsAPI'),
    path('materials/<int:id>/',views.Dispatch_MaterialsAPI.as_view(),name='Dispatch_MaterialsAPI'),
    path('details/',views.Dispatch_detailsAPI.as_view(),name='Dispatch_details'),
    path('details/<int:id>/',views.Dispatch_detailsAPI.as_view(),name='Dispatch_details'),
    path('login/',views.LoginAPI.as_view(),name='LoginAPI'),
    path('api/details/',views.Dispatch_details_post_API.as_view(),name='Dispatch_details_post_API'),
    path('stock/',views.StockAPI.as_view(),name='StockAPI')


]
