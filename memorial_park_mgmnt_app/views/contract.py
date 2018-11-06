from datedelta import datedelta
from datetime import datetime, date, timedelta

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
class ContractListView(TemplateView):
    template_name = 'contract/list.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ContractJson(BaseDatatableView):
    model = models.Contract
    columns = ['number', 'date', 'name', 'lot']
    order_columns = ['number',
                     'date',
                     ['client__last_name', 'client__first_name'],
                     ['lot__block', 'lot__lot', 'lot__unit']]

    def get_initial_queryset(self):
        branch = self.request.session.get('branch_id')
        queryset = models.Contract.objects.filter(lot__branch__id=branch)

        # filter_overdue = self.request.GET.get('overdue', False)
        # print(filter_overdue)
        # if filter_overdue == True:
        #     queryset = queryset.filter(bills__is_overdue=True)

        return queryset

    def render_column(self, row, column):
        if column == 'number':
            url = reverse('contract_read', kwargs={'contract_id': row.id})
            text = row.number
            html = '<a href="{0}"><i class="fa fa-chevron-circle-right"></i> {1}</a>'.format(url, text)
            return html
        elif column == 'date':
            return row.date.strftime('%Y-%m-%d')
        elif column == 'name':
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


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ContractCreateView(TemplateView):
    template_name = 'contract/create.html'

    def get(self, request):
        form = forms.ContractForm()
        context_dict = {'form': form}

        return render(request, self.template_name, context_dict)

    def post(self, request):
        form = forms.ContractForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)

            if form.cleaned_data.get('payment_terms') == 'SPOT':
                today = date.today()
                spot_promo = models.SpotPromo.objects.filter(start_date__lte=today,
                                                             end_date__gte=today).first()
                if spot_promo:
                    instance.save()
                    models.SpotOption.objects.create(discount=spot_promo.discount,
                                                     contract=instance)

                    models.Bill.objects.create(amount_due=instance.contract_price,
                                               contract=instance,
                                               remarks='For spot cash payment')

                    return redirect(reverse('contract_read', kwargs={'contract_id': instance.id}))
                else:
                    msg = 'No available Spot Option Promo. Kindly report to admin'
                    messages.error(request, msg)

                    context_dict = {'form': form}
                    return render(request, self.template_name, context_dict)
            else:
                instance.save()
                return redirect(reverse('contract_installment', kwargs={'contract_id': instance.id}))

        else:
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ContractUpdateView(TemplateView):
    template_name = 'contract/update.html'

    def get(self, request, contract_id):
        instance = get_object_or_404(models.Contract, pk=contract_id)
        branch_id = request.session.get('branch_id')
        if instance.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        form = forms.ContractUpdateForm(instance=instance)
        context_dict = {'form': form}

        return render(request, self.template_name, context_dict)

    def post(self, request, contract_id):
        instance = get_object_or_404(models.Contract, pk=contract_id)
        branch_id = request.session.get('branch_id')
        if instance.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        form = forms.ContractUpdateForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully updated Contract No. {0}'.format(instance.number)
            messages.success(request, msg)

            return redirect(reverse('contract_read', kwargs={'contract_id': instance.id}))

        else:
            print(form.errors)
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ContractReadView(TemplateView):
    template_name = 'contract/read.html'

    def __generate_bills(self, contract):

        if contract.payment_terms == 'SPOT':
            models.Bill.objects.create(start=contract.date,
                                       end=contract.date,
                                       issue_date=contract.date,
                                       due_date=contract.date,
                                       amount_due=contract.contract_price,
                                       remarks='Spot cash',
                                       contract=contract)

        else:
            start_date = contract.date
            for split in range(0, contract.installment_option.split):
                end_date = contract.date + datedelta(months=(split + 1))
                issue_date = end_date - timedelta(days=5)

                models.Bill.objects.create(start=start_date,
                                           end=end_date,
                                           issue_date=issue_date,
                                           due_date=end_date,
                                           amount_due=contract.downpayment_monthly,
                                           contract=contract)

                start_date = end_date + timedelta(days=1)

            split = split + 1
            for month in range(0, contract.installment_option.months):
                end_date = contract.date + datedelta(months=(split + month + 1))
                issue_date = end_date - timedelta(days=5)

                models.Bill.objects.create(start=start_date,
                                           end=end_date,
                                           issue_date=issue_date,
                                           due_date=end_date,
                                           amount_due=contract.installment_monthly,
                                           contract=contract)

                start_date = end_date + timedelta(days=1)

    def get(self, request, contract_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)
        branch_id = request.session.get('branch_id')
        if contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        if contract.payment_terms == 'SPOT' and not hasattr(contract, 'spot_option'):
            return redirect(reverse('contract_spot', kwargs={'contract_id': contract.id}))
        elif contract.payment_terms == 'INSTALLMENT' and not hasattr(contract, 'installment_option'):
            return redirect(reverse('contract_installment', kwargs={'contract_id': contract.id}))

        if request.GET.get('generate', False) and len(contract.bills.all()) < 1:
            self.__generate_bills(contract)

        context_dict = {
            'contract': contract,
            'commission_dist': contract.get_commissions()
        }

        return render(request, self.template_name, context_dict)


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ContractSpotView(TemplateView):
    template_name = 'contract/spot_payment.html'

    def get(self, request, contract_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)
        branch_id = request.session.get('branch_id')
        if contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        if contract.payment_terms == 'INSTALLMENT':
            return redirect(reverse('contract_installment', kwargs={'contract_id': contract.id}))

        form = forms.PaymentForm()
        context_dict = {
            'contract': contract,
            'form': form
        }

        return render(request, self.template_name, context_dict)

    def post(self, request, contract_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)
        branch_id = request.session.get('branch_id')
        if contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        if contract.payment_terms == 'INSTALLMENT':
            return redirect(reverse('contract_installment', kwargs={'contract_id': contract.id}))

        form = forms.PaymentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.payment_type = 'SPOT_CASH'

            target_bill = contract.bills.all().first()
            instance.bill = target_bill
            instance.save()

            if target_bill.is_paid:
                target_bill.status = 'PAID'
                target_bill.save()

            msg = 'Successfully created new Contract: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('contract_read', kwargs={'contract_id': contract.id}))

        else:
            context_dict = {
                'contract': contract,
                'form': form
            }
            return render(request, self.template_name, context_dict)


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ContractInstallmentView(TemplateView):
    template_name = 'contract/installment_payment.html'

    def get(self, request, contract_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)
        branch_id = request.session.get('branch_id')
        if contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        if contract.payment_terms == 'SPOT':
            return redirect(reverse('contract_spot', kwargs={'contract_id': contract.id}))

        form = forms.InstallmentOptionForm()
        context_dict = {
            'form': form,
            'contract': contract
        }

        return render(request, self.template_name, context_dict)

    def post(self, request, contract_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)
        branch_id = request.session.get('branch_id')
        if contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        form = forms.InstallmentOptionForm(request.POST)
        if form.is_valid():
            downpayment = form.cleaned_data['downpayment_option']
            installment = form.cleaned_data['installment_option']

            models.InstallmentOption.objects.create(split=downpayment.split,
                                                    discount=downpayment.discount,
                                                    months=installment.months,
                                                    interest=installment.interest,
                                                    contract=contract)

            msg = 'Successfully created new Contract: {0}'.format(str(contract))
            messages.success(request, msg)

            return redirect(reverse('contract_read', kwargs={'contract_id': contract.id}))

        else:
            context_dict = {
                'form': form,
                'contract': contract
            }
            return render(request, self.template_name, context_dict)


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ContractInstallmentComputeView(TemplateView):
    template_name = 'contract/info.html'

    def post(self, request, contract_id):
        contract = get_object_or_404(models.Contract, pk=contract_id)
        branch_id = request.session.get('branch_id')
        if contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        downpayment_option_id = request.data.get('downpayment_option', 0)
        downpayment_option = models.DownpaymentOption.objects.get(pk=downpayment_option_id)

        downpayment = (contract.lot.price + contract.lot.lot_type.care_fund) * 0.2
        downpayment = downpayment - (downpayment * downpayment_option.discount)

        installment_option_id = request.data.get('installment_option', 0)
        installment_option = models.InstallmentOption.objects.get(pk=installment_option_id)

        installment = (contract.lot.price + contract.lot.lot_type.care_fund) * 0.8
        installment = installment - (installment * installment_option.discount)

        context_dict = {
            'downpayment': downpayment,
            'installment': installment,
            'total': downpayment + installment
        }

        return render(request, self.template_name, context_dict)


