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
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout, update_session_auth_hash
from django.db.models import Sum
# Create your views here.

class UserRegistrationView(FormView):
    template_name='customer/register.html'
    success_url=reverse_lazy('login')
    form_class=UserRegistrationForm

    def form_valid(self,form):
        user=form.save()
        login(self.request,user)
        messages.success(self.request,"Welcome! You have registered Successfully")
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name='customer/login.html'

    def get_success_url(self):
        messages.success(self.request, "You are Successfully logged in ")
        return reverse_lazy('login')

class UserProfileView(LoginRequiredMixin, View):
    template_name = "customer/profile.html"

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        borrows = Transaction.objects.filter(
            transaction_type=BORROW, customer=self.request.user.customer)
        total_borrowing_price = borrows.aggregate(
            total_price=Sum('amount')
        )['total_price'] or 0

        return render(request, self.template_name, {"form": form, "borrows": borrows, "total_borrowing_price": total_borrowing_price})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(self.request, "Profile updated Successfully")
            return redirect("profile")
        return render(request, self.template_name, {"form": form})


class ProfileUpdateView(View):
    template_name = 'customer/edit_profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


def change_pass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed Successfully')
            update_session_auth_hash(request, form.user)
            
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'customer/change_pass.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request,"Logout successfully")
    return redirect('login')