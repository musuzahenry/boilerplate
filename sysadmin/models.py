from django.db import models
from django.contrib.auth.models import User
import random
from datetime import datetime
import os
#constants here
GENDER_CHOICES = (("Male",'Male'), ("Female",'Female'))




def upload_to_function(instance, filename):
    # Access model fields or other data from the instance
    model_name = instance.__class__.__name__.lower()  # Get model name

     #store student images
    today = datetime.today()
    year = str(today.year)[-2]+str(today.year)[-1]
    day = str(today.day)
    hour = str(datetime.now().hour)
    month = str(today.month) if len(str(today.month))>2 else "0"+str(today.month)
    location_str = year+month+day+hour

    return f'employeeimages/{location_str}/{filename}'  # Return the desired upload path




def upload_to_function_docs(instance, filename):
    # Access model fields or other data from the instance
    model_name = instance.__class__.__name__.lower()  # Get model name

     #store student images
     #store student images
    today = datetime.today()
    year = str(today.year)[-2]+str(today.year)[-1]
    day = str(today.day)
    hour = str(datetime.now().hour)
    month = str(today.month) if len(str(today.month))>2 else "0"+str(today.month)
    location_str = year+month+day+hour

    location_str = year+month+day+hour

    return f'employeedocuments/{location_str}/{filename}'  # Return the desired upload path




class Business(models.Model):
    busniness_name = models.CharField(max_length=150)
    logo = models.ImageField(null=True, blank=True, upload_to ="logo")
    contact_numbers = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    motto = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=80, null=True, blank=True)
    custom_header = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.busniness_name
#================================================================================================



class Station(models.Model):
    station_name = models.CharField(max_length=150)
    logo = models.ImageField(null=True, blank=True, upload_to ="logo")
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    contact_numbers = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    motto = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    website = models.CharField(max_length=80, null=True, blank=True)
    custom_header = models.TextField(max_length=200, null=True, blank=True)
    map_text = models.TextField(max_length=250, null=True, blank=True)
    public_view_details = models.TextField(max_length=250, null=True, blank=True)
    
    def __str__(self):
        return self.station_name




class Position(models.Model):
    #these are Employee positions, just ias any business is
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(Station, on_delete = models.CASCADE, null=True, blank=True)
    settings_name = models.CharField(max_length = 80, null=True, blank=True)
    position_name = models.CharField(max_length=80, null=True, blank=True)
    mandatory = models.BooleanField(default=False, null=True, blank=True)
  
    def __str__(self):
        return self.position_name
    class Meta:
       indexes = [ 
         models.Index(fields=["settings_name",]),
       ]




class SystemSetings(models.Model):
  businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
  stationID = models.ForeignKey(Station, on_delete = models.CASCADE, null=True, blank=True)
  app_name = models.CharField(max_length=150, null=True, blank=True)
  app_logo = models.ImageField(upload_to ="app_logo", null=True, blank=True)
  app_footer = models.CharField(max_length=150, null=True, blank=True)
  app_other_info = models.CharField(max_length=150, null=True, blank=True)
  


class SystemGeneralSettings(models.Model):
  pass
  
class SystemRoles(models.Model):    
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(Station, on_delete = models.CASCADE, null=True, blank=True)
    role_name = models.CharField(max_length=80)
    #The module settings help is define the module where the user is redirected on login.
    #it is the url reverse for that users predefined  dashboard
    module_settings = models.CharField(max_length=50, null=True, blank=True)
    user_friendly_name = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False, null=True, blank=True)


    def __str__(self):
        return self.role_name
    
    class Meta:
       indexes = [ 
         models.Index(fields=["role_name",]),
         models.Index(fields=["module_settings",]),
         models.Index(fields=["deleted",]),
       ]




