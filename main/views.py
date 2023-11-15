from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import * 
from django.core.exceptions import ValidationError

from django.db.models import Count
import pdfkit
from django.template.loader import get_template
from io   import BytesIO
from xhtml2pdf import pisa  

# retourner du json 
from django.http import JsonResponse

# afficher du contenu avec json 

from django.template.loader import render_to_string

from django.http import HttpResponse, HttpResponseRedirect

from .forms import * 

from .pdf import A4Printer

from django.contrib import messages

# file response pour les telechargements

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from users.forms import *

from users.decorators import *

from django.forms.models import model_to_dict


 



def Download_demandeur_pdf(request, demandeur_id):

    demandeur = Demandeur.objects.get(slug = demandeur_id)
    if(demandeur.Conjoint_vie == None):
        conjoint = "Pas de conjoint"
        revenuFemme = 'Pas de coinjoint'
    else:
        conjoint = Conjoint.objects.get( pk = demandeur.Conjoint_vie.id)
        revenuFemme = Revenu_mensuel.objects.get(pk = conjoint.Revenu_femme.id)
    piecesjointes = Pieces_Jointes.objects.get(pk = demandeur.Fichiers_joint.id)

    # creation du tampon de flux d'octets

    tempon = io.BytesIO()

    #  creation d'un canvas

    c = canvas.Canvas(tempon, pagesize = letter, bottomup = 0)

    #  creation de l'object texte

    textObj = c.beginText()
    textObj.setTextOrigin(inch, inch)
    textObj.setFont('Helvetica', 13)

    #  ajout des ligne de texte

    lines = []

    lines.append('Nom : {}'.format(demandeur.Noms_demandeur))
    lines.append('Prénom : {}'.format(demandeur.Prenom_demandeur))
    lines.append('date de naissance : {}'.format(demandeur.Date_de_naissance))
    lines.append('Lieu de naissance : {}'.format(demandeur.Lieu_de_Naissance))
    lines.append('Ville d\'origine : {}'.format(demandeur.Ville_origine))
    lines.append('Satut : {}'.format(demandeur.Statut))
    lines.append('Situation familiale : {}'.format(demandeur.Situation_famille))
    lines.append('Profession : {}'.format(demandeur.Profession))
    lines.append('Matricule : {}'.format(demandeur.Matricule))
    lines.append('Employeur : {}'.format(demandeur.Employeur))

    for line in lines:
        textObj.textLine(line)

    # finition

    c.drawText(textObj)
    c.showPage()
    c.save()

    
    tempon.seek(0)

    # retouner le fichier

    return FileResponse(tempon, as_attachment = True, filename = 'demandeur.pdf')



 


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        profile = request.user
        
        if( profile.role == 'Supperviseur' or profile.role == 'Administrateur'):
            return redirect('dash')
        elif(profile.role == 'Gestionnaire'):
            return redirect('home')
        return redirect('cfc_home')

@login_required
@is_gestionnaire_required
def home(request):
    context = {}

    allDemandeur = Demandeur.objects.all()
    context['allDemandeur'] = allDemandeur
    countDemandeur = Demandeur.objects.count()

    
    context['home'] = True
    context['countDemandeur'] = countDemandeur
    return render(request, 'demandeurlist.html', context)
    


