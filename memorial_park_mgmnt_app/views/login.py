from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect as django_redirect
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from memorial_park_mgmnt_app import models
from utils import utils


class LoginView(TemplateView):

    def get(self, request):
        template = 'login.html'
        redirect = request.GET.get('next', reverse('home'))
        context_dict = {'redirect_to': redirect}

        if request.user.is_authenticated:
            if hasattr(request.session, 'branch_id'):
                return django_redirect(redirect)
            else:
                return django_redirect(reverse('branch') + '?next=' + redirect)

        return render(request, template, context_dict)

    def post(self, request):
        template = 'login.html'
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:

                branches = utils.get_branches(user)
                if len(branches) > 1:
                    login(request, user)
                    request.session['branch_id'] = branches[0].id
                    request.session['branch_name'] = str(branches[0])
                    redirect = request.GET.get('next', reverse('home')) or reverse('home')
                    return django_redirect(reverse('branch') + '?next=' + redirect)
                elif len(branches) < 1:
                    msg = 'You are authenticated as {0} but this account does not belong to any branch. Kindly contact the site administrator.'.format(user.username)
                    messages.error(request, msg)
                    return render(request, template)
                else:
                    login(request, user)
                    request.session['branch_id'] = branches[0].id
                    request.session['branch_name'] = str(branches[0])
                    redirect = request.GET.get('next', reverse('home')) or reverse('home')
                    return django_redirect(redirect)

            else:
                msg = 'User is inactive.'
                messages.error(request, msg)
                return render(request, template_name)
        else:
            msg = 'Invalid username and/or password'
            messages.error(request, msg)
            return render(request, template)


@method_decorator(login_required, name='dispatch')
class LogoutView(TemplateView):

    def get(self, request):
        logout(request)
        return django_redirect(reverse('login'))


@method_decorator(login_required, name='dispatch')
class BranchView(TemplateView):
    template_name = 'branch.html'

    def get(self, request):
        redirect = request.GET.get('next', reverse('home'))
        branches = utils.get_branches(request.user)

        if len(branches) == 1:
            request.session['branch_id'] = branches[0].id
            request.session['branch_name'] = str(branches[0])
            return django_redirect(redirect)
        elif len(branches) < 1:
            msg = 'This account does not belong to any branch. Kindly contact the site administrator.'
            messages.error(request, msg)
            return django_redirect(reverse('logout'))

        context_dict = {'redirect_to': redirect,
                        'branches': branches}

        return render(request, self.template_name, context_dict)

    def post(self, request):
        branch_id = request.POST.get('branch_id')
        instance = models.Branch.objects.get(pk=branch_id)

        request.session['branch_id'] = instance.id
        request.session['branch_name'] = str(instance)

        redirect = request.GET.get('next', reverse('home'))
        return django_redirect(redirect)
