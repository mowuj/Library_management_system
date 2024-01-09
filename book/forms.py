from django import forms
from .models import Review
from .constants import RATING

class ReviewForm(forms.ModelForm):
    body=forms.CharField(widget=forms.Textarea)
    rating=forms.ChoiceField(choices=RATING)

    class Meta:
        model=Review
        fields=['body', 'rating']
