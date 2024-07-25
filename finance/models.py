from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random
from global_views.global_views import GlobalView
from sysadmin.models import Employee, Business, Station


GENDER_CHOICES = (("Male",'Male'), ("Female",'Female'))
MARITAL_STATUS = (("Married",'Married'), ("Not Married",'Not Married'))
GLOBAL_DEFS = GlobalView()

today = datetime.today() 
YEAR = str(today.year)
MONTH  = str(today.month)
DAY = str(today.day)





class MoneySource(models.Model):
    settings_name = models.CharField(max_length=20,)
    money_source_name = models.CharField(max_length=20)

    def __str__(self):
      return self.money_source_name




class PaymentMethod(models.Model):
    settings_name = models.CharField(max_length=20,)
    pay_method_name = models.CharField(max_length=20)
    class Meta:
       indexes = [ 
         models.Index(fields=["settings_name",]),
       ]
    def __str__(self):
      return self.pay_method_name


      
class ItemType(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(Station, on_delete = models.CASCADE, null=True, blank=True)
    item_type_name = models.CharField(max_length =80,)
    settings_name = models.CharField(max_length =80, null=True, blank=True)
    is_income = models.BooleanField()
    
    class Meta:
       indexes = [ 
         models.Index(fields=["is_income",]),
         models.Index(fields=["settings_name",]),
         ]
    def __str__(self):
        return self.item_type_name

    class Meta:
           indexes = [ 
             models.Index(fields=["item_type_name",]),
           ]




class ItemCategory(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(Station, on_delete = models.CASCADE, null=True, blank=True)
    settings_name= models.CharField(max_length =80,  null=True, blank=True)
    category_name = models.CharField(max_length =80, null=True, blank=True)

    def __str__(self):
        return self.category_name
    
    class Meta:
           indexes = [ 
             models.Index(fields=["settings_name",]),
             models.Index(fields=["category_name",]),
           ]




class Item(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(Station, on_delete = models.CASCADE, null=True, blank=True)
    item_typeID = models.ForeignKey(ItemType, on_delete = models.CASCADE)
    item_categoryID = models.ForeignKey(ItemCategory, on_delete = models.CASCADE, null=True, blank=True)
    settings_name = models.CharField(max_length =50, null=True, blank=True)
    item_name = models.CharField(max_length =80, null=True, blank=True)
    unit_cost = models.FloatField(default=0, null=True, blank=True)
    unit_price = models.FloatField(default=0, null=True, blank=True)
    unit_measure = models.CharField(max_length=20, default="", null=True, blank=True)
    is_income = models.BooleanField()
    is_school_fees = models.BooleanField(default=False, null=True, blank=True)
    is_monetary = models.BooleanField(default=False, null=True, blank=True)
    is_requirement = models.BooleanField(default=False, null=True, blank=True)
    #is_monetary = 
    
     
    class Meta:
       indexes = [ 
         models.Index(fields=["is_income",]),
         models.Index(fields=["item_name",]),
         models.Index(fields=["settings_name",]),
         models.Index(fields=["is_monetary",]),
         models.Index(fields=["is_school_fees",]),
         models.Index(fields=["is_requirement",]),
         ]
    
    def __str__(self):
        return str(self.item_typeID) +": "+str(self.item_name)



class PersonTypes(models.Model):
    settings_name = models.CharField(max_length=50)
    person_type_name = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.person_type_name)



  
class ClientType(models.Model):
    settings_name = models.CharField(max_length=50)
    client_type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.student_type_name
    class Meta:
       indexes = [ 
         models.Index(fields=["settings_name",]),       
       ]
    

class Client(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(Station, on_delete = models.CASCADE, null=True, blank=True)
    client_typeID = models.ForeignKey(ClientType, on_delete = models.CASCADE, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    firstname = models.CharField(max_length=50, null=True, blank=True, default="")
    othernames = models.CharField(max_length=50, null=True, blank=True, default="")
    fullname = models.CharField(max_length=80, null=True, blank=True, default="")
    initials = models.CharField(max_length = 10, null=True, blank=True)
    NIN = models.CharField(max_length=50, null=True, blank=True)
    client_NO = models.CharField(max_length=50, null=True, blank=True, unique=True)

    date_of_birth = models.DateField(null=True, blank=True)
    
    user_fullname = models.CharField(max_length=80, null=True, blank=True)
    gender = models.CharField(max_length=7, null=True, blank=True, choices = GENDER_CHOICES)
    contacts = models.CharField(max_length=50, null=True, blank=True)
    marital_status = models.CharField(max_length=15, null=True, blank=True, choices = MARITAL_STATUS)  
    client_image = models.ImageField(null=True, blank=True, upload_to ="CLIENTS/"+YEAR+"/"+MONTH+"/"+DAY)

    #Address details
    address = models.CharField(max_length = 80, null=True, blank=True)
    email_address = models.CharField(max_length = 30, null=True, blank=True)
    cell = models.CharField(max_length = 50, null=True, blank=True)
    village = models.CharField(max_length = 50, null=True, blank=True)
    parish = models.CharField(max_length = 50, null=True, blank=True)
    ward = models.CharField(max_length = 50, null=True, blank=True)
    subcounty = models.CharField(max_length = 50, null=True, blank=True)
    division = models.CharField(max_length = 50, null=True, blank=True)
    county = models.CharField(max_length = 50, null=True, blank=True)
    municipality = models.CharField(max_length = 50, null=True, blank=True)
    district = models.CharField(max_length = 50, null=True, blank=True)

    #Banking and occuptaion
    occupation = models.CharField(max_length=80, blank=True, null=True) 
    bank_name = models.CharField(max_length=60, null=True, blank=True)
    branch = models.CharField(max_length=60, null=True, blank=True)
    accountNo = models.CharField(max_length=40, null=True, blank=True)
    ATM_NO = models.CharField(max_length=40, null=True, blank=True)
    ATM_PIN = models.CharField(max_length=5, null=True, blank=True)
    
    #business and occupation
    business_name = models.CharField(max_length=80, blank=True, null=True)
    employer = models.CharField(max_length=80, blank=True, null=True)
    employer_address = models.CharField(max_length=80, blank=True, null=True)


    #speed optimization
    search_string = models.CharField(max_length=120, null=True, blank=True) 
    original_balance = models.FloatField(default=0, null=True, blank=True)
    amount_paid  = models.FloatField(default=0, null=True, blank=True)
    balance  = models.FloatField(default=0, null=True, blank=True)
    client_user_accountID = models.IntegerField(null=True, blank=True, default=0)
    deleted = models.BooleanField(null=True, blank=True, default=False)
    userID = models.ForeignKey(User, null=True, blank=True,  on_delete = models.CASCADE)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return str(self.id)+": "+str(self.surname)+" "+str(self.firstname)+" "+str(self.othernames)


    class Meta:
       indexes = [ 
        models.Index(fields=["search_string",]), 
        models.Index(fields=["client_NO",]), 
        models.Index(fields=["record_date",]),  
        models.Index(fields=["client_user_accountID",]), 
        models.Index(fields=["NIN",]),
       ]
    
    
    def save(self, *args,**kwargs): 
        self.initials = str(self.surname)[0] or "" +str(self.firstname)[0] or ""+ str(self.othernames)[0] or ""       
        self.fullname = str(self.surname)+" "+str(self.firstname)+" "+str(self.othernames)
        self.search_string = str(self.id)+" "+str(self.client_NO)+"-"+str(self.surname)+" "+str(self.firstname)+" "+str(self.othernames)+" "+str(self.NIN)+" "+str(self.contacts)
        
        loop_it = True

        if self.client_NO is None or self.client_NO =="":
          while loop_it:
            today = datetime.today()
            year = str(today.year)[-2]+str(today.year)[-1]
            month = str(today.month) if len(str(today.month))>2 else "0"+str(today.month)
            numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
            no = str(random.choice(numbers)) + str(random.choice(numbers)) + \
                str(random.choice(numbers)) + str(random.choice(numbers))

            client_NO =  year+month+"/"+no

            if Client.objects.filter(client_NO = client_NO).exists():
              pass
            else:
              self.client_NO = client_NO
              loop_it = False

            self.address = self.address.upper() if self.address else  ""
            self.firstname = self.firstname.upper() if self.firstname else  ""
            self.surname = self.surname.upper() if self.surname else ""
            self.othernames = self.othernames.upper() if self.othernames else ""
        
        super(Client, self).save(*args, **kwargs)




class ClientNextOKin(models.Model):
    #Next of Kin info
    clientID = models.ForeignKey(Client, on_delete = models.CASCADE, null=True, blank=True)
    next_of_kin_full_name =models.CharField(max_length=80, blank=True, null=True) 
    next_of_kin_contacts =models.CharField(max_length=50, blank=True, null=True) 
    next_of_kin_address =models.CharField(max_length=80, blank=True, null=True)
    next_of_kin_relation =  models.CharField(max_length=80, blank=True, null=True)  
    next_of_kin_image = models.ImageField(null=True, blank=True, upload_to = "NEXTOFKIN/"+YEAR+"/"+MONTH+"/"+DAY)





class CashBook(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(Station, on_delete = models.CASCADE, null=True, blank=True)
    item_typeID = models.ForeignKey(ItemType, on_delete = models.CASCADE, null=True, blank=True)
    item_categoryID = models.ForeignKey(ItemCategory, on_delete = models.CASCADE, null=True, blank=True)
    money_sourceID = models.ForeignKey(MoneySource, on_delete = models.CASCADE, null=True, blank=True)
    pay_methodID = models.ForeignKey(PaymentMethod, on_delete = models.CASCADE, null=True, blank=True)
    person_typeID = models.ForeignKey(PersonTypes, on_delete = models.CASCADE, null=True, blank=True)
    pseronID = models.IntegerField(default=0, null=True, blank=True)
    
    itemID = models.ForeignKey(Item, on_delete = models.CASCADE, null=True, blank=True)
    particulars = models.CharField(max_length=80, default="", null=True, blank=True) #index
    item_name = models.CharField(max_length=80, null=True, blank=True)
    payID_NO = models.CharField(max_length = 40, null=True, blank=True)
    is_income = models.BooleanField(default=True, null=True, blank=True)
    unit_cost = models.FloatField(default=0, null=True, blank=True)
    unit_price = models.FloatField(default=0, null=True, blank=True)

    quantity = models.FloatField(default=0, null=True, blank=True) #2.5
    income_received = models.FloatField(default=0, null=True, blank=True)
    expense_made = models.FloatField(default=0, null=True, blank=True)
    net = models.FloatField(default=0, null=True, blank=True)
    net_str = models.CharField(max_length=30, null=True, blank=True)

    userID = models.ForeignKey(User, on_delete = models.CASCADE, null=True, blank=True)
    user_fullname = models.CharField(max_length=80, null=True, blank=True)
    record_date = models.DateTimeField(auto_now_add = True, null=True, blank=True)
    refund_date = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True) #same as refund

    #color code=red indicated refunded
    color_code = models.CharField(max_length=10, null=True, blank=True, default="transparent") 
    running_total = models.FloatField(default=0, null=True, blank=True)
    running_total_str = models.CharField(max_length=30, null=True, blank=True)


    def __str__(self):
        return str(self.record_date)+": "+str(self.item_name)

    class Meta:
       indexes = [ 
         models.Index(fields=["is_income",]),
         models.Index(fields=["record_date",]),
         models.Index(fields=["refund_date",]),
         models.Index(fields=["is_deleted",]),
         models.Index(fields=["pseronID",]),
         ]





class RefundedItens(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(Station, on_delete = models.CASCADE, null=True, blank=True)
    cashbookID = models.ForeignKey(CashBook, on_delete = models.CASCADE,  null=True, blank=True)
    itemID = models.ForeignKey(Item, on_delete = models.CASCADE, null=True, blank=True)
    particulars = models.CharField(max_length=80, default="", null=True, blank=True) #index
    item_name = models.CharField(max_length=80, null=True, blank=True)
    amount_refunded = models.FloatField(default=0, null=True, blank = True)
    userID = models.ForeignKey(User, on_delete = models.CASCADE)
    user_fullname = models.CharField(max_length=80)
    record_date = models.DateTimeField(auto_now_add = True)





