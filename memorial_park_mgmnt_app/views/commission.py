from datetime import datetime, timedelta

from django.views.generic import TemplateView
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.db.models import Q
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator

from django_datatables_view.base_datatable_view import BaseDatatableView

from memorial_park_mgmnt_app import models, forms
from utils import utils


@method_decorator(utils.branch_required(utils.is_auth_and_has_branch), name='dispatch')
class CommissionReadView(TemplateView):
    template_name = 'commission/read.html'

    def get(self, request, commission_id):
        commission = get_object_or_404(models.Commission, pk=commission_id)
        branch_id = request.session.get('branch_id')
        if commission.bill.contract.lot.branch.id != branch_id:
            return HttpResponseForbidden()

        context_dict = {
            'commission': commission
        }

        return render(request, self.template_name, context_dict)
