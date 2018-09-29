from datetime import date

from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from django_datatables_view.base_datatable_view import BaseDatatableView

from memorial_park_mgmnt_app import models, forms
from utils import utils


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class BillJson(BaseDatatableView):
    model = models.Bill
    columns = ['period', 'due_date', 'amount_due']
    order_columns = [['start', 'end'],
                      'due_date',
                      'amount_due'
                    ]

    def get_initial_queryset(self):
        queryset = models.Bill.objects.all()

        contract_id =  self.request.GET.get('contract_id')
        if contract_id:
            contract = models.Contract.objects.get(pk=contract_id)

            branch = self.request.session.get('branch_id')
            if contract.lot.branch.id == branch:
                queryset = contract.bills.all()

        return queryset

    def render_column(self, row, column):
        if column == 'period':
            url = reverse('bill_read', kwargs={'bill_id': row.id})
            text = '{0} TO {1}'.format(row.start.strftime('%b %d, %Y'), row.end.strftime('%b %d, %Y'))
            html = '<a href="{0}">{1}</a>'.format(url, text)
            return html
        if column == 'amount_due':
            text = '{0:.2f}'.format(row.total_amount_due)
            if row.status == 'PAID':
                html = '<span class="text-green">{0}</span>'.format(text)
            elif row.status == 'OVERDUE':
                html = '<span class="text-red">{0}</span>'.format(text)
            else:
                html = text

            return html
        else:
            return super(BillJson, self).render_column(row, column)


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class BillReadView(TemplateView):
    template_name = 'bill/read.html'

    def get(self, request, bill_id):
        bill = get_object_or_404(models.Bill, pk=bill_id)
        branch_id = request.session.get('branch_id')
        if bill.contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        form = forms.BillStatusForm(instance=bill)
        context_dict = {
            'bill': bill,
            'form': form
        }

        return render(request, self.template_name, context_dict)

@utils.branch_required(utils.is_auth_and_has_branch)
def bill_update_status(request, bill_id):

    if request.method == 'POST':
        bill = get_object_or_404(models.Bill, pk=bill_id)
        branch_id = request.session.get('branch_id')
        if bill.contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        form = forms.BillStatusForm(request.POST, instance=bill)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully updated Bill'
            messages.success(request, msg)
        else:
            msg = 'Error in updating Bill'
            messages.error(request, msg)

        return redirect(reverse('bill_read', kwargs={'bill_id': bill.id}))

@utils.branch_required(utils.is_auth_and_has_branch)
def bill_mark_as_overdue(request, bill_id):

    if request.method == 'POST':
        bill = get_object_or_404(models.Bill, pk=bill_id)
        branch_id = request.session.get('branch_id')
        if bill.contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        bill.is_overdue = True
        bill.save()

        return redirect(reverse('bill_read', kwargs={'bill_id': bill.id}))
