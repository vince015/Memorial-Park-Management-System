from datetime import date, datetime

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
    columns = ['period', 'due_date', 'amount_due', 'amount_paid']
    order_columns = [['start', 'end'],
                      'due_date',
                      '',
                      ''
                    ]

    def get_initial_queryset(self):
        queryset = models.Bill.objects.all()

        contract_id =  self.request.GET.get('contract_id')
        if contract_id:
            contract = models.Contract.objects.get(pk=contract_id)

            branch_id = self.request.session.get('branch_id')
            if contract.lot.branch.id == branch_id:
                queryset = contract.bills.all()
        else:
            queryset = models.Bill.objects.filter(contract__lot__branch__id=branch_id)

        return queryset

    def filter_queryset(self, queryset):
        until = self.request.GET.get('until')
        if until:
            until = datetime.fromtimestamp(int(until)/1000).date()
            queryset = queryset.filter(start__lte=until)

        # is_overdue = self.request.GET.get('is_overdue')
        # is_paid = self.request.GET.get('is_paid')
        # if is_overdue is not None and is_paid is not None:
        #     excluded = []
        #     for bill in queryset:
        #         if (bill.is_overdue != bool(is_overdue.title()) and
        #             bill.is_paid != bool(is_paid.title())):
        #             excluded.append(bill.pk)

        # queryset = queryset.exclude(id__in=excluded)
        return queryset

    def render_column(self, row, column):
        if column == 'period':
            url = reverse('bill_read', kwargs={'bill_id': row.id})
            text = '{0} TO {1}'.format(row.start.strftime('%b %d, %Y'), row.end.strftime('%b %d, %Y'))
            html = '<a href="{0}">{1}</a>'.format(url, text)
            return html
        if column == 'amount_due':
            text = '{0:.2f}'.format(row.total_amount_due)
            if row.is_paid:
                html = '<span class="text-green">{0}</span>'.format(text)
            elif row.is_overdue:
                html = '<span class="text-red">{0}</span>'.format(text)
            else:
                html = text

            return html
        if column == 'amount_paid':
            return '{0:.2f}'.format(row.total_amount_paid)
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

@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class BillCommmisionList(TemplateView):
    template_name = 'commission/list.html'

    def get(self, request, bill_id):
        bill = get_object_or_404(models.Bill, pk=bill_id)
        branch_id = request.session.get('branch_id')
        if bill.contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        context_dict = {
            'commissions': bill.commission_set.all().order_by('-created')
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
