from django import forms
from .models import *
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ['subject','review','rating']