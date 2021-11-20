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
    path('product/price/',views.Product_price_API.as_view(),name='Productprice'),
    # path('product/price/<int:cid>/',views.prod_price_company.as_view(),name='Productprice'),

    path('price/company/<int:company>/',views.prod_price_company.as_view(),name='prod_price_company'),
    path('price/product/po<int:poid>cmp<int:cmpid>/',views.prod_price_product.as_view(),name='prod_price_product'),
    path('price/<int:id>/',views.prod_price_id.as_view(),name='prod_price_product'),
    path('subprocess/po<int:poid>cmp<int:cmpid>/',views.process_card_list.as_view(),name='prod_price_subprocess'),

    path('product/req/',views.ProductreqAPI.as_view(),name='ProductreqAPI'),
    path('prod/req/<int:id>/',views.get_ProductreqAPI.as_view()),
    path('product/requ/<int:product__id>/',views.ProdReq.as_view(),name='ProdReq'),
    path('product/req/<int:id>/',views.ProductreqUpdate.as_view(),name='ProductreqUpdate'),
    path('prod/requ/<int:pid>/',views.Prodrequi.as_view()),
    path('prod/req/raw/<int:rid>/',views.Prodrequi_raw.as_view()),
   
    path('company/details/',views.Company_detailsApi.as_view(),name='Company_detailsApi'),
    path('company/details/<int:id>/',views.Company_detailsUpdateApi.as_view(),name='Company_detailsUpdateApi'),
    path('company/<int:id>/',views.company_id.as_view()),

    path('supplier/contact/',views.Supliers_contactApi.as_view(),name='Supliers_contactApi'),
    path('supplier/contact/<int:id>/',views.Supliers_contactUpdateApi.as_view(),name='Company_detailsUpdateApi'),

    # path('user/',views.Register_User_API.as_view(),name='Register_User_API'),
    # path('user/<int:id>/',views.User_API.as_view(),name='User_API'),
    # path('roles/',views.Role_API.as_view(),name='Role_API'),

    # path('user/api/',views.User_API_new.as_view(),name='User_API'),
    path('api-token-auth/',obtain_auth_token, name='api-token-auth'),
    # path('api/welcome/',views.welcome.as_view(),name='welcome'),

  
]
