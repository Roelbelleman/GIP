from django.forms import ModelForm
from .models import idModel
from django import forms
from django.forms.widgets import DateInput

class idForm(forms.ModelForm):
    class Meta:
        model = idModel
        fields = '__all__'
        widgets = {
           'password': forms.PasswordInput(),
        }
        labels = {
            "password": "password",
            "username" : "username",
            "school" : "school"
        }
class dateField(forms.Form):
    date_field = forms.DateField(widget=DateInput(attrs={
        'type': 'date',
        'placeholder': 'yyyy-mm-dd',
        'id' : 'datafield'
        }), label="")

