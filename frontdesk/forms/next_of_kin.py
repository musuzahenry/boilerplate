from finance.models import ClientNextOKin
from django import forms


class ClientNextOKinForm(froms.ModelForm):
    class Meta:
        model = ClientNextOKin
        fields = "__all__"