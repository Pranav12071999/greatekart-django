from django import forms 
from .models import *
from django.core.exceptions import ValidationError

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    confirm_password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'phone_number']
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        # For single field
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your phone number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your Email'
        # This will apply 'form-control' class to all fields.
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean() # This will fetch the cleaned data dictionary. 
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError(
                "Password doesn't match with each other."
            )