@login_required
@is_gestionnaire_required
def formdemandeur(request):

    context = {}
    allDemandeur = Demandeur.objects.all()
    formDemandeur = DemandeurForm(request.POST or None, request.FILES or None)
    formEngagement_Client = Engagement_ClientForm(request.POST or None)
    formEngagement_Financier = Engagement_FinancierForm(request.POST or None)
    formRevenuFemme = RevenuFemmeForm(request.POST or None)
    formRevenuHomme = RevenuFemmeForm(request.POST or None)
    formEnfant_legitime = Enfant_legitimeForm(request.POST or None)
    formConjoint = ConjointForm(request.POST or None)
    formPieces_Jointes = Pieces_JointesForm(request.POST or None, request.FILES or None)
    formVille = VilleForm()
    formprofession = ProfessionForm()
    formBanque =BanqueForm()
    formEmployeur = EmployeurForm()
    

    context['formVille'] = formVille
    context['formprofession'] = formprofession
    context['formEmployeur'] = formEmployeur
    context['formBanque'] = formBanque

    context['home'] = True

    if(request.method == 'POST'):
        # if(request.POST['villeA']):
        #     if(formVille.is_valid()):
        #         formVille.save()
        # if (formDemandeur.is_valid() and formEngagement_Client.is_valid()
        #     and formRevenuFemme.is_valid() and formRevenuHomme.is_valid()
        #     and formEnfant_legitime.is_valid() and formConjoint.is_valid()
        #     and formPieces_Jointes.is_valid() and formEngagement_Financier.is_valid()
        # ):
        if (formDemandeur.is_valid() 
        ):
       
        
           
            engagementclient = formEngagement_Client.save()
            fianc = formEngagement_Financier.save()
            # revenufemme = formRevenuFemme.save()
            revenuhomme = formRevenuHomme.save()

            # El = False
            # if(formEnfant_legitime.cleaned_data['Nom'] != None):

            #     Enfant_legitm = formEnfant_legitime.save()
            #     El = True
            # Cj = False
            # if( formConjoint.cleaned_data['Nom_conjoint'] != None):
        
            #     conjoint = formConjoint.save(commit = False)
            #     conjoint.Revenu_femme = revenufemme
            #     conjoint.save()
            #     Cj = True
            
            


            pieces = formPieces_Jointes.save(commit = False)
            
            demandeur = formDemandeur.save(commit = False)
            demandeur.createur = request.user
            demandeur.revenu = revenuhomme
            
          
            # if(Cj):
            #     demandeur.Conjoint_vie = conjoint
            # if(El):
            #     demandeur.Enfant_leg = Enfant_legitm
            # demandeur.Engagement = engagementclient
            # demandeur.Engagement_bancaire = fianc
            # demandeur.Fichiers_joint = pieces
            # demandeur.Revenu_homme = revenuhomme

            demandeur.save()
            pieces.demande = demandeur
            pieces.save()
            messages.success(request, "Demandeur ajouté avec succèss")
            return redirect('home')

        else:
            print(formDemandeur.errors)
            messages.error(request, "Erreur veuillez remplir tout les champs requis")
    # passing form in context
    context['formDemandeur'] = formDemandeur
    context['formEngagement_Client'] = formEngagement_Client
    # context['formRevenuFemme'] = formRevenuFemme
    context['formRevenuHomme'] = formRevenuHomme
    # context['formEnfant_legitime'] = formEnfant_legitime
    # context['formConjoint'] = formConjoint
    context['formPieces_Jointes'] = formPieces_Jointes
    context['formEngagement_Financier'] = formEngagement_Financier

    

    return render(request, "demandeur.html", context)



@login_required
@is_gestionnaire_required
def DeleteDemandeur(request, demandeur_id):

    demandeur = Demandeur.objects.get(slug = demandeur_id)
    demandeur.delete()
    messages.success(request, "Demandeur supprimé avec succèss")
    return redirect('home')


@login_required
@is_gestionnaire_required
def VerifyeDeleting(request, demandeur_id):

    demandeur = Demandeur.objects.get(slug = demandeur_id)
    
    return render(request, "confirmDeletetion.html",{'demandeur':demandeur})


@login_required
@is_gestionnaire_required
def ViewDemandeur(request, demandeur_id):
    context = {}
    context['DEVISE'] = 'FCFA'
    demandeur = Demandeur.objects.get(slug = demandeur_id)
    # if(demandeur.Conjoint_vie == None):
    #     conjoint = "Pas DE CONJOINT "
    #     revenuFemme = 'pas de conjoint'
    # else:
    #     conjoint = Conjoint.objects.get( pk = demandeur.Conjoint_vie.id)
    #     revenuFemme = Revenu_mensuel.objects.get(pk = conjoint.Revenu_femme.id)
    piecesjointes = Pieces_Jointes.objects.get(demande = demandeur)
    context['home'] = True
    context['demandeur'] = demandeur
    # context['revenuFemme'] = revenuFemme
    return render(request, 'custumdemandeur.html', context)


@login_required
@is_gestionnaire_required
def DemandeurResults(request):
    if(request.method == 'GET'):
        search = request.GET['search']
        # search = search.capitalize()
        allDemandeur = Demandeur.objects.filter( Noms_demandeur__icontains = search)
       
        context = {}
        context['allDemandeur'] = allDemandeur
        context['home'] = True
        return render(request, 'demandeur/search.html', context)

