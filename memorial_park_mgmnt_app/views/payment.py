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
class PaymentCreateView(TemplateView):
    template_name = 'payment/create.html'

    def get(self, request, bill_id):
        bill = get_object_or_404(models.Bill, pk=bill_id)
        branch_id = request.session.get('branch_id')
        if bill.contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        form = forms.PaymentForm()
        context_dict = {'bill': bill,
                        'form': form}

        return render(request, self.template_name, context_dict)

    def post(self, request, bill_id):
        form = forms.PaymentForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.bill_id = bill_id
            instance.save()

            msg = 'Successfully created new Payment: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('bill_read', kwargs={'bill_id': instance.bill.id}))

        else:
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class PaymentUpdateView(TemplateView):
    template_name = 'payment/update.html'

    def get(self, request, bill_id, payment_id):
        bill = get_object_or_404(models.Bill, pk=bill_id)
        instance = get_object_or_404(models.Payment, pk=payment_id)
        branch_id = request.session.get('branch_id')
        if bill.contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        form = forms.PaymentForm(instance=instance)
        context_dict = {'bill': bill,
                        'form': form}

        return render(request, self.template_name, context_dict)

    def post(self, request, bill_id, payment_id):
        bill = get_object_or_404(models.Bill, pk=bill_id)
        instance = get_object_or_404(models.Payment, pk=payment_id)
        branch_id = request.session.get('branch_id')
        if bill.contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        form = forms.PaymentForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully updated Payment: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('home'))

        else:
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)
