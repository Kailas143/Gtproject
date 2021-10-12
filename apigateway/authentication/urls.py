from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from . import views

app_name='authentication'

urlpatterns = [
    path('api/register/',views.RegisterAPI.as_view(),name='register_api'),
    path('api/login/',obtain_auth_token,name='obtain_auth_token'),
    path('api/welcome/',views.welcome.as_view(),name='welcome'),
    # path('user/',views.user,name='user'),
    path('register/',views.branding_register.as_view(),name='branding_register'),
    path('tenant/',views.TenantCompany_API.as_view(),name='TenantCompany_API'),
    path('dispatch/',views.Dispatch.as_view(),name='Dispatch'),
    path('dispatch/<int:id>/',views.Dispatch.as_view(),name='Dispatch'),
    path('product/',views.product_Api.as_view(),name='product_Api'),
    path('raw/',views.Raw_Api.as_view(),name='Raw_Api'),
    path('cost/',views.Process_Cost_Api.as_view(),name='Process_Cost_Api'),
    path('prod/req/',views.Productrequirements_Api.as_view(),name='Productrequirements'),
    path('company/',views.Company_details_Api.as_view(),name='Company_details_Api'),
    path('suppliers/',views.supliers_contact__Api.as_view(),name='supliers_contact__Api'),
    path('process/',views.process_Api.as_view(),name='process_Api'),
    path('accepted/user/',views.Superadmin_accepted_user.as_view(),name='Superadmin _accepted_user'),
    path('logout/',views.Logout.as_view(),name='logout'),
    path('user/tenant/<str:domain>/',views.user_tenant_id.as_view(),name='logout'),
    path('user/<str:tid>/',views.user_tenant_filter.as_view(),name='user_tenant_filter'),
    # path('api/token',TokenObtainPairView.as_view()),
    # path('api/token/refresh',TokenRefreshView.as_view()),
 
    # path('users/',views.AdminUsers.as_view(),name='AdminUsers')
    
    
]

