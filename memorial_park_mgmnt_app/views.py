from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
from django.utils.html import escape
from django.db.models import Q
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django_datatables_view.base_datatable_view import BaseDatatableView

from memorial_park_mgmnt_app import models
from memorial_park_mgmnt_app import forms


class LoginView(TemplateView):

    def get(self, request):
        template = 'login.html'
        redirect = request.GET.get('next', reverse('home'))
        context_dict = {'redirect_to': redirect}

        if request.user.is_authenticated:
            return HttpResponseRedirect(redirect)

        return render(request, template, context_dict)

    def post(self, request):
        template = 'login.html'
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                redirect = request.GET.get('next', reverse('home'))
                return HttpResponseRedirect(redirect)
            else:
                msg = 'User is inactive.'
                messages.error(request, msg)
                return render(request, template_name)
        else:
            msg = 'Invalid username and/or password'
            messages.error(request, msg)
            return render(request, template)


@method_decorator(login_required, name='dispatch')
class LogoutView(TemplateView):

    def get(self, request):
        logout(request)
        return redirect(reverse('login'))


@method_decorator(login_required, name='dispatch')
class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request):
        res = models.Client.objects.all().order_by('last_name', 'first_name', 'middle_name')
        return render(request, self.template_name, {'clients': res})


@method_decorator(login_required, name='dispatch')
class ContractListView(TemplateView):
    template_name = 'contract_list.html'

    def get(self, request):
        query = request.GET.get('query', None)
        if query:
            data = models.Contract.objects.filter(Q(date__year=query) |
                                                  Q(date__month=query) |
                                                  Q(date__day=query) |
                                                  Q(client__first_name__icontains=query) |
                                                  Q(client__last_name__icontains=query) |
                                                  Q(client__middle_name__icontains=query) |
                                                  Q(lot__block__icontains=query) |
                                                  Q(lot__lot__icontains=query) |
                                                  Q(lot__unit__icontains=query))
            data = data.order_by('-date',
                                 Lower('client__last_name'),
                                 Lower('client__first_name'),
                                 Lower('client__middle_name'))
        else:
            data = models.Contract.objects.all().order_by('-date',
                                                          Lower('client__last_name'),
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


@method_decorator(login_required, name='dispatch')
class ContractReadView(TemplateView):
    template_name = 'contract_read.html'

    def get(self, request, contract_id):
        instance = get_object_or_404(models.Contract, pk=contract_id)

        data = {
            'contract': instance,
            'downpayments': instance.downpayments.all().order_by('-date'),
            'commissions': instance.commissions.all().order_by('-date'),
            'commission_dist': instance.get_commissions()
        }

        return render(request, self.template_name, data)


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class ContractCreateView(TemplateView):
    template_name = 'contract_create.html'

    def get(self, request):
        form = forms.ContractForm()

        context_dict = {
            'form': form
        }

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
            context_dict = {
                'form': form
            }

            return render(request, self.template_name, context_dict)


@method_decorator(login_required, name='dispatch')
class ContractJson(BaseDatatableView):
    model = models.Contract
    columns = ['date', 'name', 'lot']
    order_columns = ['date',
                     ['client__last_name', 'client__first_name'],
                     ['lot__block', 'lot__lot', 'lot__unit']]

    def get_initial_queryset(self):
        return models.Contract.objects.all()

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

            queryset = queryset.filter(Q(date__year=search) |
                                       Q(date__month=search) |
                                       Q(date__day=search) |
                                       Q(client__last_name__icontains=search) |
                                       Q(client__first_name__icontains=search) |
                                       Q(lot__block__icontains=search) |
                                       Q(lot__lot__icontains=search) |
                                       Q(lot__unit__icontains=search))
        return queryset


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class ClientUpdateView(TemplateView):
    template_name = 'client_update.html'

    def get(self, request, client_id):
        instance = get_object_or_404(models.Client, pk=client_id)
        form = forms.ClientForm(instance=instance)
        form.base_fields['valid_id'].required = False

        context_dict = {
            'form': form
        }

        return render(request, self.template_name, context_dict)

    def post(self, request, client_id):
        instance = get_object_or_404(models.Client, pk=client_id)
        form = forms.ClientForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully updated client: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('client_list'))

        else:
            context_dict = {
                'form': form
            }

            return render(request, self.template_name, context_dict)


