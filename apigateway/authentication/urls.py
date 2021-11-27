from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views
from django.urls import path, include

from . import views

app_name='authentication'

urlpatterns = [
    #authentication
    path('api/register/',views.RegisterAPI.as_view()),
    path('api/token/',views.MyTokenObtainPairView.as_view()),
    path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
    path('api/change/password/',views.ChangePasswordView.as_view(),name='change-password'),
    path('welcome/',views.welcome.as_view()),
    path('forgetpassword/',views.forgetpassword.as_view()),
    path('logout/',views.LogoutView.as_view(), name='auth_logout'),
    
    #employee adding section
    path('emp/role/add/',views. emp_roles_post.as_view()),
    path('emp/role/',views.emp_roles_add.as_view()),
    path('employee/',views.add_employee.as_view()),
    path('add/roles/',views.add_roles.as_view()),
    path('api/register/',views.RegisterAPI.as_view()),

    path('register/',views.branding_register.as_view()),
    path('tenant/',views.TenantCompany_API.as_view()),

    path('product/',views.product_Api.as_view()),
    path('product/<int:id>/',views.Product_update.as_view()),

    path('raw/',views.Raw_Api.as_view()),
    path('raw/<int:id>/',views.Raw_update.as_view()),

    path('cost/',views.Process_Cost_Api.as_view()),
    path('cost/<int:id>/',views.Process_Cost_Update.as_view()),



    path('prod/spec/',views.ProductspecAPI_Api.as_view()),
    path('prod/spec/<int:id>/',views.Prod_spec_Update.as_view()),

    path('prod/req/',views.Productrequirements_Api.as_view()),
    path('prod/req/<int:id>/',views.prod_req_update.as_view()),

    path('company/',views.Company_details_Api.as_view()),
    path('company/list/',views.company_details_list.as_view()),
    path('company/<int:id>/',views.comp_update.as_view()),


    path('suppliers/',views.supliers_contact__Api.as_view()),
    path('suppliers/<int:id>/',views.suppliers_update.as_view()),

    path('process/',views.process_Api.as_view()),
    path('process/<int:id>/',views.Process_Update.as_view()),
    
    path('product/price/list/',views.get_product_price_list.as_view()),
    path('product/price/<int:id>/',views. prod_price_update.as_view()),
    path('product/price/add/',views.add_product_price.as_view()),

    path('accepted/user/',views.Superadmin_accepted_user.as_view()),
   
    path('user/tenant/<str:domain>/',views.user_tenant_id.as_view()),
    path('user/<str:tid>/',views.user_tenant_filter.as_view()),
    path('sales/',views.sales_list.as_view()),
   
    path('company/update/<int:id>/',views.company_update.as_view()),
    path('add/service/',views.create_service.as_view()),
    path('prod/company/<int:cid>/',views.company_product_price.as_view()),

    path('add/menu/',views.MenuViewset.as_view()),
    path('add/menu/link/',views.add_menu_link.as_view()),

    


    #inward
    path('inward/dc/details/',views.get_inward_dc_details.as_view()),#get all dc details
    path('inward/dc/materials/',views.get_inward_dc_materials.as_view()),#get dc materials list
    path('inward/dc/materials/update/<int:id>/',views.update_inward_dc.as_view()),
    path('add/inward/',views.add_inward.as_view()),#post dc inward details and materials in same post functions
    path('inward/company/<int:cid>/',views.company_product_rawmaterials.as_view()),


    #dispatch
    path('dispatch/materials/',views.get_dispatch_dc_materials.as_view()),#dispatch materials list
    path('dispatch/materials/quality/',views.quality_unchecked_dispatch_materials.as_view()),#quality unchecked dispatch materials
    path('dispatch/details/',views.get_dispatch_details.as_view()),
    path('dispatch/materials/bill/<int:id>/',views.materials_details_bill_id.as_view()),
    path('add/dispatch/',views.add_dispatch.as_view()),
    path('dispatch/company/<int:cid>/',views.dispatch_company_bal_qty.as_view()),


    #dc

    path('dc/list/',views.dc_dc_list.as_view()),
    path('dc/dcnumber/',views.get_dc_dcnumber.as_view()),
    path('dc/dccreate/',views.dc_dcreate.as_view()),
    path('dc/dcforprint/<int:id>/',views.dc_for_print.as_view()),
    path('dc/dcdetails/bng/',views.dc_print.as_view()),


    #purchase 
    path('invoice/create/',views.invoice_create.as_view()),
    path('invoice/delete/<int:id>/',views.invoice_delete.as_view()),
    path('invoice/update/<int:id>/',views.invoice_update.as_view()),

    #production
    path('production/mainprocess/create/',views.add_production_mainproccess.as_view()),
    path('production/subprocess/create/',views.add_production_subprocess.as_view()),
    path('production/card/create/',views.add_production_prodcard.as_view()),
    path('production/processcard/po<int:poid>cmp<int:cmpid>/',views.get_prod_card_all_details.as_view()),
    path('production/subprocess/<int:pid>/',views.process_based_subprocess.as_view()),
    path('prod/card/<int:pid>/',views.process_card_process_id_details.as_view()),
    path('subprocess/prd<int:pid>prc<int:prid>/',views.subprocess_process_id_prodprice_id.as_view()),


    #payment
    path('payment/salespayment/all/',views.get_sales_payment_list_post.as_view()),
    path('payment/purchasepayment/all/',views.get_purchase_payment_list_post.as_view()),


    #sales
    path('sales/invoicenumber/',views.dc_sales_invoicenum.as_view()),
    path('sales/dcinv/all/',views.dc_sales_dcinv_all.as_view()),
    path('dc/details/company/',views.dc_details_company.as_view()),
    path('sales/dcinv/',views.dc_sales_dcinv.as_view()),
    path('sales/disinv/all/',views.sales_disinv_all.as_view()),
    path('sales/disinv/',views.sales_disinv.as_view()),

    #quality
    path('quality/process/report/',views.quality_process_report.as_view()),
    path('quality/process/report/<int:id>/',views.quality_process_report_id.as_view()),
    path('quality/parameter/',views.quality_parameter.as_view()),
    path('quality/sample/value/',views.quality_sample_value.as_view()),
    path('quality/status/',views.quality_status.as_view()),
    path('quality/report/',views.quality_report.as_view()),
    path('quality/final/report/<int:id>/',views.quality_final_report.as_view()),









]
