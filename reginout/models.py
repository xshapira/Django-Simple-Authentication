from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django_countries.fields import CountryField
from django_countries import countries

# Custom Manager
class MyAccountManager(BaseUserManager):
  def create_user(self, email, username, password=None, country=None):
    if not email:
      raise ValueError("Users Must have Email")
    if not username:
      raise ValueError("Users Must have Username")

    user = self.model(email=self.normalize_email(email),username=username,country=country)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self,email,username,password):
    user = self.create_user(email=self.normalize_email(email), username=username, password=password)
    user.is_admin = True
    user.is_staff = True
    user.is_superuser = True
    user.save(using=self._db)
    return user

# Custom User Model with extra Country, is_banned field, is_verified field
class Account(AbstractBaseUser):
  email = models.EmailField(verbose_name="email", max_length=60,unique=True)
  username = models.CharField(max_length=30,unique=True)
  date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
  last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=True)
  is_staff = models.BooleanField(default=False)
  is_superuser = models.BooleanField(default=False)
  is_banned = models.BooleanField(default=False)      # You can make user's is_banned True and redirect easily with a simple decorator on decorators.py
  is_verified = models.BooleanField(default=False)    # is_verified gets True when user click's the confirmation mail 
  country = CountryField()                            # You can ask user's country when they are register

  USERNAME_FIELD = "username"                         # username --> login with username // email --> login with email
  REQUIRED_FIELDS = ["email"]                         # if username_field = username --> that must be email and vice versa

  objects = MyAccountManager()

  def __str__(self):
      return self.username

  def has_perm(self,perm,obj=None):
    return self.is_admin
  
  def has_module_perms(self,app_label):
    return True


# Simple Post Model For Testing
class Post(models.Model):
  author = models.ForeignKey(Account, on_delete=models.CASCADE)
  title = models.CharField(max_length=150)

  def __str__(self):
      return self.title