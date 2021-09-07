from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name='master'

urlpatterns = [
    path('raw/',views.RawAPI.as_view(),name='RawAPI'),
    path('raw/<int:id>/',views.RawAPIUpdate.as_view(),name='RawAPIUpdate'),

    path('process/cost/',views.ProcessCostAPI.as_view(),name='ProcessCostAPI'),
    path('process/cost/<int:id>/',views.ProcessCostUpdate.as_view(),name='ProcessCostUpdate'),

    path('process/',views.ProcessAPI.as_view(),name='ProcessAPI'),
    path('process/<int:id>/',views.ProcessUpdate.as_view(),name='ProcessUpdate'),

    path('product/spec/',views.ProductspecAPI.as_view(),name='ProductspecAPI'),
    path('product/spec/<int:id>/',views.ProductspecUpdate.as_view(),name='ProcessspecUpdate'),

    path('product/',views.ProductAPI.as_view(),name='ProductAPI'),
    path('product/<int:id>/',views.ProductAPIUpdate.as_view(),name='ProductUpdate'),

    path('product/req/',views.ProductreqAPI.as_view(),name='ProductreqAPI'),
    path('product/req/<int:id>/',views.ProductreqUpdate.as_view(),name='ProductreqUpdate'),
   
    path('company/details/',views.Company_detailsApi.as_view(),name='Company_detailsApi'),
    path('company/details/<int:id>/',views.Company_detailsUpdateApi.as_view(),name='Company_detailsUpdateApi'),

    path('supplier/contact/',views.Supliers_contactApi.as_view(),name='Supliers_contactApi'),
    path('supplier/contact/<int:id>/',views.Supliers_contactUpdateApi.as_view(),name='Company_detailsUpdateApi'),

    path('user/',views.Register_User_API.as_view(),name='Register_User_API'),
    path('user/<int:id>/',views.User_API.as_view(),name='User_API'),
    path('roles/',views.Role_API.as_view(),name='Role_API'),

    # path('user/api/',views.User_API_new.as_view(),name='User_API'),
    path('api-token-auth/',obtain_auth_token, name='api-token-auth'),
    path('api/welcome/',views.welcome.as_view(),name='welcome'),

  
]
