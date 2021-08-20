from django.urls import path 
from . import views 

app_name='registration'

urlpatterns = [
    path('api/',views.RegisterApi.as_view(),name='register_details'),
    path('user/',views.accepted_user,name='accepted_user')
]
