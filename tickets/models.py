from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from mail_templated import send_mail

# Create your models here.
GENDER = (('M', _('Male')), ('F', _('Female')))


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, email and password.
        """
        if not email:raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser with the given email, username and password.
        """
        user = self.create_user(email, username, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    Extends the default User profiles of Django. The fields of this model can be obtained by the
    user.get_profile method and it's extended by the django-profile application.
    """
    user_id = models.AutoField(primary_key=True)
    user_first_name = models.CharField(_('First Name'), max_length=32, blank=True, null=True,
                                  validators=[RegexValidator(regex='^[A-Za-z]*$')])
    user_last_name = models.CharField(_('Last Name'), max_length=32, blank=True, null=True,
                                    validators=[RegexValidator(regex='^[A-Za-z]*$')])
    email = models.EmailField(_('Email'), db_index=True, unique=True)
    user_dob = models.DateField(_('Birth Date'), blank=True, null=True)
    user_gender = models.CharField(_('Gender'), max_length=1, choices=GENDER, blank=True, null=True)
    user_bio = models.CharField(_('Short Bio'), max_length=1000,blank=True )
    date_joined = models.DateTimeField(auto_now_add=True)
    username = models.CharField(_('username'), max_length=32, blank=False, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def get_name(self):
        if self.user_first_name and self.user_last_name:
            return (self.user_first_name +' '+ self.user_last_name )
        else:
            return self.username

    def get_first_name(self):
        return (self.user_first_name)

    def get_short_name(self):
        return self.username

    def get_email(self):
        return self.email

    def get_full_name(self):
        return self.username

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_user_id(self):
        return self.user_id

    @property
    def is_staff(self):
        return self.is_admin

    def __unicode__(self):
        return self.username


class Ticket(models.Model):
    """
    Ticket model
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(_('Your Name'), max_length=100, blank=False, unique=False)
    institution = models.CharField(_('Your Institution'), max_length=100, blank=False, unique=False)
    designation = models.CharField(_('Your Designation'), max_length=100, blank=False, unique=False)
    email = models.CharField(_('Your Email'), max_length=100, blank=False, unique=False)
    phone = models.CharField(_('Your Phone'), max_length=100, blank=False, unique=False)

    def __unicode__(self):
        return self.name


class Attendee(models.Model):
    ticket = models.ForeignKey(Ticket)
    name = models.CharField(_('Name'), max_length=100, blank=False, unique=False)
    email = models.CharField(_('Email'), max_length=100, blank=False, unique=False)


