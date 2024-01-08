from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserUpdateForm
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import View
from transaction.models import Transaction
from transaction.constants import BORROW
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class UserRegistrationView(FormView):
    template_name='customer/register.html'
    success_url=reverse_lazy('login')
    form_class=UserRegistrationForm

    def form_valid(self,form):
        print('hey')
        user=form.save()
        login(self.request,user)
        messages.success(self.request,"Welcome! You have registered Successfully")
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name='customer/login.html'

    def get_success_url(self):
        messages.success(self.request, "You are Successfully logged in ")
        return reverse_lazy('login')

def user_logout(request):
    logout(request)
    messages.success(request,"Logout successfully")
    return redirect('login')