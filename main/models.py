

from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

GENDER_CHOICES = (("Male",'Male'), ("Female",'Female'))

#custom functions
#=======================================================
from django.conf import settings
import os


  

class Business(models.Model):
    busniness_name = models.CharField(max_length=150)
    logo = models.ImageField(null=True, blank=True, upload_to ="logo")
    contact_numbers = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    motto = models.CharField(max_length=100, null=True, blank=True) #sometimes called tagline
    email = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=80, null=True, blank=True)
    #the custom header and custom footer are rich text fields that help us richly define custom footers
    # and headers common to all reports in the system
    custom_header = models.CharField(max_length=200, null=True, blank=True)
    custom_footer = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.busniness_name
#================================================================================================