@login_required
@is_gestionnaire_required
def updateDemandeur(request, demandeur_id):

    context = {}

    demandeur = Demandeur.objects.get(slug = demandeur_id)
    allDemandeur = Demandeur.objects.all()
    formDemandeur = DemandeurForm(request.POST or None, request.FILES or None, instance= demandeur)
    formEngagement_Client = Engagement_ClientForm(request.POST or None, instance= demandeur.Engagement)
    formEngagement_Financier = Engagement_FinancierForm(request.POST or None, instance=demandeur.Engagement_bancaire)
    if(not demandeur.Conjoint_vie):
        formRevenuFemme = RevenuFemmeForm(request.POST or None)
    else:
        formRevenuFemme = RevenuFemmeForm(request.POST or None, instance=demandeur.Conjoint_vie.Revenu_femme)
    formRevenuHomme = RevenuFemmeForm(request.POST or None, instance=demandeur.Revenu_homme)
    formEnfant_legitime = Enfant_legitimeForm(request.POST or None, instance=demandeur.Enfant_leg)
    formConjoint = ConjointForm(request.POST or None, instance=demandeur.Conjoint_vie)
    formPieces_Jointes = Pieces_JointesForm(request.POST or None, request.FILES or None, instance=demandeur.Fichiers_joint)

    context['home'] = True

    if(request.method == 'POST'):
        # if(request.POST['villeA']):
        #     if(formVille.is_valid()):
        #         formVille.save()
        if (formDemandeur.is_valid() and formEngagement_Client.is_valid()
            and formRevenuFemme.is_valid() and formRevenuHomme.is_valid()
            and formEnfant_legitime.is_valid() and formConjoint.is_valid()
            and formPieces_Jointes.is_valid() and formEngagement_Financier.is_valid()
        ):
       
        
           
            engagementclient = formEngagement_Client.save()
            fianc = formEngagement_Financier.save()
            revenufemme = formRevenuFemme.save()
            revenuhomme = formRevenuHomme.save()

            El = False
            if(formEnfant_legitime.cleaned_data['Nom'] != None):

                Enfant_legitm = formEnfant_legitime.save()
                El = True
            Cj = False
            if( formConjoint.cleaned_data['Nom_conjoint'] != None):
        
                conjoint = formConjoint.save(commit = False)
                conjoint.Revenu_femme = revenufemme
                conjoint.save()
                Cj = True
            
            


            pieces = formPieces_Jointes.save()
            
            demandeur = formDemandeur.save(commit = False)
            demandeur.Auteur = request.user
            if(Cj):
                demandeur.Conjoint_vie = conjoint
            if(El):
                demandeur.Enfant_leg = Enfant_legitm
            demandeur.Engagement = engagementclient
            demandeur.Engagement_bancaire = fianc
            demandeur.Fichiers_joint = pieces
            demandeur.Revenu_homme = revenuhomme

            demandeur.save()
            return redirect('home')
      
            
                
    




    # passing form in context
    context['formDemandeur'] = formDemandeur
    context['formEngagement_Client'] = formEngagement_Client
    context['formRevenuFemme'] = formRevenuFemme
    context['formRevenuHomme'] = formRevenuHomme
    context['formEnfant_legitime'] = formEnfant_legitime
    context['formConjoint'] = formConjoint
    context['formPieces_Jointes'] = formPieces_Jointes
    context['formEngagement_Financier'] = formEngagement_Financier

    context['Mod'] = True

    formVille = VilleForm()
    formprofession = ProfessionForm()
    formBanque =BanqueForm()
    formEmployeur = EmployeurForm()
    

    context['formVille'] = formVille
    context['formprofession'] = formprofession
    context['formEmployeur'] = formEmployeur
    context['formBanque'] = formBanque
    
    
    return render(request, 'demandeur.html', context)




@login_required
@is_supperviseur_required
def Appartements(request):

    context = {}

    formAppartement = AppartementForm(request.POST or None, )
    if(request.method == 'POST'):
        if(formAppartement.is_valid()):
            formAppartement.save()
            messages.success(request, "appartement ajouté avec succèss")
            return HttpResponseRedirect('Appartement')
    
    AllApp = Appartement.objects.all()
    context['AllApp'] = AllApp 
    context['formAppartement'] = formAppartement
    context['app'] = True
    return render(request, "appartement/index.html", context)


