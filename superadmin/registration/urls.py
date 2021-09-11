from django.urls import path 
from . import views 

app_name='registration'

urlpatterns = [
    path('api/',views.RegisterApi.as_view(),name='register_details'),
    path('api/<int:id>/',views.RegisterApi.as_view(),name='register_details'),
    path('user/',views.accepted_user,name='accepted_user'),
    path('accepted/',views.Accepted_user.as_view(),name='Accepted_user'),
    path('accepted/user/<int:id>/',views.Register_Update.as_view(),name='Register_Update')
]
