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
from django.db.models import Sum
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.
def send_transaction_email(user,amount,subject,template):
    message=render_to_string(template,{
        'user':user,
        'amount':amount
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()
    # mail_subject='Deposit Message'
        # message=render_to_string('transactions/deposit_mail.html',{
        #     'user':self.request.user,
        #     'amount':amount
        # })
        # to_email=self.request.user.email
        # send_email = EmailMultiAlternatives(mail_subject, '', to=[to_email])
        # send_email.attach_alternative(message,"text/html")
        # send_email.send()
        
class TransactionViewMixin(LoginRequiredMixin,CreateView):
    model=Transaction
    template_name = 'transaction/transaction.html'
    success_url=reverse_lazy('profile')
    title=''

    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs.update({
            'customer' : self.request.user.customer
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
        amount=form.cleaned_data.get('amount')
        customer=self.request.user.customer
        customer.balance += amount
        customer.save(
            update_fields=['balance']
        )
        messages.success(self.request,
                        f'{"{:,.2f}".format(float(amount))}$ has ben successfully Deposit')
        send_transaction_email(
            self.request.user, amount, 'Deposit Message', 'transaction/deposit_mail.html')
        return super().form_valid(form)

class BorrowBookView(TransactionViewMixin):
    form_class=BorrowForm
    title='Borrow Book'

    def get_initial(self):
        id = self.kwargs['id']
        book = Book.objects.get(pk=id)
        initial = {'transaction_type': BORROW, 'amount': book.borrowing_price, 'book': book}
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
        send_transaction_email(
            self.request.user, amount, 'Borrow Message', 'transaction/borrow_mail.html')
        return super().form_valid(form)

class ReturnBookView(LoginRequiredMixin,View):
    
    def get(self,request,id):
        return_book=get_object_or_404(Transaction,pk=id)
        return_book.transaction_type=RETURN
        customer=self.request.user.customer
        amount = return_book.amount
        customer.balance += return_book.amount
        customer.save()
        return_book.save()

        messages.success(self.request,
                        f'Thank you for returning The book {return_book.book.title}.You will be refund ${return_book.book.borrowing_price}')
        send_transaction_email(
            self.request.user, amount, 'Borrow Message', 'transaction/borrow_mail.html')
        return redirect('profile')
    