@login_required
@is_supperviseur_required
def DeleteAppartement(request,appartent_id):
    app = Appartement.objects.get(pk = appartent_id)
    app.delete()
    messages.success(request, "Appartement supprimé avec succès")
    return redirect('Appartement')

@login_required
@is_supperviseur_required
def EditApparatement(request,appartent_id):
    context = {}
    app = Appartement.objects.get(pk = appartent_id)
    formAppartement = AppartementForm(request.POST or None, instance = app)
    if(request.method == 'POST'):
        if(formAppartement.is_valid()):
            formAppartement.save()
            return redirect('Appartement')
    
    
    context['formAppartement'] = formAppartement
    context['app'] = True
    context['appart'] = app
    return render(request, "appartement/edit.html", context)




@login_required
@is_supperviseur_required
def Immeubles(request):

    context = {}

    formImmeuble = ImmeubleForm(request.POST or None)
    if(request.method == 'POST'):
        if(formImmeuble.is_valid()):
            formImmeuble.save()
            return HttpResponseRedirect('Immeubles')
    
    AllImb = Immeuble.objects.all()
    context['AllImb'] = AllImb 
    context['formImmeuble'] = formImmeuble
    context['im'] = True
    return render(request, "immeuble/index.html", context)


@login_required
@is_supperviseur_required
def DeleteImmeuble(request,immeuble_id):
    imm = Immeuble.objects.get(pk = immeuble_id)
    imm.delete()
    return redirect('Immeuble')

@login_required
@is_supperviseur_required
def EditImmeuble(request,immeuble_id):
    context = {}
    imm = Immeuble.objects.get(pk = immeuble_id)
    formIm = ImmeubleForm(request.POST or None, instance = imm)
    if(request.method == 'POST'):
        if(formIm.is_valid()):
            formIm.save()
            return redirect('Immeuble')
    
    
    context['formIm'] = formIm
    context['im'] = True
    context['imm'] = imm
    return render(request, "immeuble/edit.html", context)



@login_required
@is_supperviseur_required
def Logements(request):

    context = {}

    formbloc = Logement_socialForm(request.POST or None)
    
    if(request.method == 'POST'):
        if(formbloc.is_valid()):
            formbloc.save()
            return HttpResponseRedirect('Logements')
    
    Allloc = Logement_social.objects.all()
    context['Allloc'] = Allloc 
    context['formbloc'] = formbloc
    context['log'] = True
    
    return render(request, "logement/index.html", context)


@login_required
@is_supperviseur_required
def DeleteLogement(request,logement_id):
    imm = Logement_social.objects.get(pk = logement_id )
    imm.delete()
    return redirect('Logement')

@login_required
@is_supperviseur_required
def EditLogement(request,logement_id):
    context = {}
    imm = Logement_social.objects.get(pk = logement_id)
    formbloc = Logement_socialForm(request.POST or None, instance = imm)
    if(request.method == 'POST'):
        if(formbloc.is_valid()):
            formbloc.save()
            return redirect('Logement')
    
    
    context['formbloc'] = formbloc
    context['log'] = True
    context['imm'] = imm
    return render(request, "logement/edit.html", context)





@login_required
@is_supperviseur_required
def Decision(request):

    context = {}

    formdecision = DecisionForm(request.POST or None, request.FILES or None)
    # if(request.method == 'POST'):
    #     if(formdecision.is_valid()):
    #         # des = formdecision.save()
    #         print(formdecision.cleaned_data['Commentaire '])
            
    #         # appartement = Appartement.objects.get(pk = des.Numero_logement_attribue)
    #         # demandeur = Demandeur.objects.get(id = formdecision.cleaned_data['Demandeur'])
    #         # appartement.demandeur = demandeur
    #         # appartement.save()
           
    #         return HttpResponseRedirect('Decision')
    
    Allldec = Decision_comite_attribution.objects.all()
    context['Allldec'] = Allldec 
    context['formdecision'] = formdecision
    context['des'] = True
    alldemande = Demandeur.objects.all()
    context['alldemande'] = alldemande
    return render(request, "decision/index.html", context)

