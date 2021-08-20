from django.urls import path 
from . import views

app_name='registration'

urlpatterns = [
    path('register/',views.register,name='register'),
    path('register/api/',views.RegisterApi.as_view(),name='registerapi')
]
