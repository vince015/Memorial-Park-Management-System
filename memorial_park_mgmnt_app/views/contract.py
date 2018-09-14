from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.utils.html import escape

from django_datatables_view.base_datatable_view import BaseDatatableView

from memorial_park_mgmnt_app import models, forms
from utils import utils


@method_decorator(login_required, name='dispatch')
class ContractListView(TemplateView):
    template_name = 'contract/list.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class ContractJson(BaseDatatableView):
    model = models.Contract
    columns = ['date', 'name', 'lot']
    order_columns = ['date',
                     ['client__last_name', 'client__first_name'],
                     ['lot__block', 'lot__lot', 'lot__unit']]

    def get_initial_queryset(self):
        print(self.request.session.get('branch_id'))
        branch = self.request.session.get('branch_id')
        return models.Contract.objects.filter(lot__branch__id=branch)

    def render_column(self, row, column):
        if column == 'date':
            url = reverse('contract_read', kwargs={'contract_id': row.id})
            text = row.date.strftime('%Y-%m-%d')
            html = '<a href="{0}">{1}</a>'.format(url, text)
            return html
        elif column == 'name':
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


@method_decorator(login_required, name='dispatch')
class ContractCreateView(TemplateView):
    template_name = 'contract/create.html'

    def get(self, request):
        form = forms.ContractForm()
        context_dict = {'form': form}

        return render(request, self.template_name, context_dict)

    def post(self, request):
        form = forms.ContractForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully created new Contract: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('home'))

        else:
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)
