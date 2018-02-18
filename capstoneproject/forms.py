from django import forms

class LogInForm(forms.Form):
    username = forms.CharField(label='Username',
                               max_length=20,
                               widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter username'}))
    password = forms.CharField(label='Password',
                               max_length=20,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'}))

class NewUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
    confirm_password = forms.CharField()