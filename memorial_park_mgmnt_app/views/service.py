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
class ServiceCreateView(TemplateView):
    template_name = 'service/create.html'

    def get(self, request, contract_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)
        branch_id = request.session.get('branch_id')
        if contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        form = forms.ServiceForm()
        context_dict = {
            'contract': contract,
            'form': form
        }

        return render(request, self.template_name, context_dict)

    def post(self, request, contract_id):
        form = forms.ServiceForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.contract_id = contract_id
            instance.save()

            msg = 'Successfully created new Service: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('contract_read', kwargs={'contract_id': instance.contract.id}))

        else:
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)
