from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from django_datatables_view.base_datatable_view import BaseDatatableView

from memorial_park_mgmnt_app import models, forms
from utils import utils


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ClientListView(TemplateView):
    template_name = 'client/list.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ClientJson(BaseDatatableView):
    model = models.Client
    columns = ['name', 'main_address', 'contact_number']
    order_columns = [['last_name', 'first_name', 'middle_name'], None, '']

    def get_initial_queryset(self):
        branch = self.request.session.get('branch_id')
        return models.Client.objects.filter(branch__id=branch)

    def render_column(self, row, column):
        if column == 'name':
            url = reverse('client_update', kwargs={'client_id': row.id})
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


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ClientCreateView(TemplateView):
    template_name = 'client/create.html'

    def get(self, request):
        form = forms.ClientForm()
        form.base_fields['valid_id'].required = False
        context_dict = {'form': form}

        return render(request, self.template_name, context_dict)

    def post(self, request):
        form = forms.ClientForm(request.POST, request.FILES)
        form.base_fields['valid_id'].required = False

        if form.is_valid():
            instance = form.save(commit=False)
            branch_id = request.session.get('branch_id')
            instance.branch_id = branch_id
            instance.save()

            msg = 'Successfully created new client: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('client_list'))

        else:
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ClientUpdateView(TemplateView):
    template_name = 'client/update.html'

    def get(self, request, client_id):
        instance = get_object_or_404(models.Client, pk=client_id)
        branch_id = request.session.get('branch_id')
        if instance.branch.id != branch_id:
            return HttpResponseForbidden()

        form = forms.ClientForm(instance=instance)
        form.base_fields['valid_id'].required = False
        context_dict = {'form': form}

        return render(request, self.template_name, context_dict)

    def post(self, request, client_id):
        instance = get_object_or_404(models.Client, pk=client_id)
        branch_id = request.session.get('branch_id')
        if instance.branch.id != branch_id:
            return HttpResponseForbidden()

        form = forms.ClientForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.branch_id = branch_id
            instance.save()

            msg = 'Successfully updated client: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('client_list'))

        else:
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)
