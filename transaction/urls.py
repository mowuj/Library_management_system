from django.urls import path
from .views import DepositView,BorrowBookView,ReturnBookView
urlpatterns = [
    path('deposit', DepositView.as_view(),name='deposit'),
    path('borrow/<int:id>/', BorrowBookView.as_view(),name='borrow'),
    path('return/<int:id>/', ReturnBookView.as_view(),name='return')
]
