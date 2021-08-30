from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify # new
from Util.utils import rand_slug
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserAccountManager(BaseUserManager):

    def create_user(self, email, username, full_name, gender, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not username:
            raise ValueError(_('Users must have a username'))
        if not full_name:
            raise ValueError(_('Users must provide their full name'))
        if not gender:
            raise ValueError(_('Users must provide their gender'))
        if not phone_number:
            raise ValueError(_('Users must provide their phone number'))

        # phone_number.setdefault('is_staff', True)
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
            gender=gender,
            phone_number=phone_number,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, full_name, gender, phone_number,
                         password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            full_name=full_name,
            gender=gender,
            phone_number=phone_number,
            password=password

        )
        # user.set_password(password)
        user.admin = True
        user.staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    from Util.ListsOfData import  WORKING_FILED
    from Util.ListsOfData import GENDER_CHOICES
    # from django.core.validators import RegexValidator
    # phone_regex = RegexValidator(regex=r'^9\d{8}$|^1\d{8}$',
    #                              message=_("Phone number must start with 9 or 1 (no zeros) and includes 9 numbers."))
    username = models.CharField(
        verbose_name=_('User Name'),
        blank=False,
        null=False,
        max_length=350,
        unique=True

    )
    full_name = models.CharField(
        verbose_name=_('Full Name'),
        max_length=350,
        blank=False,
        null=False
    )
    organization = models.CharField(
        verbose_name=_('Organization'),
        max_length=350,
        blank=False,
        null=False
    )
    phone_number = models.CharField(
        verbose_name=_('Phone Number'),
        blank=False,
        null=False,
        max_length=100,
        unique=True
    )

    email = models.EmailField(
        verbose_name=_('Email Address'),
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)
    slug = models.SlugField(
        default=slugify(rand_slug()),
        verbose_name=_('User Slug')

    )
    registration_datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(rand_slug() + "-" + str(self.username))
        return super().save(*args, **kwargs)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['password', 'full_name',
                       'username']  # Email & Password are required by default.
    objects = UserAccountManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):
        return self.full_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # return self.user_role == 3
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        # return self.user_role == 1
        return self.admin




class ContactUs(models.Model):
    from django.core.validators import RegexValidator
    phone_regex = RegexValidator(regex=r'^9\d{8}$|^1\d{8}$',
                                 message=_("Phone number must start with 9 or 1 (no zeros) and includes 9 numbers."))

    phone_number = models.CharField(
        verbose_name=_('Phone Number'),
        blank=False,
        null=False,
        max_length=100,
        unique=True
    )
    marketing_executive_phone_number = models.CharField(
        verbose_name=_('Marketing Executive Phone Number'),
        blank=False,
        null=False,
        max_length=100,
        unique=True
    )

    email = models.EmailField(
        verbose_name=_('Email Address'),
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        max_length=150,
        verbose_name=_('Name')
    )
    address = models.CharField(
        max_length=250,
        verbose_name=_('Address')
    )
    message = models.TextField(
        verbose_name=_('Message'),
    )
    website = models.URLField(
        verbose_name=_('Website')
    )
    facebook = models.URLField(
        verbose_name=_('Facebook')
    )
    twitter = models.URLField(
        verbose_name=_('Twitter')
    )
    linkedin = models.URLField(
        verbose_name=_('LinkedIn')
    )
    instagram = models.URLField(
        verbose_name=_('Instagram')
    )

    def __str__(self):
        return self.email



