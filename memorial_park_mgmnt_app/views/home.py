from datetime import datetime, timedelta

from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django_datatables_view.base_datatable_view import BaseDatatableView

from memorial_park_mgmnt_app import models, forms
from utils import utils


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class HomeView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request):
        branch_id = request.session.get('branch_id')
        pst = datetime.utcnow() + timedelta(hours=8)
        five_days = pst + timedelta(days=5)

        # Due for the next 5 days
        # bills = models.Bill.objects.filter(contract__lot__branch__id=branch_id,
        #                                    due_date__gte=pst.date(),
        #                                    due_date__lte=five_days.date()).order_by('due_date')

        overdues = models.Bill.objects.filter(contract__lot__branch__id=branch_id,
                                              status='OVERDUE').order_by('due_date')

        context_dict = {
            'bills': [],
            'overdues': overdues
        }

        return render(request, self.template_name, context_dict)


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class DueBillsView(TemplateView):
    template_name = 'home/due_bills.html'

    def get(self, request):
        branch_id = request.session.get('branch_id')
        pst = datetime.utcnow() + timedelta(hours=8)
        five_days = pst + timedelta(days=5)

        # Due for the next 5 days
        bill_list = models.Bill.objects.filter(contract__lot__branch__id=branch_id,
                                               due_date__gte=pst.date(),
                                               due_date__lte=five_days.date()).order_by('due_date')
        page = request.GET.get('page', 1)

        paginator = Paginator(bill_list, 25)
        try:
            bills = paginator.page(page)
        except PageNotAnInteger:
            bills = paginator.page(1)
        except EmptyPage:
            bills = paginator.page(paginator.num_pages)

        context_dict = {'bills': bills}

        return render(request, self.template_name, context_dict)


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class CommisionRecentView(TemplateView):
    template_name = 'home/recent_commissions.html'

    def get(self, request):
        branch_id = request.session.get('branch_id')

        commission_list = models.Commission.objects.filter(bill__contract__lot__branch__id=branch_id).order_by('-created')[:100]
        page = request.GET.get('page', 1)

        paginator = Paginator(commission_list, 25)
        try:
            commissions = paginator.page(page)
        except PageNotAnInteger:
            commissions = paginator.page(1)
        except EmptyPage:
            commissions = paginator.page(paginator.num_pages)

        context_dict = {'commissions': commissions}

        return render(request, self.template_name, context_dict)

    def post(self, request):
        branch_id = request.session.get('branch_id')
        release_commission = request.POST.getlist('release-commission')

        pst = datetime.utcnow() + timedelta(hours=8)
        commissions = models.Commission.objects.filter(pk__in=release_commission, bill__contract__lot__branch__id=branch_id)
        commissions.update(release_date=pst.date())

        commission_list = models.Commission.objects.filter(Q(bill__contract__lot__branch__id=branch_id) |
                                                           Q(pk__in=release_commission))
        commission_list = commission_list.order_by('-created')[:100]
        page = request.GET.get('page', 1)

        paginator = Paginator(commission_list, 25)
        try:
            commissions = paginator.page(page)
        except PageNotAnInteger:
            commissions = paginator.page(1)
        except EmptyPage:
            commissions = paginator.page(paginator.num_pages)

        context_dict = {'commissions': commissions}

        return render(request, self.template_name, context_dict)