@utils.branch_required(utils.is_auth_and_has_branch)
def contract_forfeit(request, contract_id):

    if request.method == 'POST':
        contract = get_object_or_404(models.Contract, pk=contract_id)
        branch_id = request.session.get('branch_id')
        if contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        contract.status = 'FORFEITED'
        contract.save()

        return redirect(reverse('contract_read', kwargs={'contract_id': contract.id}))


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class ContractResultsView(TemplateView):
    template_name = 'payment/add.html'

    def get(self, request):
        branch_id = request.session.get('branch_id')

        query = request.GET.get('q')
        if query:
            branch_id = request.session.get('branch_id')
            contract_list = models.Contract.objects.filter(Q(lot__id=branch_id) &
                                                           Q(client__first_name__icontains=query) |
                                                           Q(client__last_name__icontains=query) |
                                                           Q(client__middle_name__icontains=query))
            contract_list = contract_list.order_by('client__last_name', 'client__first_name')
        else:
            contract_list = models.Contract.objects.filter(contract__lot__id=branch_id).order_by('-timestamp')

        page = request.GET.get('page', 1)

        paginator = Paginator(contract_list, 25)
        try:
            contracts = paginator.page(page)
        except PageNotAnInteger:
            contracts = paginator.page(1)
        except EmptyPage:
            contracts = paginator.page(paginator.num_pages)

        context_dict = {'contracts': contracts}

        return render(request, self.template_name, context_dict)
