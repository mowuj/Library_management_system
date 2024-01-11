from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=['amount','transaction_type',]
    
    def __init__(self, *args, **kwargs):
        self.customer = kwargs.pop('customer')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()
        

    def save(self, commit=True):
        self.instance.customer = self.customer
        self.instance.balance_after_transaction = self.customer.balance
        return super().save()


class DepositForm(TransactionForm):

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        min_deposit = 100

        if amount < min_deposit:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit}'
            )

        return amount


class BorrowForm(TransactionForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].disabled = True
        self.fields['amount'].widget = forms.HiddenInput()
    
    def get_initial(self):
        initial = super().get_initial()
        book = self.initial.get('book')  # Retrieve the book from initial data
        if book:
            initial['book'] = book
        return initial

    
    def save(self, commit=True):

        book = self.initial.get('book')

        self.instance.book = book
        
        return super().save(commit)



class ReturnForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        return amount
