from django import forms
from .models import Review
from .constants import RATING

class ReviewForm(forms.ModelForm):
    body=forms.CharField(widget=forms.Textarea)
    rating=forms.ChoiceField(choices=RATING)

    class Meta:
        model=Review
        fields=['body', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['book'].disabled=True
        self.fields['book'].widget=forms.HiddenInput()