from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', 'law_firm', 'preferred_arrest_location', 'city', 'password')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
