from django.db import models
from django.contrib.auth.models import User
import datetime
from global_views.global_views import GlobalView
from sysadmin.models import Employee, Business, Station


GENDER_CHOICES = (("Male",'Male'), ("Female",'Female'))
GLOBAL_DEFS = GlobalView()





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
    item_name = models.CharField(max_length =80,)
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
         models.Index(fields=["is_monetary",]),
         models.Index(fields=["is_school_fees",]),
         models.Index(fields=["is_requirement",]),
         ]
    
    def __str__(self):
        return str(self.item_typeID) +" "+str(self.item_name)



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
    surname = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50, null=True, blank=True, default="")
    othernames = models.CharField(max_length=50, null=True, blank=True, default="")
    fullname = models.CharField(max_length=80, null=True, blank=True, default="")
    NIN = models.CharField(max_length=50, null=True, blank=True)
    client_NO = models.CharField(max_length=50, null=True, blank=True, unique=True)

    date_of_birth = models.DateField(null=True, blank=True)
    
    user_fullname = models.CharField(max_length=80, null=True, blank=True)
    gender = models.CharField(max_length=7, null=True, choices = GENDER_CHOICES)
    contacts = models.CharField(max_length=50)
    search_string = models.CharField(max_length=120, null=True, blank=True)
    address = models.CharField(max_length = 100, null=True, blank=True)
    client_image = models.ImageField(null=True, blank=True, upload_to ="images")
    #speed optimization
    original_balance = models.FloatField(default=0, null=True, blank=True)
    amount_paid  = models.FloatField(default=0, null=True, blank=True)
    balance  = models.FloatField(default=0, null=True, blank=True)
    client_user_accountID = models.IntegerField(null=True, blank=True, default=0)
    userID = models.ForeignKey(User, null=True, blank=True,  on_delete = models.CASCADE)
    record_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return str(self.id)+": "+str(self.surname)+" "+str(self.firstname)+" "+str(self.othernames)

    def save(self, *args,**kwargs):
        self.search_string = str(self.surname)+" "+str(self.firstname)+" "+str(self.othernames)+" "+str(self.NIN)+" "+str(self.contacts)
        self.fullname = str(self.surname)+" "+str(self.firstname)+" "+str(self.othernames)
        super(Student, self).save(*args, **kwargs)
 
    class Meta:
       indexes = [ 
        models.Index(fields=["search_string",]), 
        models.Index(fields=["client_NO",]), 
        models.Index(fields=["record_date",]),  
        models.Index(fields=["client_user_accountID",]), 
        models.Index(fields=["NIN",]),
       ]






class CashBook(models.Model):
    businessID = models.ForeignKey(Business, on_delete = models.CASCADE, null=True, blank=True)
    stationID = models.ForeignKey(Station, on_delete = models.CASCADE, null=True, blank=True)
    item_typeID = models.ForeignKey(ItemType, on_delete = models.CASCADE, null=True, blank=True)
    money_sourceID = models.ForeignKey(MoneySource, on_delete = models.CASCADE, null=True, blank=True)
    pay_methodID = models.ForeignKey(PaymentMethod, on_delete = models.CASCADE, null=True, blank=True)
    
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
    is_deleted = models.BooleanField(default=False, null=True, blank=True)

    #color code=red indicated refunded
    color_code = models.CharField(max_length=10, null=True, blank=True) 
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
         ]


    def save(self, *args,**kwargs): 
        current_employee = Employee.objects.get(userID = self.userID)

        GLOBAL_DEFS.save_business_info(self, current_employee)
 
        try:
          last_cashbook = CashBook.objects.filter(
                                                  id__lt = self.id, 
                                                  stationID = current_employee.stationID,
                                                  ).order_by("-id")[0]
        except:
          last_cashbook = None
  
          self.net = float(self.income_received) - float(self.expense_made)
          self.net_str =  "{:,}".format(float(self.net)) if self.net >= 0  else "(" +  "{:,}".format(-1*float(self.net)) + ")"
        
        if last_cashbook is None:
          self.running_total  = float(self.net)+ float(0)
          self.running_total_str =  "{:,}".format(float(self.running_total)) if self.running_total >= 0 else  "(" + "{:,}".format(-1*float(self.running_total)) + ")"
        else:
          self.running_total  = float(self.net)+ float(last_cashbook.running_total)


          self.running_total_str =  "{:,}".format(float(self.running_total)) if self.running_total >=0  else "(" + "{:,}".format(-1*float(self.running_total)) + ")"

        super(CashBook, self).save(*args, **kwargs)

       




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





