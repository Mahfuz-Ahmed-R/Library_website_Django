from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, ListView
from django.views.generic.edit import FormView
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserAccountModel
from .forms import UserForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from core.models import Borrow

class UserAccountView(FormView):
    # model = UserAccountModel
    form_class = UserForm
    template_name = 'account.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account created successfull!!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Account not created!!')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Register'
        return context
    
class UserLoginView(LoginView):
    template_name = 'account.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Logged in successfully!!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Login failed!!')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
    
class UserLogout(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, 'Logged out!!!')
        return redirect('homepage')

class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        borrowed_books = Borrow.objects.filter(user=user)
        account = UserAccountModel.objects.get(user=request.user)
        return render(request, 'profile.html', {'borrowed_books': borrowed_books, 'account': account})
    
class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Logged out!!!')
        return redirect('homepage')

class UserDetailsChange(LoginRequiredMixin, UpdateView):
    model = UserAccountModel
    form_class = UserChangeForm
    template_name = 'account.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!!!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Change Details'
        return context

class PasswordView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'account.html'

    def form_valid(self, form):
        messages.success(self.request, 'Password changed successfully!!!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Change Password'
        return context
    