from . models import User,Tenant_Company

def get_hostname(request) :
    return request.get_host().split(':')[0].lower()

def get_tenant(request):
    hostname=get_hostname(request)
    subdomain=hostname.split('.')[0]
    
    
    return User.objects.filter(tenant_company=subdomain)