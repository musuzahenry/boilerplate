

from django import forms
from finance.models import CashBook


class CashBookForm(forms.ModelForm):
    class Meta:
        model = CashBook
        fields = "__all__"