from datetime import datetime, timedelta

from django.views.generic import TemplateView
from django.shortcuts import render
from django.utils.html import escape
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from django_datatables_view.base_datatable_view import BaseDatatableView

from expense_report import models
from expense_report import forms


@method_decorator(login_required, name='dispatch')
class ExpenseListView(TemplateView):
    template_name = 'expense/list.html'

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class ExpenseJson(BaseDatatableView):
    model = models.Expense
    columns = ['date', 'payee', 'category', 'amount']
    order_columns = ['date', 'payee', 'category', 'amount']

    def get_initial_queryset(self):
        return models.Expense.objects.all()

    def render_column(self, row, column):
        if column == 'date':
            url = reverse('expense_update', kwargs={'expense_id': row.id})
            text = row.date.strftime('%Y-%m-%d')
            html = '<a href="{0}">{1}</a>'.format(url, text)
            return html
        else:
            return super(ExpenseJson, self).render_column(row, column)

    def filter_queryset(self, queryset):
        search = self.request.GET.get('search[value]', None)
        if search:
            queryset = queryset.filter(Q(reference_number__icontains=search) |
                                       Q(payee__icontains=search) |
                                       Q(category__icontains=search))
        return queryset

@method_decorator(login_required, name='dispatch')
class ExpenseCreateView(TemplateView):
    template_name = 'expense/create.html'

    def get(self, request):
        form = forms.ExpenseForm()
        context_dict = {'form': form}

        return render(request, self.template_name, context_dict)

    def post(self, request):
        form = forms.ExpenseForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully created new Expense: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('expense_list'))

        else:
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)


@method_decorator(login_required, name='dispatch')
class ExpenseUpdateView(TemplateView):
    template_name = 'expense/update.html'

    def get(self, request, expense_id):
        instance = models.Expense.objects.get(pk=expense_id)
        form = forms.ExpenseForm(instance=instance)
        context_dict = {'form': form}

        return render(request, self.template_name, context_dict)

    def post(self, request, expense_id):
        instance = models.Expense.objects.get(pk=expense_id)
        form = forms.ExpenseForm(request.POST, instance=instance)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully created updated Expense: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('expense_list'))

        else:
            context_dict = {'form': form}

            return render(request, self.template_name, context_dict)


@method_decorator(login_required, name='dispatch')
class PettyCashListView(TemplateView):
    template_name = 'petty_cash/list.html'

    def get(self, request):
        days = int(request.GET.get('days', 7))

        pst_now = datetime.utcnow() + timedelta(hours=8)
        pst_tomorrow = datetime.combine(pst_now.date(), datetime.min.time()) + timedelta(days=1)
        days_ago = pst_tomorrow - timedelta(days=days + 1)

        transactions = models.Transaction.objects.filter(timestamp__gte=days_ago,
                                                         timestamp__lt=pst_tomorrow).order_by('timestamp')
        init = models.Transaction.objects.filter(timestamp__lt=days_ago).aggregate(balance=Sum('value'))

        context_dict = {'transactions': transactions,
                        'init': init.get('balance', 0)}

        return render(request, self.template_name, context_dict)


@method_decorator(login_required, name='dispatch')
class PettyCashCreateView(TemplateView):
    template_name = 'petty_cash/create.html'

    def get(self, request):
        form = forms.TransactionForm()
        context_dict = {'form': form}

        return render(request, self.template_name, context_dict)

    def post(self, request):
        form = forms.TransactionForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            msg = 'Successfully created new Petty Cash Transaction: {0}'.format(str(instance))
            messages.success(request, msg)

            return redirect(reverse('pettycash_list'))

        else:
            context_dict = {'form': form}
            return render(request, self.template_name, context_dict)
