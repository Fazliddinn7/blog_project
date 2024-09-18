from django import forms
from django.contrib.auth.forms import UserCreationForm, BaseUserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=250)
    password = forms.CharField(widget=forms.PasswordInput)


# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(max_length=250, label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(max_length=250, label='Confirm password', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = 'username', 'email', 'first_name'
#
#     def clean_password2(self):
#         if self.cleaned_data['password'] != self.cleaned_data['password2']:
#             raise forms.ValidationError('Ikkita parol bir-biriga teng bo\'lishi kk')
#         return self.cleaned_data['password2']


class UserRegistrationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = 'username', 'email', 'first_name'
