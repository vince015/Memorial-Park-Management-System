from django.views.generic import TemplateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils.html import escape
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404

from django_datatables_view.base_datatable_view import BaseDatatableView

from memorial_park_mgmnt_app import models

import json, re

class HomeView(TemplateView):
    template_name = 'home2.html'

    def get(self, request):
        res = models.Client.objects.all().order_by('last_name', 'first_name', 'middle_name')
        return render(request, self.template_name, {'clients': res})


class ContractListView(TemplateView):
    template_name = 'contract_list.html'

    def get(self, request):
        query = request.GET.get('query', None)
        if query:
            data = models.Contract.objects.filter(Q(client__first_name__icontains=query) |
                                                  Q(client__last_name__icontains=query) |
                                                  Q(client__middle_name__icontains=query))
            data = data.order_by(Lower('client__last_name'),
                                 Lower('client__first_name'),
                                 Lower('client__middle_name'))
        else:
            data = models.Contract.objects.all().order_by(Lower('client__last_name'),
                                                          Lower('client__first_name'),
                                                          Lower('client__middle_name'))

        page = request.GET.get('page', 1)
        paginator = Paginator(data, 25)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {'contracts': data})


class ContractReadView(TemplateView):
    template_name = 'contract_read.html'

    def get(self, request, contract_id):
        instance = get_object_or_404(models.Contract, pk=contract_id)

        data = {
            'contract': instance,
            'downpayments': instance.downpayments.all().order_by('-date'),
            'commissions': instance.commissions.all().order_by('-date')
        }

        return render(request, self.template_name, data)

class ContractJson(BaseDatatableView):
    model = models.Contract
    columns = ['name', 'lot']
    order_columns = [['client__last_name', 'client__first_name'],
                     ['lot__block', 'lot__lot', 'lot__unit']]

    def get_initial_queryset(self):
        return models.Contract.objects.all()

    def render_column(self, row, column):
        if column == 'name':
            return escape('{0}, {1}'.format(row.client.last_name.upper(), row.client.first_name))
        elif column == 'lot':
            return escape('{0}'.format(str(row.lot)))
        else:
            return super(ContractJson, self).render_column(row, column)

    def filter_queryset(self, queryset):
        search = self.request.GET.get('search[value]', None)
        if search:

            queryset = queryset.filter(Q(client__last_name__icontains=search) |
                                       Q(client__first_name__icontains=search) |
                                       Q(lot__block__icontains=search) |
                                       Q(lot__lot__icontains=search) |
                                       Q(lot__unit__icontains=search))
        return queryset
