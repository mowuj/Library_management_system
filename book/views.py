from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from .models import Book, Review
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ReviewForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from .models import Review
# Create your views here.

class BookDetailView(LoginRequiredMixin,DetailView):
    template_name='book/book_detail.html'
    model=Book
    pk_url_kwarg='id'
    context_object_name='book'

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        book = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.save()
            return self.get(request, *args, **kwargs)

    def form_valid(self, form):
        book = self.get_object()
        isAlreadyReviewed = Review.objects.filter(
            book=book, user=self.request.user).count()
        if isAlreadyReviewed >= 1:
            messages.info(self.request, "You have already reviewed this book.")
            return redirect("profile")
        else:
            new_review = form.save(commit=False)
            new_review.book = book
            new_review.save()
            messages.success(self.request, "Thanks for your valuable review")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        review = book.reviews.all()
        review_form = ReviewForm()

        context['review'] = review
        context['review_form'] = review_form
        return context
    
