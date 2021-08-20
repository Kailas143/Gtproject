from django.urls import path

from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name='register'

urlpatterns = [
    path('api/register/',views.RegisterAPI.as_view(),name='register_api'),
    path('api/login/',obtain_auth_token,name='obtain_auth_token'),
    path('api/welcome/',views.welcome.as_view(),name='welcome'),
    path('user/',views.user,name='users'),
    path('register/',views.branding_register.as_view(),name='branding_register')
    
]

