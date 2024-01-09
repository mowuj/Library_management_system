from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from .models import Transaction
from .forms import DepositForm, BorrowForm
from .constants import DEPOSIT, RETURN, BORROW
from django.contrib import messages
from django.urls import reverse_lazy
from book.models import Book

# Create your views here.
class TransactionViewMixin(LoginRequiredMixin,CreateView):
    model=Transaction
    template_name=''
    success_url=reverse_lazy('profile')
    title=''

    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({
            'customer':self.request.user.customer
        })
        return kwargs
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            'title':self.title
        })
        return context

class DepositView(TransactionViewMixin):
    form_class=DepositForm
    title='Deposit'

    def get_initial(self):
        initial={'transaction_type':DEPOSIT}
        return initial
    
    def form_valid(self,form):
        amount=form.cleaned_data('amount')
        customer=self.request.user.customer
        customer.balance +=amount
        customer.save(
            update_fields=['balance']
        )
        messages.success(self.request,
                        f'{"{:,.2f}".format(float(amount))}$ has ben successfully Deposit')
        return super().form_valid(form)

class BorrowBookView(TransactionViewMixin):
    form_class=BorrowForm
    title='Borrow Book'

    def get_initial(self):
        id=self.kwargs['id']
        book=Book.objects.get(pk=id)
        initial = {'book':book,'transaction_type': BORROW,'amount':book.borrowing_price}
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        book = Book.objects.get(id=id)
        context.update({
            'book': book
        })
        return context

    def form_valid(self, form):
        id=self.kwargs['id']
        customer = self.request.user.customer
        book=Book.objects.get(id=id)
        amount=book.borrowing_price

        if customer.balance <amount:
            messages.error(self.request,f'Opps ! You don not have enough Balance.Please Deposit')
            return redirect('profile')

        customer.balance -= amount
        customer.save(
            update_fields=['balance']
        )
        messages.success(self.request,
                         f'Welcome! You has ben successfully Borrowed.Your current balance is ${customer.balance}')
        return super().form_valid(form)

class ReturnBookView(LoginRequiredMixin,View):
    
    def get(self,request,id):
        return_book=get_object_or_404(Transaction,pk=id)
        return_book.transaction_type=RETURN
        customer=self.request.user.customer
        customer.balance += return_book.amount
        customer.save()
        return_book.save()

        messages.success(self.request,
                        f'Thank you for returning The book {return_book.book.title}.You will be refund ${return_book.book.amount}')
        return redirect('profile')