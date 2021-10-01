from django.urls import path

from . import views

app_name='outward'

urlpatterns = [
    path('outward/',views.Outward_API.as_view(),name='outward'),
    path('materials/',views.Outwardmaterial_API.as_view(),name='Outwardmaterial_API')
]
