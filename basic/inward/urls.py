from django.urls import path

from . import views

app_name='inward'

urlpatterns = [
    path('dc/materials/',views.Dc_MaterialsAPI.as_view(),name='Dc_MaterialsAPI'),
    path('dc/materials/<int:id>/',views.Dc_MaterialsAPI.as_view(),name='Dc_MaterialsAPI'),
    path('dc/materials/year/',views.DC_materials_year.as_view(),name='DC_materials_year'),

    path('dc/details/',views.Dc_detailsAPI.as_view(),name='Dc_details'),
    path('dc/details/<int:id>/',views.Dc_detailsAPI.as_view(),name='Dc_details'),
    path('dc/details/year/',views.DC_details_year.as_view(),name='DC_details_year'),
    path('dc/details/add/',views.DC_details_add.as_view(),name='DC_details_add'),

    path('login/',views.LoginAPI.as_view(),name='LoginAPI'),
    path('api/',views.UserPermission.as_view(),name='UserPermission')

    
    


]
