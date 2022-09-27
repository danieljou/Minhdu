
    # from django import forms
import django.db
from .models import *
from django import forms
from django.forms import (
    CheckboxInput,TextInput,ModelForm,EmailInput, 
    NumberInput, DateInput, 
    BooleanField, Select, FileInput,
    Textarea,
    
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings



from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput


from django.core.exceptions import ObjectDoesNotExist



class DemandeurForm(forms.ModelForm):
    class Meta:
        model = Demandeur
        exclude = (
            'Auteur','Matricule',
            'slug', 'Enfant_leg',
            'Conjoint_vie', 'Engagement_bancaire',
            'Revenu_homme', 'Engagement',
            'Fichiers_joint', 'Decision_attribution',
            'Publie_le', 'Statut',
            'info_cfc',     
            'Etat_demandes',

            )
        
        widgets = {
            'Situation_famille' : forms.Select(
                attrs = {
                    'class': 'statutMat'
                }
            ),

            'Date_de_naissance': TextInput(attrs = {
                'type':'date'
            }),
            'Type_paiement': forms.Select(  attrs = {
                'class' : 'form-select'
            }),
            'Civilite': forms.Select(  attrs = {
                'class' : 'form-select'
            }),
            'Ville_origine': forms.Select(  attrs = {
                'class' : 'form-select'
            }),
            'Situation_famille': forms.Select(  attrs = {
                'class' : 'form-select'
            }),
    
            
        }

        labels = {
            'Date_naiss':'Date de naissance',
        }
       
        


class Engagement_ClientForm(forms.ModelForm):
    
    class Meta:
        model = Engagement_Client
        fields = ('__all__')

class RevenuFemmeForm(forms.ModelForm):
    
    class Meta:
        model = Revenu_mensuel
        fields = ('__all__')
        widgets = {
            'Nature': Select(attrs = {
                'class': 'form-select'
            }),

            'Montant': NumberInput (attrs = {
                'placeholder': 'Entrez le montant'
            })
        }

class Enfant_legitimeForm(forms.ModelForm):
    
    class Meta:
        model = Enfant_legitime
        fields = ('__all__')
        widgets = {'Date_naiss':TextInput(attrs={
            'type':'date'
        })}

class ConjointForm(forms.ModelForm):
    
    class Meta:
        model = Conjoint
        exclude = ('Revenu_femme', 'Matricule_conjoint', )
        fields = ('__all__')

class Pieces_JointesForm(forms.ModelForm):
    
    class Meta:
        model = Pieces_Jointes
        fields = ('__all__')
       

class Engagement_FinancierForm(forms.ModelForm):
    
    class Meta:
        model = Engagement_Financier
        fields = ('__all__')
        labels = {
            'Jusquen':'Date de fin',
        }
        widgets = {
            'Jusquen': TextInput( attrs = {
                'type':'date'
            })
        }


class DecisionForm(forms.ModelForm):
    
    class Meta:
        model = Decision_comite_attribution
        exclude = ('Demandeur','Numero_logement_attribue',)
        labels = {
            'Favorable' : 'Valider l\'attribution'
        }


class Logement_socialForm(forms.ModelForm): 

     class Meta:      

       
        model = Logement_social
        fields = '__all__'
        widgets = {
            'Ville': Select( attrs = {
                'class':'form-select'
            }),

            'Quartier': Select( attrs = {
                'class':'form-select'
            }),
        }

    



class ImmeubleForm(forms.ModelForm): 

    class Meta:     
        model = Immeuble
        fields = ('__all__')

        
        widgets = {
            'Lettre': TextInput(attrs = {'class': "form-control",'placeholder': "Lettre",}),   
            'bloc': Select(attrs = {'class': "form-select",  }),    
        }
        labels = {
            'bloc' : 'Logement correspondant'
        }

    def clean_Lettre(self , *args, **kwargs):
        data = self.cleaned_data.get('Lettre')
        try:
            get = Immeuble.objects.get(Lettre = data)
        except ObjectDoesNotExist:
            get = None
        
        if get is not None:
            raise forms.ValidationError("Vous ne pouvez plus utiliser la lettre {} ".format(data))

        # Always return a value to use as the new cleaned data, even if
        # this method didn't change it.
        return data

class AppartementForm(forms.ModelForm): 

    class Meta:      

       
        model =Appartement
        exclude = ('demandeur','Vide',)
        widgets = {
            
            'Descrip_logement': Textarea(
                attrs = {
                    'rows':2
                }
            ),   
        }


    # def clean_Descrip_logement(self , *args, **kwargs):
    #     data = self.cleaned_data.get('Descrip_logement')
    #     if "fred@example.com" not in data:
    #         raise forms.ValidationError("You have forgotten about Fred!")

    #     # Always return a value to use as the new cleaned data, even if
    #     # this method didn't change it.
    #     return data



class VilleForm(forms.ModelForm):
    
    class Meta:
        model = Ville
        fields = ('__all__')


        


class ProfessionForm(forms.ModelForm):
    
    class Meta:
        model = Profession
        fields = ('__all__')


class EmployeurForm(forms.ModelForm):
    
    class Meta:
        model = Employeur
        fields = ('__all__')


class BanqueForm(forms.ModelForm):
    
    class Meta:
        model = Banque
        fields = ('__all__')



