from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from django_countries import countries

User = get_user_model()

# Resend Activation Mail
class ResendForm(forms.Form):
  email = forms.EmailField()
  # Find the user and check the mail if its mail already verified raise error
  def clean_email(self):
    email = self.cleaned_data.get("email")
    user = User.objects.get(email=email)
    if user.is_verified:
      raise forms.ValidationError("Email already Activated")
    return email


class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField(widget=forms.PasswordInput)

  # checks username exits 
  def clean_username(self):
    username = self.cleaned_data.get("username")
    password = self.cleaned_data.get("password")
    qs = User.objects.filter(username__iexact=username)  
    if not qs.exists():
      raise forms.ValidationError("This is invalid User")
    return username

  # Check For username's password is right
  def clean_password(self):
    username = self.cleaned_data.get("username")
    password = self.cleaned_data.get("password")
    if not authenticate(username=username,password=password):
      raise forms.ValidationError("incorrect password")
    return password


non_allowed_usernames = ["admin","staff","famousperson","etc"]
class RegisterForm(forms.Form):
  username = forms.CharField()
  email = forms.EmailField()
  password1 = forms.CharField(label="Password",widget=forms.PasswordInput)
  password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput)
  country = forms.ChoiceField(choices=countries)

  # if username already exists or if user chooses a username that we define before raise error
  def clean_username(self):
    username = self.cleaned_data.get("username")
    qs = User.objects.filter(username__iexact=username)
    if username in non_allowed_usernames:
      raise forms.ValidationError("You cant choose that username")
    if qs.exists():
      raise forms.ValidationError("Username already Exists")
    return username

  # if the email that user enter is already in database raise error
  def clean_email(self):
    email = self.cleaned_data.get("email")
    qs = User.objects.filter(email__iexact=email)
    if qs.exists():
      raise forms.ValidationError("Email already Exists")
    return email
