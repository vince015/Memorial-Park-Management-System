from django.views.generic import TemplateView
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils.html import escape
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

from django_datatables_view.base_datatable_view import BaseDatatableView

from memorial_park_mgmnt_app import models
from memorial_park_mgmnt_app import forms


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


class ContractUpdateView(TemplateView):
    template_name = 'contract_update.html'

    def get(self, request, contract_id):
        instance = get_object_or_404(models.Contract, pk=contract_id)
        form = forms.ContractForm(instance=instance)

        context_dict = {
            'form': form
        }

        return render(request, self.template_name, context_dict)

    def post(self, request, contract_id):
        instance = get_object_or_404(models.Contract, pk=contract_id)
        form = forms.ContractForm(request.POST, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully updated Contract {0}'.format(instance.id)
            messages.success(request, msg)

            return redirect(reverse('contract_read', kwargs={'contract_id': instance.id}))

        else:
            context_dict = {
                'form': form
            }

            return render(request, self.template_name, context_dict)


class ContractCreateView(TemplateView):
    template_name = 'contract_create.html'

    def get(self, request):
        form = forms.ContractForm()

        context_dict = {
            'form': form
        }

        return render(request, self.template_name, context_dict)

    def post(self, request, contract_id):
        form = forms.contractForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully created new Contract: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('home'))

        else:
            context_dict = {
                'form': form
            }

            return render(request, self.template_name, context_dict)


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


class DownpaymentCreateView(TemplateView):
    template_name = 'downpayment_create.html'

    def get(self, request, contract_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)
        form = forms.DownpaymentForm()

        context_dict = {
            'contract': contract,
            'form': form
        }

        return render(request, self.template_name, context_dict)

    def post(self, request, contract_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)
        form = forms.DownpaymentForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.contract = contract
            instance.save()

        context_dict = {
            'contract': contract,
            'form': form
        }
        messages.success(request, 'Successfully added a new commission for this Contract.')

        return redirect(reverse('contract_read', kwargs={'contract_id': contract.id}) + '?active=downpayments')


class CommissionCreateView(TemplateView):
    template_name = 'commission_create.html'

    def get(self, request, contract_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)
        form = forms.CommissionForm()

        context_dict = {
            'contract': contract,
            'form': form
        }

        return render(request, self.template_name, context_dict)

    def post(self, request, contract_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)
        form = forms.CommissionForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.contract = contract
            instance.save()

            messages.success(request, 'Successfully added a new commission for this Contract.')
            return redirect(reverse('contract_read', kwargs={'contract_id': contract.id}) + '?active=commissions')

        context_dict = {
            'contract': contract,
            'form': form
        }

        return render(request, self.template_name, context_dict)


class ClientUpdateView(TemplateView):
    template_name = 'client_update.html'

    def get(self, request, contract_id, client_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)

        instance = get_object_or_404(models.Client, pk=client_id)
        form = forms.ClientForm(instance=instance)
        form.base_fields['valid_id'].required = False

        context_dict = {
            'contract': contract,
            'form': form
        }

        return render(request, self.template_name, context_dict)

    def post(self, request, contract_id, client_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)

        instance = get_object_or_404(models.Client, pk=client_id)
        form = forms.ClientForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully updated client: {0}'.format(str(instance))
            messages.success(request, msg)

            return render(request, self.template_name, context_dict)

        else:
            context_dict = {
                'contract': contract,
                'form': form
            }

            return render(request, self.template_name, context_dict)


class ClientCreateView(TemplateView):
    template_name = 'client_create.html'

    def get(self, request):
        form = forms.ClientForm()
        form.base_fields['valid_id'].required = False

        context_dict = {
            'form': form
        }

        return render(request, self.template_name, context_dict)

    def post(self, request):
        form = forms.ClientForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully created new client: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('home'))

        else:
            context_dict = {
                'form': form
            }

            return render(request, self.template_name, context_dict)


class AgentUpdateView(TemplateView):
    template_name = 'agent_update.html'

    def get(self, request, contract_id, agent_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)

        instance = get_object_or_404(models.Agent, pk=agent_id)
        form = forms.AgentForm(instance=instance)
        form.base_fields['valid_id'].required = False

        context_dict = {
            'contract': contract,
            'form': form
        }

        return render(request, self.template_name, context_dict)

    def post(self, request, contract_id, agent_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)

        instance = get_object_or_404(models.Agent, pk=Agent_id)
        form = forms.agentForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully updated agent: {0}'.format(str(instance))
            messages.success(request, msg)

            return render(request, self.template_name, context_dict)

        else:
            context_dict = {
                'contract': contract,
                'form': form
            }

            return render(request, self.template_name, context_dict)


class AgentCreateView(TemplateView):
    template_name = 'agent_create.html'

    def get(self, request):
        form = forms.AgentForm()
        form.base_fields['valid_id'].required = False

        context_dict = {
            'form': form
        }

        return render(request, self.template_name, context_dict)

    def post(self, request, agent_id):
        form = forms.agentForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully created new agent: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('home'))

        else:
            context_dict = {
                'form': form
            }

            return render(request, self.template_name, context_dict)
