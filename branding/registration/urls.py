from django.urls import path 
from . import views

app_name='registration'

urlpatterns = [
    # path('register/',views.register,name='register'),
    path('register/',views.RegisterApi.as_view(),name='registerapi'),
    path('user/<int:id>/',views.Register_Update.as_view(),name='Register_update')
]
