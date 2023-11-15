import django.db
from .models import *
from django import forms
from django.forms import (
    CheckboxInput,TextInput,ModelForm,EmailInput, 
    NumberInput, DateInput, 
    BooleanField, Select, FileInput,
    Textarea,
    
)
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.conf import settings

from main.models import *

class FormUser(UserCreationForm):
    email = forms.EmailField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100, label="Nom")
   
    
    class Meta:
        model = Utilisateur
        fields = [ 'role','username','last_name','first_name','email','password1','password2']
        widgets = {
            'last_name': forms.TextInput(),
            'role': Select(attrs = {
                'class': 'form-select'
            })
        }


class FormUser2(UserCreationForm):
    email = forms.EmailField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100, label="Nom")
   
    
    class Meta:
        model = Utilisateur
        fields = ( 'username','last_name','first_name','email','password1','password2')
        widgets = {
            'last_name': forms.TextInput(),
            'role': Select(attrs = {
                'class': 'form-select'
            })
        }


class FormUserMod(UserCreationForm):
    email = forms.EmailField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100, label="Nom")
   
    
    class Meta:
        model = Utilisateur
        fields = ('username','last_name','first_name','email')
        exlude = ('password1','password2',)
        widgets = {
            'last_name': forms.TextInput()
        }


class UserProfileMod(forms.ModelForm):
    email = forms.EmailField(required=True, max_length=100)
    last_name = forms.CharField(required=True, max_length=100, label="Nom")
   
    
    class Meta:
        model = Utilisateur
        fields = ('username','last_name','first_name','email')
        exlude = ('password1','password2',)
        widgets = {
            'last_name': forms.TextInput()
        }
        labels = {
            'email' : 'Addresse E-mail'
        }