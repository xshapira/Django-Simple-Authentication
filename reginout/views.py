from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.urls import reverse_lazy
from django.views.generic import ListView,View
from time import sleep

from .forms import *
from .tokens import account_activation_token
from .models import *
from .decorators import *


Account = get_user_model()

# Home view 
def HomeViewFBV(request):
  return render(request, "index.html")

# Guests Only Can View Pages
class GuestView(View):
  def dispatch(self, request, *args, **kwargs):
    if self.request.user.is_authenticated:
      return redirect("posts")
    return super(GuestView,self).dispatch(request, *args, **kwargs)

# Members only pages 
class MemberView(View):
  def dispatch(self, request, *args, **kwargs):
    return (super(MemberView, self).dispatch(request, *args, **kwargs)
            if self.request.user.is_authenticated else redirect("login"))

# Redirect users to banned Page
class BannedView(View):
  def dispatch(self, request, *args, **kwargs):
    if self.request.user.is_banned:
      return redirect("home")
    return super(BannedView,self).dispatch(request, *args, **kwargs)

# Views

# Simple Post Listing View
class PostListView(MemberView,ListView):
  model = Post
  template_name = "posts.html"
  context_object_name = "posts"
  

@login_excluded("posts")
def login_view(request):
  form = LoginForm(request.POST or None)
  if form.is_valid():
    username = form.cleaned_data.get("username") 
    password = form.cleaned_data.get("password") 
    user = authenticate(request, username=username, password=password)
    # if user is banned = True then show banned message or redirect to another page 
    # banned user wont be logged in and cant reach posts page
    if user and user.is_banned:
      return HttpResponse("You have been banned")
    # User is Valid And Active
    elif user != None:
      login(request,user)
      return redirect("posts")  
  return render(request, "login.html",{"form":form})
  

@login_excluded("posts")
def register_view(request):
  form = RegisterForm(request.POST or None)
  if form.is_valid():
    username = form.cleaned_data.get("username") 
    email = form.cleaned_data.get("email") 
    password = form.cleaned_data.get("password1") 
    password2 = form.cleaned_data.get("password2") 
    country = form.cleaned_data.get("country") 
    try:
      user = Account.objects.create_user(email,username,password,country)
    except:
      user = None
    if Account.objects.filter(email__iexact=email).count() == 1:
      current_site = get_current_site(request)
      mail_subject = 'Activate your account.'
      message = render_to_string('email_template.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
      to_email = form.cleaned_data.get('email')
      send_mail(mail_subject, message, 'fethido@gmail.com', [to_email])
      return HttpResponse('Please confirm your email address to complete the registration')
  return render(request, "login.html",{"form":form})



# Resend Activation mail if user didnt get the mail
@members_allowed("home") 
def resendemail(request):
  # initial gets the non verified user's mail and auto fills the form
  form = ResendForm(request.POST or None, initial={"email":request.user.email})
  if form.is_valid(): 
    email = form.cleaned_data.get("email")
    user = Account.objects.get(email=email) 
    if Account.objects.filter(email__iexact=email).count() == 1:
      current_site = get_current_site(request)
      mail_subject = 'Activate your account.'
      message = render_to_string('email_template.html', {
                            'user': user,
                            'domain': current_site.domain,
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'token': account_activation_token.make_token(user),
                        })
      to_email = form.cleaned_data.get('email')
      send_mail(mail_subject, message, 'fethido@gmail.com', [to_email])
      return HttpResponse('Please confirm your email address to complete the registration')
  return render(request, "resend.html",{"form":form})


# make users is_verified True 
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verified = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class PasswordChange(MemberView,SuccessMessageMixin,PasswordChangeView):
  model = User
  form_class = PasswordChangeForm
  template_name = "passwordchange.html"
  success_message = "Password Changed Successfully You will be redirected in 1 second"
  success_url = reverse_lazy("password_change_done")
  

class PasswordDone(PasswordChangeDoneView):
  template_name = "password_change_done.html"

  def dispatch(self, request, *args, **kwargs):
    if self.request.user.is_authenticated:
      sleep(1)
      return redirect("posts")
    return super(PasswordDone,self).dispatch(request, *args, **kwargs)
  

