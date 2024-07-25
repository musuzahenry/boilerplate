from django import forms
from finance.models import ClientNextOKin



class ClientNextOKinForm(forms.ModelForm):
    class Meta:
        model = ClientNextOKin
        fields = "__all__"
