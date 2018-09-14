from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse

from memorial_park_mgmnt_app import models
from utils import utils

@login_required
def lot_lookup(request):
    if request.method == 'GET':
        branches = utils.get_branches(request.user)
        queryset = models.Lot.objects.filter(branch__id__in=branches)

        if request.GET.get('q'):
            queryset = queryset.filter(Q(block__icontains=q) |
                                       Q(lot__icontains=q) |
                                       Q(unit__icontains=q))

        queryset = queryset.order_by('block', 'lot', 'unit')

        res = []
        for item in queryset:
            res.append({
                    'id': item.id,
                    'name': str(item),
                    'ignore': False
                })

        return JsonResponse(res, safe=False)

@login_required
def client_lookup(request):
    if request.method == 'GET':
        branches = utils.get_branches(request.user)
        queryset = models.Client.objects.filter(branch__id__in=branches)
        
        if request.GET.get('q'):
            queryset = queryset.filter(Q(first_name__icontains=q) |
                                       Q(last_name__icontains=q) |
                                       Q(middle_name__icontains=q))

        queryset = queryset.order_by('last_name', 'first_name', 'middle_name')

        res = []
        for item in queryset:
            res.append({
                    'id': item.id,
                    'name': str(item),
                    'ignore': False
                })

        return JsonResponse(res, safe=False)

@login_required
def agent_lookup(request):
    if request.method == 'GET':
        branches = utils.get_branches(request.user)
        queryset = models.Agent.objects.filter(branch__id__in=branches)

        if request.GET.get('q'):
            queryset = queryset.filter(Q(first_name__icontains=q) |
                                       Q(last_name__icontains=q) |
                                       Q(middle_name__icontains=q))

        queryset = queryset.order_by('last_name', 'first_name', 'middle_name')

        res = []
        for item in queryset:
            res.append({
                    'id': item.id,
                    'name': str(item),
                    'ignore': False
                })

        return JsonResponse(res, safe=False)
