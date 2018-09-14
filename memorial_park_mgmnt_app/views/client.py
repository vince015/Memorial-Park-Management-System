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
class ClientListView(TemplateView):
    template_name = 'client/list.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class ClientJson(BaseDatatableView):
    model = models.Client
    columns = ['name', 'main_address', 'contact_number']
    order_columns = [['last_name', 'first_name', 'middle_name'], None, '']

    def get_initial_queryset(self):
        branches = utils.get_branches(self.request.user)
        return models.Client.objects.filter(branch__id__in=branches)

    def render_column(self, row, column):
        if column == 'name':
            # url = reverse('client_update', kwargs={'client_id': row.id})
            url = '#'
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
            instance.save()

            msg = 'Successfully created new client: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('client_list'))

        else:
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)


@method_decorator(login_required, name='dispatch')
class ClientUpdateView(TemplateView):
    template_name = 'client/update.html'

    def get(self, request, client_id):
        branches = utils.get_branches(request.user)
        queryset = models.Client.objects.filter(branch__id__in=branches)
        instance = queryset.get(pk=client_id)

        form = forms.ClientForm(instance=instance)
        form.base_fields['valid_id'].required = False
        context_dict = {'form': form}

        return render(request, self.template_name, context_dict)

    def post(self, request, client_id):
        branches = utils.get_branches(request.user)
        queryset = models.Client.objects.filter(branch__id__in=branches)
        instance = queryset.get(pk=client_id)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully updated client: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('client_list'))

        else:
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)
