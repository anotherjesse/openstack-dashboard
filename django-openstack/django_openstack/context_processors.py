
from django_openstack import api


def tenants(request):
    if not request.user or not request.user.is_authenticated():
        return {}
    return {'tenants': api.token_list_tenants(request, request.user.token)}
