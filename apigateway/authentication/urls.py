from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt import views as jwt_views
from django.urls import path, include

from . import views

app_name='authentication'

urlpatterns = [
    
    path('logout/',views.LogoutView.as_view(), name='auth_logout'),
    path('emp/role/add/',views. emp_roles_post.as_view()),
    path('emp/role/',views.emp_roles_add.as_view()),
    path('employee/',views.add_employee.as_view()),
    path('add/roles/',views.add_roles.as_view()),
    path('api/register/',views.RegisterAPI.as_view()),
    path('api/token/',
		jwt_views.TokenObtainPairView.as_view()),
	# 	name ='token_obtain_pair'),
    # path('api/login/',obtain_auth_token,name='obtain_auth_token'),
    path('api/token/refresh/',
		jwt_views.TokenRefreshView.as_view(),
		name ='token_refresh'),
    path('api/welcome/',views.welcome.as_view()),
    # path('user/',views.user,name='user'),
    path('register/',views.branding_register.as_view()),
    path('tenant/',views.TenantCompany_API.as_view()),
    path('product/',views.product_Api.as_view()),
    path('raw/',views.Raw_Api.as_view()),
    path('cost/',views.Process_Cost_Api.as_view()),
    path('prod/req/',views.Productrequirements_Api.as_view()),
    path('company/',views.Company_details_Api.as_view()),
    path('company/list/',views.company_details_list.as_view()),
    path('suppliers/',views.supliers_contact__Api.as_view(),),
    path('process/',views.process_Api.as_view()),
    path('accepted/user/',views.Superadmin_accepted_user.as_view()),
    path('logout/',views.Logout.as_view()),
    path('user/tenant/<str:domain>/',views.user_tenant_id.as_view()),
    path('user/<str:tid>/',views.user_tenant_filter.as_view()),
    path('sales/',views.sales_list.as_view()),
    path('company/<int:cid>/',views.company_product_rawmaterials.as_view()),
    path('company/update/<int:id>/',views.company_update.as_view()),


    #inward
    path('inward/dc/details/',views.get_inward_dc_details.as_view()),#get all dc details
    path('inward/dc/materials/',views.get_inward_dc_materials.as_view()),#get dc materials list
    path('inward/dc/materials/update/<int:id>/',views.update_inward_dc.as_view()),
    path('add/inward/',views.add_inward.as_view()),#post dc inward details and materials in same post functions


    #dispatch
    path('dispatch/materials/',views.get_dispatch_dc_materials.as_view()),#dispatch materials list
    path('dispatch/materials/quality/',views.quality_unchecked_dispatch_materials.as_view()),#quality unchecked dispatch materials
    path('dispatch/details/',views.get_dispatch_dc_details.as_view()),
    path('dispatch/',views.add_dispatch.as_view())
    
]
