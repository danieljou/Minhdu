from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
from .decorators import *

# Create your views here.

@login_required
@is_admin_required
def index(request):
    context = {}
    context['users'] = True
    allusers = User.objects.exclude(id = request.user.id)
    context['allusers'] = allusers
    return render(request,'index.html',context)

@login_required
@is_admin_required
def add_form(request):
    context = {}
   
    form_user = FormUser(request.POST or None, request.FILES or None)

    if(request.method == 'POST'):
        if(form_user.is_valid()):
            account = form_user.save()
            messages.success(request, "Enregistrement éffectué avec succès")
            return redirect('users')
        else:
             messages.warning(request, "Veuillez compléter le formulaire")

    context['form_user'] = form_user
    context['users'] = True
    return render(request,'form.html',context)

def user_mod(request,user_id):
    
    users = User.objects.get(pk =user_id)
    context = {}
    form_user = FormUserMod(request.POST or None, request.FILES or None,instance = users )
    if(request.method == 'POST'):
        if(form_user.is_valid()):
            account = form_user.save()
            messages.success(request, "Modification éffectuée avec succès")
            return redirect('users')
        else:
             messages.warning(request, "Veuillez compléter le formulaire")

    context['form_user'] = form_user 
    context['users'] = True
    return render(request,'form.html',context)


def user_confirm_delation(request,user_id):
    account = Custum_user.objects.get(pk = user_id)
    users = User.objects.get(pk = account.user.id)

    context={}
    context['users'] = True
    context['users'] = users
    return render(request, 'confirm.html', context)

def delete_user(request,user_id):
    users = User.objects.get(pk = user_id)
    users.delete()
    messages.success(request,"Utilisateur supprimé avec success")
    return redirect('users')


      