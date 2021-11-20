from django.urls import path
from . import views 

urlpatterns = [
    path('add/mainprocess/',views.ProcessViewset.as_view()),
    path('add/subprocess/',views.add_subprocess.as_view())
]

