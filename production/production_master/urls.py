from django.urls import path
from . import views 

urlpatterns = [
    path('add/mainprocess/',views.ProcessViewset.as_view()),
    path('add/subprocess/',views.add_subprocess.as_view()),
    path('process/subprocess/<int:pid>/',views.process_subprocess.as_view()),
    path('add/card/',views.process_card_details.as_view()),
    path('subprocess/prod/price/<int:pdid>/',views.product_subprocess.as_view()),
    path('process/card/subprocess/<int:spid>/',views.process_card_subprocess.as_view()),
    path('process/card/quantity/sp<int:spid>ppid<int:ppid>op<int:op>/',views.quantity_aggreagate.as_view()),
    path('process_card/po<int:poid>cmp<int:cmpid>/',views.process_card_all_details.as_view()),
    path('card/process/<int:pid>/',views.process_card_process_id.as_view()),
    path('subprocess/prod/proc/prd<pid>proc<prid>/',views.subprocess_process_prprice.as_view()),
]


