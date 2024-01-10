from django import forms
from .models import Review
from .constants import RATING

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=RATING)
    body=forms.CharField(widget=forms.Textarea(attrs={'rows':3}))
    

    class Meta:
        model=Review
        fields=['body', 'rating']
