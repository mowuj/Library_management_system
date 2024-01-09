from django.urls import path
from .views import BookDetailView
urlpatterns = [
    path('book<int:id>',BookDetailView.as_view(),name='book_detail')
]
