from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render


@staff_member_required(login_url="admin:login")
def resource_hub(request):
    hostname = request.get_host().split(":", maxsplit=1)[0]
    if hostname != "admin.autolang.deo-core.codes":
        raise Http404

    return render(request, "catalog/resource_hub.html")
