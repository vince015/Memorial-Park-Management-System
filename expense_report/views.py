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

from django_datatables_view.base_datatable_view import BaseDatatableView

from expense_report import models
from expense_report import forms


@method_decorator(login_required, name='dispatch')
class ExpenseListView(TemplateView):
    template_name = 'expense/list.html'

    def get(self, request):
        return render(request, self.template_name)

@method_decorator(login_required, name='dispatch')
class PettyCashView(TemplateView):
    template_name = 'expense/petty_cash.html'

    def __compute_petty_cash_monthly(self):
        pst = datetime.utcnow() + timedelta(hours=8)
        month_expenses = models.Expense.objects.filter(from_petty_cash=True,
                                                       date__month=pst.month)

        total = 0
        for expense in month_expenses:
            total = total + expense.amount

        return total

    def get(self, request):
        month_expense = self.__compute_petty_cash_monthly()
        context_dict = {
            'expense': month_expense,
            'percent': ((50000 - month_expense) / 50000) * 100,
            'remaining': 50000 - month_expense
        }
        return render(request, self.template_name, context_dict)


@method_decorator(login_required, name='dispatch')
class ExpenseJson(BaseDatatableView):
    model = models.Expense
    columns = ['date', 'payee', 'category', 'amount', 'from_petty_cash']
    order_columns = ['date', 'payee', 'category', 'amount', 'from_petty_cash']

    def get_initial_queryset(self):
        from_petty_cash = self.request.GET.get('petty_cash', 0)
        from_petty_cash = int(from_petty_cash)
        if from_petty_cash == 0:
            return models.Expense.objects.filter(from_petty_cash=False)
        else:
            return models.Expense.objects.filter(from_petty_cash=True)

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


from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta

def expense_report(request):

    if request.method == 'GET':
        ret = {
            'range': [],
            'vals': []
        }

        start = timezone.now()
        end = start - timedelta(days=30)
        print(0, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))

        for cnt in range(1, 12):
            start = end - timedelta(days=1)
            end = end - timedelta(days=30*cnt)
            print(cnt, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'))

        return JsonResponse(ret, safe=False)
