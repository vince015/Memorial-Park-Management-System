import re

from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from memorial_park_mgmnt_app import models, forms
from utils import utils


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ReceiptCreateView(TemplateView):
    template_name = 'receipt/create.html'

    def get(self, request):
        form = forms.ReceiptForm(initial={'amount': '0.00'})
        context_dict = {'form': form}
        return render(request, self.template_name, context_dict)

    def post(self, request):

        form = forms.ReceiptForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            branch_id = request.session.get('branch_id')
            instance.branch_id = branch_id
            instance.save()
            return redirect(reverse('receipt_payment', kwargs={'receipt_id': instance.id}))
        else:
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)

@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ReceiptContactView(TemplateView):
    template_name = 'receipt/payment.html'

    def __create_contract_map(self, request_dict):
        contract_mapping = {}

        for item in request_dict.keys():
            status = re.match(r'^(?P<contract_id>[\d]+)-status$', item)
            if status and request_dict[item] == 'on':
                contract_id = status.groupdict().get('contract_id')
                if contract_id:
                    contract_mapping[contract_id] = {'amount': 0, 'instance': None}

            amount = re.match(r'^(?P<contract_id>[\d]+)-amount$', item)
            if amount and float(request_dict[item]) > 0:
                contract_id = amount.groupdict().get('contract_id')
                if contract_id:
                    contract_mapping[contract_id]['amount'] = float(request_dict[item])

        return contract_mapping

    def __process_payment(self, contract_mapping, receipt):
        for contract_id in contract_mapping:
            instance = contract_mapping[contract_id]['instance']
            if instance:
                total_payment_amount = contract_mapping[contract_id]['amount']
                for bill in instance.bills.all().order_by('issue_date'):
                    if total_payment_amount < 1:
                        break

                    payment_amount = bill.total_amount_due
                    if total_payment_amount < bill.total_amount_due:
                        payment_amount = total_payment_amount

                    models.Payment.objects.create(amount=payment_amount,
                                                  bill=bill,
                                                  receipt=receipt)

                    total_payment_amount = total_payment_amount - payment_amount

    def get(self, request, receipt_id):
        receipt = get_object_or_404(models.Receipt, pk=receipt_id)
        context_dict = {'receipt': receipt}

        client_id = request.GET.get('client-id')
        if client_id:
            client = get_object_or_404(models.Client, pk=client_id)
            contracts = models.Contract.objects.filter(client=client)

            context_dict.update({
                'client': client,
                'contracts': contracts
            })

        return render(request, self.template_name, context_dict)

    def post(self, request, receipt_id):
        receipt = get_object_or_404(models.Receipt, pk=receipt_id)
        client = get_object_or_404(models.Client, pk=request.POST.get('client-id', 0))

        contract_mapping = self.__create_contract_map(request.POST)

        ### validate ###
        has_error = False

        total = 0
        for contract_id in contract_mapping.keys():
            total = total + contract_mapping[contract_id].get('amount', 0)

            instance = get_object_or_404(models.Contract, pk=contract_id)
            if instance.client.id != client.id:
                has_error = True
                msg = 'Contract No. {0} does not match client {1}'.format(contract.id, str(client))
                messages.error(request, msg)
                break

            contract_mapping[contract_id]['instance'] = instance

        if total > receipt.amount:
            has_error = True
            msg = 'Total amount in payments ({0:.2f}) cannot be more than indicated amount in receipt ({1:.2f})'.format(total, receipt.amount)
            messages.error(request, msg)
        elif total < receipt.amount:
            has_error = True
            msg = 'Please make sure all {0:.2f} is allocated'.format(receipt.amount)
            messages.error(request, msg)

        if has_error:
            context_dict = {
                'contracts': models.Contract.objects.filter(client=client),
                'client': client,
                'receipt': receipt,
            }
            return render(request, self.template_name, context_dict)
        else:
            self.__process_payment(contract_mapping, receipt)
            msg = 'Successfully added payments'
            messages.success(request, msg)
            return redirect(reverse('home'))

@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ReceiptPaymentView(TemplateView):
    template_name = 'receipt/payment.html'

    def get(self, request, receipt_id):
        receipt = get_object_or_404(models.Receipt, pk=receipt_id)
        context_dict = {'receipt': receipt}
        return render(request, self.template_name, context_dict)
