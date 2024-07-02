from django import forms
from sysadmin.models import Employee



class EmployeeForm(forms.ModelForm):
    class Meta:
       model =Employee
       fields = ["firstname", "surname", "othername", "employee_image", "gender", "date_of_birth", "NIN", \
                "positionID" ,"date_of_hire", "employee_title", "qualifications", \
                 "NSSF_NO", "phone_contacts", "email_address", "address", "bank_name", "bank_branch", \
                "bank_account_no", "system_roleID", "is_system_user","academic_documents_upload", \
                 "net_salary", "nssf", "PAYE", 
                "next_of_kin_names", "next_of_kin_contacts","next_of_kin_address", 
                "next_of_kin2_names", "next_of_kin2_contacts", "next_of_kin2_address", 
                ] 
