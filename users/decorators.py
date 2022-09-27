from functools import wraps
from django.http import HttpResponseRedirect
from .models import *



def is_admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        profile = request.user
       
        if(profile.role == 'Administrateur'):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    return wrap

def is_gestionnaire_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        profile = request.user
       
        if(profile.role == 'Gestionnaire' or profile.role == 'Supperviseur' or profile.role == 'Administrateur'):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    return wrap


def is_cfc_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        profile = request.user
        
        if(profile.role == 'Agent CFC'):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    return wrap

def is_supperviseur_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        profile = request.user
        
        if(profile.role == 'Supperviseur' or profile.role == 'Administrateur'):
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
    return wrap