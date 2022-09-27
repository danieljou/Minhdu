from django.shortcuts import render, redirect
from users.decorators import is_cfc_required
from django.contrib.auth.decorators import login_required
from main.models import Demandeur, Pieces_Jointes
from django.contrib import messages
from .forms import *
# Create your views here.

from django.http import JsonResponse


@login_required
@is_cfc_required
def index(request):
    context = {}
    all_demandes = Demandeur.objects.filter(Type_paiement = 'CFC')
    context['home'] = True
    context['all_demandes'] = all_demandes
    return render(request, 'cfc_index.html', context)


@login_required
@is_cfc_required
def favorable(request):
    context = {}
    all_demandes = Demandeur.objects.filter(Type_paiement = 'CFC', info_cfc = 'F')
    context['fav'] = True
    context['all_demandes'] = all_demandes
    return render(request, 'cfc_index.html', context)


@login_required
@is_cfc_required
def non_favorable(request):
    context = {}
    all_demandes = Demandeur.objects.filter(Type_paiement = 'CFC', info_cfc = 'NF')
    context['nfav'] = True
    context['all_demandes'] = all_demandes
    return render(request, 'cfc_index.html', context)


@login_required
@is_cfc_required
def non_traite(request):
    context = {}
    all_demandes = Demandeur.objects.filter(Type_paiement = 'CFC', info_cfc = 'NT')
    context['ntr'] = True
    context['all_demandes'] = all_demandes
    return render(request, 'cfc_index.html', context)


@login_required
@is_cfc_required
def Validate(request,demandeur_slug):
    demandeur = Demandeur.objects.get(slug = demandeur_slug)
    form = AccordForm(request.POST or None, request.FILES or None)
    context = {}
    context['form'] = form
    context['fav'] = True
    context['demandeur'] = demandeur
    if(request.method == 'POST'):
        if(form.is_valid()):
            activate = form.cleaned_data['Avis']
            if(activate):
                demandeur.info_cfc = 'F'
                demandeur.save()
                messages.success(request,'Demande confirmée')
            else:
                demandeur.info_cfc = 'NF'
                demandeur.save()
                messages.success(request,'Demande refusée')
            data = form.save(commit = False)
            data.demande = demandeur
            data.save()
            return redirect('cfc_home')
        else:
            messages.warning(request,'erreur')
    return render(request,'cfc_favorable.html',context)


@login_required
@is_cfc_required
def custum(request, demandeur_slug):

    context = {}
    demandeur = Demandeur.objects.get(slug = demandeur_slug)
    accord = None
    try:
        accord = Accord.objects.get(demande = demandeur.id)
    except Accord.DoesNotExist:
        go = None

    
    context['demandeur'] = demandeur
    context['home'] = True
    if accord != None:
        context['accord'] = accord
    return render(request,'cfc_custum.html', context)