@method_decorator(login_required, name='dispatch')
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
        form.base_fields['valid_id'].required = False

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


@method_decorator(login_required, name='dispatch')
class ClientListView(TemplateView):
    template_name = 'client_list.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class ClientJson(BaseDatatableView):
    model = models.Client
    columns = ['name', 'main_address', 'contact_number']
    order_columns = [['last_name', 'first_name', 'middle_name'], None, '']

    def get_initial_queryset(self):
        return models.Client.objects.all()

    def render_column(self, row, column):
        if column == 'name':
            url = reverse('agent_update', kwargs={'agent_id': row.id})
            text = '{0}, {1}'.format(row.last_name.upper(), row.first_name)
            html = '<a href="{0}">{1}</a>'.format(url, text)
            return html
        else:
            return super(ClientJson, self).render_column(row, column)

    def filter_queryset(self, queryset):
        search = self.request.GET.get('search[value]', None)
        if search:

            queryset = queryset.filter(Q(last_name__icontains=search) |
                                       Q(first_name__icontains=search) |
                                       Q(street__icontains=search) |
                                       Q(barangay__icontains=search) |
                                       Q(town__icontains=search) |
                                       Q(province__icontains=search))
        return queryset


@method_decorator(login_required, name='dispatch')
class AgentUpdateView(TemplateView):
    template_name = 'agent_update.html'

    def get(self, request, agent_id):
        instance = get_object_or_404(models.Agent, pk=agent_id)
        form = forms.AgentForm(instance=instance)
        form.base_fields['valid_id'].required = False

        context_dict = {
            'form': form
        }

        return render(request, self.template_name, context_dict)

    def post(self, request, agent_id):
        instance = get_object_or_404(models.Agent, pk=agent_id)
        form = forms.AgentForm(request.POST, request.FILES, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully updated agent: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('agent_list'))

        else:
            context_dict = {
                'form': form
            }

            return render(request, self.template_name, context_dict)


@method_decorator(login_required, name='dispatch')
class AgentCreateView(TemplateView):
    template_name = 'agent_create.html'

    def get(self, request):
        form = forms.AgentForm()
        form.base_fields['valid_id'].required = False

        context_dict = {
            'form': form
        }

        return render(request, self.template_name, context_dict)

    def post(self, request):
        form = forms.AgentForm(request.POST, request.FILES)
        form.base_fields['valid_id'].required = False

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully created new agent: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('agent_list'))

        else:
            print(form.errors)
            context_dict = {
                'form': form
            }

            return render(request, self.template_name, context_dict)

@method_decorator(login_required, name='dispatch')
class AgentListView(TemplateView):
    template_name = 'agent_list.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class AgentJson(BaseDatatableView):
    model = models.Agent
    columns = ['name', 'main_address', 'contact_number']
    order_columns = [['last_name', 'first_name', 'middle_name'], None, '']

    def get_initial_queryset(self):
        return models.Agent.objects.all()

    def render_column(self, row, column):
        if column == 'name':
            url = reverse('agent_update', kwargs={'agent_id': row.id})
            text = '{0}, {1}'.format(row.last_name.upper(), row.first_name)
            html = '<a href="{0}">{1}</a>'.format(url, text)
            return html
            # return escape('{0}, {1}'.format(row.last_name.upper(), row.first_name))
        else:
            return super(AgentJson, self).render_column(row, column)

    def filter_queryset(self, queryset):
        search = self.request.GET.get('search[value]', None)
        if search:

            queryset = queryset.filter(Q(last_name__icontains=search) |
                                       Q(first_name__icontains=search) |
                                       Q(street__icontains=search) |
                                       Q(barangay__icontains=search) |
                                       Q(town__icontains=search) |
                                       Q(province__icontains=search))
        return queryset

### Lookups ###
from django.http import JsonResponse

def lot_lookup(request):
    if request.method == 'GET':
        queryset = models.Lot.objects.all()
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

def client_lookup(request):
    if request.method == 'GET':
        queryset = models.Client.objects.all()
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

def agent_lookup(request):
    if request.method == 'GET':
        queryset = models.Agent.objects.all()
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
