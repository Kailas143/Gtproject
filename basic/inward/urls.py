from django.urls import path

from . import views

app_name='inward'

urlpatterns = [
    path('dc/materials/',views.Dc_MaterialsAPI.as_view(),name='Dc_MaterialsAPI'),
    path('dc/materials/<int:id>/',views.Dc_MaterialsAPI.as_view(),name='Dc_MaterialsAPI'),
    path('dc/details/',views.Dc_detailsAPI.as_view(),name='Dc_details'),
    path('dc/details/<int:id>/',views.Dc_detailsAPI.as_view(),name='Dc_details'),
    path('login/',views.LoginAPI.as_view(),name='LoginAPI'),


]
