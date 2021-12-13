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
    path('product/main/<int:id>/',views.Product_main_component.as_view(),name='ProductUpdate'),
    path('product/price/',views.Product_price_API.as_view(),name='Productprice'),
    path('product/price/patch/<int:id>/',views.Productpricepatch.as_view(),name='Productprice'),
    # path('product/price/<int:cid>/',views.prod_price_company.as_view(),name='Productprice'),

    path('price/company/<int:company>/',views.prod_price_company.as_view(),name='prod_price_company'),
    path('price/product/po<int:poid>cmp<int:cmpid>/',views.prod_price_product.as_view(),name='prod_price_product'),
    path('price/<int:id>/',views.prod_price_id.as_view(),name='prod_price_product'),
    path('subprocess/po<int:poid>cmp<int:cmpid>/',views.process_card_list.as_view(),name='prod_price_subprocess'),
    path('price/list/',views.Product_price_list.as_view()),
    path('price/update/<int:id>/',views.prod_price_id_update.as_view()),
   

    path('add/product/req/',views.prod_req_raw_add.as_view()),
    path('product/req/',views.ProductreqAPI.as_view(),name='ProductreqAPI'),
    path('prod/req/<int:id>/',views.get_ProductreqAPI.as_view()),
    path('prod/req/pp<int:pid>pr<int:prid>/',views.prod_req_process_id_product_id.as_view()),
    # path('product/requ/<int:product__id>/',views.ProdReq.as_view(),name='ProdReq'),
    path('product/req/<int:id>/',views.ProductreqUpdate.as_view(),name='ProductreqUpdate'),
    path('prod/requ/<int:pid>/',views.Prodrequi.as_view()),
    path('prod/req/raw/<int:rid>/',views.Prodrequi_raw.as_view()),
   
    path('company/details/',views.Company_detailsApi.as_view(),name='Company_detailsApi'),
    path('company/details/<int:id>/',views.Company_detailsUpdateApi.as_view(),name='Company_detailsUpdateApi'),
    path('company/<int:id>/',views.company_id.as_view()),
    path('purchase/company/list/',views.purchase_company_list.as_view()),

    path('product/patch/<int:id>/',views.Productpatch.as_view()),
    path('product/ppid<int:pid>raw<int:rcid>/',views.prod_id_raw_comp_id.as_view()),\
    

    path('supplier/contact/',views.Supliers_contactApi.as_view(),name='Supliers_contactApi'),
    path('supplier/contact/<int:id>/',views.Supliers_contactUpdateApi.as_view(),name='Company_detailsUpdateApi'),


  
]