@is_supperviseur_required
def decision_form(request):
    context = {}
    appart_vide = Appartement.objects.filter(Vide = True)
    demandes = Demandeur.objects.filter(Etat_demandes = False)
    form = DecisionForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        Valid = True
        if form.is_valid():
            Valid = True
            demande_id = request.POST['demande']
            appartement_id = request.POST['appartement']
            decision = form.save(commit = False)

            appartement = None
            demande = None


            # Conversion en entier
            try:
                demande_id = int(demande_id)
            except  ValueError:
                demande_id = -1
            # Conversion en entier
            try:
                appartement_id = int(appartement_id)
            except  ValueError:
                appartement_id = -1

            #  Recuperation du demandeur
            try:
                demande = Demandeur.objects.get(pk = demande_id)
            except Demandeur.DoesNotExist:
                demande = None
            # Récuperation de l'appartement
            try:
                appartement = Appartement.objects.get(pk = appartement_id)
            except Appartement.DoesNotExist:
                appartement = None
            # Avis de validation
            Avis = decision.Favorable

            if Avis == True and ( appartement == None or demande ==None ):
                Valid = False
                messages.error(request, """
                Veuillez verifier tous vons champ <br> vous avez
                validé l'attribution sans remplir les champs 
                demandeur et appartement convemablement
                """)
            else:
                decision.Demandeur = demande
                decision.Numero_logement_attribue = appartement
                appartement.Vide = False
                appartement.save()
                decision.save()
                messages.success(request, 'Décision créée avec succès')
            
            
        # else:
        #     Valid = False
        #     messages.error(request, 'Veuillez verifier votre formulaire')

        if Valid :
            messages.error(request, """
                Veuillez verifier tous vons champ <br> vous avez
                validé l'attribution sans remplir les champs 
                demandeur et appartement convemablement
            """)
        else:
            messages.error(request, """
                Veuillez verifier tous vons champ <br> vous avez
                validé l'attribution sans remplir les champs 
                demandeur et appartement convemablement
            """)

        
    context['appart_vide'] = appart_vide
    context['demandes'] = demandes
    context['form'] = form

    return render(request,'decision/form.html', context)

def get_demandeur(request, id):

    demandeur = Demandeur.objects.get(pk = id)
    nbpdispo = demandeur.getPieceNumber()
    nbpiece_total = demandeur.getTotalPieces()
    return JsonResponse({
        'demandeur': model_to_dict(demandeur), 
        'nbpdispo': nbpdispo, 
        'nbpiece_total': nbpiece_total
    }, status = 200)

def get_appart(request, id):
    appart = Appartement.objects.get(pk = id)

    return JsonResponse({
        'appart': model_to_dict(appart), 
    }, status = 200)


def Decision_add(request):
    formdecision = DecisionForm(request.POST ,  request.FILES )
    if formdecision.is_valid():
        print(formdecision.cleaned_data['Commentaire'])
        return JsonResponse({}, status = 200)
    else:
        print()
        return JsonResponse({})
@login_required
@is_supperviseur_required
def DeleteDecision(request,Decision_id):
    imm = Decision_comite_attribution.objects.get(pk = Decision_id )
    imm.delete()
    return redirect('Decision')

@login_required
@is_supperviseur_required
def EditDecision(request,Decision_id):
    context = {}
    imm = Decision_comite_attribution.objects.get(pk = Decision_id)
    formdecision = DecisionForm(request.POST or None, instance = imm)
    if(request.method == 'POST'):
        if(formdecision.is_valid()):
            formdecision.save()
            #demandeur = Demandeur.objects.get('')
            return redirect('Decision')
    
    
    context['formdecision'] = formdecision
    context['des'] = True
    context['imm'] = imm
    return render(request, "decision/edit.html", context)


@login_required
@is_supperviseur_required
def addVille(request):
    formVille = VilleForm(request.POST)
    if formVille.is_valid():
        new_ville = formVille.save()
        
        return JsonResponse({'new_ville': model_to_dict(new_ville)
            
        }, status = 200)
    # else:
    #     return redirect('')

@login_required
@is_supperviseur_required
def addprofession(request):
    formprofession = ProfessionForm(request.POST)
    if formprofession.is_valid():
        new_prosession = formprofession.save()
        return JsonResponse(
            {'new_prosession': model_to_dict(new_prosession)
        }, status = 200)
@login_required
@is_gestionnaire_required
def addbanque(request):
    formBanque = BanqueForm(request.POST)
    if formBanque.is_valid():
        new_banque = formBanque.save()
        
        return JsonResponse({'new_banque': model_to_dict(new_banque)
            
        }, status = 200)

