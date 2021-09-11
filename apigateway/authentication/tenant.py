
def tenant(request):
    tenant_id=request.user.tenant_company.id
    return tenant_id
