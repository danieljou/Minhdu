import django.db
from .models import *
from django import forms
from django.forms import (
    CheckboxInput,TextInput,ModelForm,EmailInput, 
    NumberInput, DateInput, 
    BooleanField, Select, FileInput,
    Textarea,
    
)
from django.conf import settings


class AccordForm(forms.ModelForm):
    
    class Meta:
        model = Accord
        exclude = ('demande',)

        widgets = {
            
            'Commentaire': Textarea(
                attrs = {
                    'row':2
                }
            ),   
            'Justificatif':FileInput(attrs={
                'class':'form-control'
            })
        }

