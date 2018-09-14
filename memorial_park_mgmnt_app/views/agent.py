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
class AgentListView(TemplateView):
    template_name = 'agent/list.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class AgentJson(BaseDatatableView):
    model = models.Agent
    columns = ['name', 'main_address', 'contact_number']
    order_columns = [['last_name', 'first_name', 'middle_name'], None, '']

    def get_initial_queryset(self):
        branches = utils.get_branches(self.request.user)
        return models.Agent.objects.filter(branch__id__in=branches)

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


@method_decorator(login_required, name='dispatch')
class AgentCreateView(TemplateView):
    template_name = 'agent/create.html'

    def get(self, request):
        form = forms.AgentForm()
        form.base_fields['valid_id'].required = False
        context_dict = {'form': form}

        return render(request, self.template_name, context_dict)

    def post(self, request):
        form = forms.AgentForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully created new agent: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('agent_list'))

        else:
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)


@method_decorator(login_required, name='dispatch')
class AgentUpdateView(TemplateView):
    template_name = 'agent/update.html'

    def get(self, request, agent_id):
        instance = get_object_or_404(models.Agent, pk=agent_id)
        form = forms.AgentForm(instance=instance)
        context_dict = {'form': form}

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
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)
