from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

from .manager import UserManager

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    mobile_number = models.CharField(unique=True, max_length=10)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

class Employee(models.Model):
    employee_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(_('email address'), unique=True)
    department = models.CharField(max_length=50, null=False)
    designation = models.CharField(max_length=255, null=False)
    salary = models.FloatField(null=False)
    date_of_joining = models.DateField(blank=False)