@login_required
@is_gestionnaire_required
def addempoyeur(request):
    formEmpoyeur = EmployeurForm(request.POST)
    if formEmpoyeur.is_valid():
        new_employeur = formEmpoyeur.save()
        
        return JsonResponse({'new_employeur': model_to_dict(new_employeur)
            
        }, status = 200)


@login_required
@is_gestionnaire_required
def demandeurPdf(request, demandeur_slug):
    template = get_template('pdf2.html')

    demandeur = Demandeur.objects.get(slug = demandeur_slug)
    # if(demandeur.Conjoint_vie == None):
    #     conjoint = "Pas DE CONJOINT "
    #     revenuFemme = 'pas de conjoint'
    # else:
    #     conjoint = Conjoint.objects.get( pk = demandeur.Conjoint_vie.id)
    #     revenuFemme = Revenu_mensuel.objects.get(pk = conjoint.Revenu_femme.id)
    piecesjointes = Pieces_Jointes.objects.get(demande = demandeur)
    
    
    
    context = {}
    context['DEVISE'] = 'Fcfa'
    context['demandeur'] = demandeur
    # context['revenuFemme'] = revenuFemme
    html = template.render(context)
    options = {
        'page-size': 'Letter',
        'encoding':  'UTF-8',
        
    }

    result = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')),result)

    
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type = 'application/pdf')
    return None


@login_required
@is_supperviseur_required
def dash(request):
    context = {}
    context['dash'] = True

    nbdemandeur = Demandeur.objects.count()
    nbappart = Appartement.objects.count()
    nblogement = Logement_social.objects.count()
    nbappimme = Immeuble.objects.count()
    nb_nom_traite = Demandeur.objects.filter(Etat_demandes = False).count()
    # nb_nom_accorde = Decision_comite_attribution.objects.filter(Favorable = False).count()
    nb_nom_accorde = 1
    # nb_accorde = Decision_comite_attribution.objects.filter(Favorable = True).count()
    nb_accorde = 1
    nbdecision = Decision_comite_attribution.objects.count()
    nbappart_occupe = Appartement.objects.filter(Vide = False).count()
    nbappart_libre = Appartement.objects.filter(Vide = True).count()
    try:
        porcentage_occupation = (nbappart_occupe * 100) / (nbappart_libre + nbappart_occupe) or None
    except:
        porcentage_occupation = 0
    context['nbdemandeur'] = nbdemandeur
    context['nbappart'] = nbappart
    context['nbappimme'] = nbappimme
    context['nblogement'] = nblogement
    context['nbappart_occupe'] = nbappart_occupe
    context['nbappart_libre'] = nbappart_libre
    context['porcentage_occupation'] =porcentage_occupation
    context['nbdecision'] = nbdecision
    context['nb_nom_traite'] = nb_nom_traite
    context['nb_nom_accorde'] = nb_nom_accorde
    context['nb_accorde'] = nb_accorde
    
    alllogements = Logement_social.objects.all()
    allville = []
    allv = Logement_social.objects.values('Ville').annotate(total=Count('id'))
    context['allv'] = allv     
    
    return render(request, 'dash.html',context)



@login_required
def profile(request):

    context = {}
   
    context['profile'] = True
    
    account = Utilisateur.objects.get(id = request.user.id)
    role = account.role
    formProfileMod =   UserProfileMod(request.POST or None, request.FILES or None , instance = request.user, )
    if request.method == 'POST':
        if formProfileMod.is_valid():
            formProfileMod.save()
        else:
             messages.error(request, "")
    if(role == 'Agent CFC'):
        template = 'cfc_base.html'
    else:
        template = 'base2.html'
    
    context['template'] = template
    context['account'] = account
    context['formProfileMod'] = formProfileMod
    return render(request, 'registration/profile.html', context)


@login_required
@is_supperviseur_required
def Logements_details(request, logement_id):
    context = {}
    context['log'] = True
    context['logement'] = Logement_social.objects.get(pk = logement_id)


    context['all_immeubles'] = Immeuble.objects.filter(bloc_id = logement_id)
    return render(request, 'logement/logement_details.html', context)


def get_immeuble(request, id):
    immeuble = Immeuble.objects.get(pk = id)
    appartement = Appartement.objects.filter(immeuble = immeuble)
    context = {}
    context['appartement'] = appartement
    html_document = render_to_string('logement/apartement_draw.html',
    context,
    request=request,
    )
   

    return JsonResponse({'html_document' : html_document})