class Rights(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(Station, on_delete = models.CASCADE, null=True, blank=True)
    settings_name = models.CharField(max_length = 50, null=True, blank=True,)
    right_name = models.CharField(max_length = 80, null=True, blank=True)
    description = models.CharField(max_length = 120, null=True, blank=True)
    mandatory = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return self.right_name

    class Meta:
       indexes = [ 
         models.Index(fields=["settings_name",]),
         models.Index(fields=["mandatory",]),
       ]





class RoleRights(models.Model):  
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(Station, on_delete = models.CASCADE, null=True, blank=True)
    roleID = models.ForeignKey(SystemRoles, on_delete=models.CASCADE)
    rightID = models.ForeignKey(Rights, on_delete=models.CASCADE)
    #each mandatory role is a system role, i.e, inbuilt and cant be edited or deleted
    mandatory = models.BooleanField(default=False, null=True, blank=True) 

    def __str__(self):
      return str(self.roleID)+": "+str(self.rightID)
         
    class Meta:
       indexes = [ 
         models.Index(fields=["mandatory",]),
       ]




class Employee(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(Station, on_delete = models.CASCADE, null=True, blank=True)
    emp_no = models.CharField(max_length = 80, default="", blank=True, null=True)
    firstname = models.CharField(max_length = 80, default="")
    surname = models.CharField(max_length=80, default="")
    othername = models.CharField(max_length=80, default="", null=True, blank=True)
    fullname =  models.CharField(max_length=120, default="", null=True, blank=True)
    initials = models.CharField(max_length=50, null=True, blank=True, default="")
    employee_image = models.ImageField(null=True, blank=True, upload_to=upload_to_function)
    gender = models.CharField(max_length=7, choices = GENDER_CHOICES)
    date_of_birth = models.DateField()
    NIN = models.CharField(max_length=40, default="",  null=True, blank=True,)
    positionID  = models.ForeignKey(Position, on_delete = models.CASCADE, null=True, blank=True)
    system_roleID = models.ForeignKey(SystemRoles, on_delete = models.CASCADE, null=True, blank=True)
    is_system_user = models.BooleanField(default=False, null=True, blank=True)
    deleted = models.BooleanField(default=False, null=True, blank=True)
    date_of_hire = models.DateField(null=True, blank=True)
    employee_title = models.CharField(max_length=80, null=True, blank=True, default="")
    qualifications = models.CharField(max_length=80, null=True, blank=True, default="")
    academic_documents_upload = models.FileField(upload_to =upload_to_function_docs, blank=True, default="")
    NSSF_NO = models.CharField(max_length=80, null=True, blank=True, default="")
    phone_contacts = models.CharField(max_length=50, null=True, blank=True, default="")
    email_address = models.CharField(max_length=50, null=True, blank=True, default="")
    address = models.CharField(max_length=40, null=True, blank=True, default="")
    bank_name = models.CharField(max_length=80, null=True, blank=True, default="")
    bank_branch = models.CharField(max_length=80, null=True, blank=True, default="")
    bank_account_no = models.CharField(max_length=40, null=True, blank=True, default="")

    net_salary = models.FloatField(default=0, null=True, blank=True)
    nssf =   models.FloatField(default=0, null=True, blank=True)
    PAYE =   models.FloatField(default=0, null=True, blank=True)
    userID = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)

    next_of_kin_names = models.CharField(max_length=50, null=True, blank=True, default="")
    next_of_kin_contacts = models.CharField(max_length=50, null=True, blank=True, default="")
    next_of_kin_address = models.CharField(max_length=40, null=True, blank=True, default="")

    
    next_of_kin2_names = models.CharField(max_length=50, null=True, blank=True, default="")
    next_of_kin2_contacts = models.CharField(max_length=50, null=True, blank=True, default="")
    next_of_kin2_address = models.CharField(max_length=40, null=True, blank=True, default="")

    class Meta:
       indexes = [ 
         models.Index(fields=["is_system_user",]),
         models.Index(fields=["NIN",]),
         models.Index(fields=["NSSF_NO",]),
         models.Index(fields=["deleted",]),
       ]
    
    def __str__(self):
      return str(self.surname)+" "+ str(self.firstname)+" "+ str(self.othername)
    
    def save(self, *args,**kwargs): 
        self.initials = str(self.surname)[0] or "" +str(self.firstname)[0] or ""+ str(self.othername)[0] or ""       
        self.fullname = str(self.surname)+" "+ str(self.firstname)+" "+ (str(self.othername) if self.othername else "")

        loop_it = True

        if self.emp_no is None or self.emp_no =="":
          while loop_it:
            today = datetime.today()
            year = str(today.year)[-2]+str(today.year)[-1]
            month = str(today.month) if len(str(today.month))>2 else "0"+str(today.month)
            numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            no = str(random.choice(numbers)) + str(random.choice(numbers)) + \
                str(random.choice(numbers)) + str(random.choice(numbers))

            emp_no =  year+month+"/"+no

            if Employee.objects.filter(emp_no = emp_no).exists():
              pass
            else:
              self.emp_no = emp_no
              loop_it = False

            self.address = self.address.upper() if self.address else  ""
            self.firstname = self.firstname.upper() if self.firstname else  ""
            self.surname = self.surname.upper() if self.surname else ""
            self.othername = self.othername.upper() if self.othername else ""

        super(Employee, self).save(*args, **kwargs)


