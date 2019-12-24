from django.contrib.auth.models import User
from django.contrib.auth import (
    login, logout)
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    View, ListView, DetailView, CreateView, FormView, UpdateView)
from .forms import AuthForm


class UserLogin(FormView):
    template_name = 'accounts/login.html'
    form_class = AuthForm

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.get_user()

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(self.get_success_url())
                else:
                    form.add_error('username', 'User is not active anymore.')
            else:
                form.add_error('username', 'Wrong username or password.')

        return render(request, self.template_name, {'form': form})
    
    def get_success_url(self):
        next_url = self.request.GET.get('next', None)
        if next_url:
            return f'{next_url}'
        else:
            return reverse('work:comp_list')


class UserLogout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('accounts:login'))
