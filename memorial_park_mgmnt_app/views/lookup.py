from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse

from memorial_park_mgmnt_app import models
from utils import utils

@utils.branch_required(utils.is_auth_and_has_branch)
def lot_lookup(request):
    if request.method == 'GET':
        branch = request.session.get('branch_id')
        queryset = models.Lot.objects.filter(branch__id=branch)

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

@utils.branch_required(utils.is_auth_and_has_branch)
def client_lookup(request):
    if request.method == 'GET':
        branch = request.session.get('branch_id')
        queryset = models.Client.objects.filter(branch__id=branch)
        
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

@utils.branch_required(utils.is_auth_and_has_branch)
def agent_lookup(request):
    if request.method == 'GET':
        queryset = models.Agent.objects.all()

        rank = request.GET.get('rank')
        if rank:
            print(rank)
            queryset = queryset.filter(rank=rank)

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
