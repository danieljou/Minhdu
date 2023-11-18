import django.forms
from enum import unique
from tkinter import CASCADE
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.auth.models import User, AbstractUser




from django.core.exceptions import ValidationError

class Demandeur(models.Model):

    MONSIEUR = 'M.'
    MADAME = 'Mme'
    MADEMOISELLE = 'Mlle'
    CIVILITE_CHOICHES = [
        (MONSIEUR, 'Monsieur'),
        (MADAME, 'Madame'),
        (MADEMOISELLE, 'Mademoiselle'),
    ]

    CASH = "CASH"
    CFC = 'CFC'
    
    TYPE_PAIEMENT = [
        (CASH, 'Cash'),
        (CFC, 'CFC'),
        
    ]

    MARIE = 'MA'
    VEUF = 'VE'
    CELIBAT = 'CE'
    SITUATION_FAMILLE_CHOICHES = [
        (MARIE, 'Marié(e)'),
        (VEUF, 'Veuf(ve)'),
        (CELIBAT, 'Célibataire'),   
    ]    
    Type_paiement = models.CharField(
        max_length=50,
        choices = TYPE_PAIEMENT,  
    )
    Civilite = models.CharField(
        max_length=4,
        choices=CIVILITE_CHOICHES,
        default=MONSIEUR,
        )
    Noms_demandeur = models.CharField(max_length=80, null=False)
    Prenom_demandeur = models.CharField(max_length=80)
    Date_de_naissance = models.DateField( auto_now=False, auto_now_add=False)
    Lieu_de_Naissance = models.ForeignKey("Ville", related_name = 'naiss_ho' , on_delete=models.SET_NULL, null = True)
    Ville_origine = models.ForeignKey("Ville", related_name = 'vorigine' , on_delete=models.SET_NULL, null = True)
    Situation_matrimoniale = models.CharField(
        max_length=4,
        choices=SITUATION_FAMILLE_CHOICHES,
        default=MARIE,
    )
    Profession = models.ForeignKey("Profession", on_delete=models.SET_NULL, null = True)
    Employeur = models.ForeignKey("Employeur", on_delete=models.SET_NULL, null = True)
    Adresse = models.CharField(max_length=80, null=True , blank = True)
    Email = models.EmailField(max_length=30, null=True , blank = True)
    Telephone = models.IntegerField('Téléphone',null=True , blank = True)
    Numero_identite = models.IntegerField( null=True , blank = True)
    Numero_compte_bancaire = models.IntegerField( null=True , blank = True)
    Nom_banque = models.ForeignKey("Banque", on_delete=models.SET_NULL, null = True)
    Mis_a_jour = models.DateTimeField(auto_now=True)
    Publie_le = models.DateTimeField(auto_now_add = True)
    slug = models.SlugField (max_length=100, unique=True)
    createur = models.ForeignKey('main.Utilisateur', blank = True, on_delete=models.CASCADE, related_name='createur')
    Etat_demandes = models.BooleanField(default = False)
    revenu = models.ForeignKey("Revenu_mensuel",  on_delete=models.CASCADE)

    PiecesTotale = 4
    PieceManquantes = []
    PicesManquantesCfc = []
    
    NT = 'NT'
    FA = 'FA'
    DEF = 'DEF'
    cfc_choice = [
        (NT, 'Marié(e)'),
        (FA, 'Veuf(ve)'),
        (DEF, 'Célibataire'),   
    ]
    info_cfc = models.CharField( max_length=50, choices = cfc_choice, default = NT)
    
    
    class Meta:
        ordering = ['-Publie_le']
    
    def __str__(self):
        return self.Noms_demandeur
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.Noms_demandeur+ ' '+self.Prenom_demandeur + ' ' + str(self.Publie_le)  )
        self.slug = self.slug.replace(" ", "_")
        super(Demandeur, self).save(*args, **kwargs)    

    # def getPieceNumber(self):
    #     nbPieces = 0
    #     state = False
    #     self.PieceManquantes = []
    #     self.PiecesTotale = 4
    #     if(self.Fichiers_joint.Demande_logement):
    #         nbPieces = nbPieces + 1 
    #         state = True  
    #     else:
            
    #         state = False
    #         self.PieceManquantes.append('Demande de logement')

    #     # 
    #     if(self.Fichiers_joint.Cni_demandeur):
    #         nbPieces = nbPieces + 1
    #         state = True
    #     else:
            
    #         state = False
    #         self.PieceManquantes.append('CNI Demandeur')

    #     # 

    #     if(self.Fichiers_joint.Cni_conjoint):
    #         nbPieces = nbPieces + 1
    #         state = True
    #     else:
    #         if self.Civilite == 'NT':
    #             self.PieceManquantes.append('CNI conjoint')
    #             state = False
    #             self.PiecesTotale = self.PiecesTotale + 1 
        
    #     # 

    #     if(self.Fichiers_joint.Acte_naissance):
    #         nbPieces = nbPieces + 1
    #     else:
    #         self.PieceManquantes.append('Acte de naissance')

    #     # 
    #     if(self.Fichiers_joint.Acte_mariage):
    #         nbPieces = nbPieces + 1
    #         state = True
    #     else:
    #         if(self.Conjoint_vie):
    #             self.PieceManquantes.append('Acte de mariage')
    #             state = False
    #             self.PiecesTotale = self.PiecesTotale + 1 
    #         else:
    #             state = True

    #     if(self.Fichiers_joint.Acte_deces_conjoint):
    #         nbPieces = nbPieces + 1
    #         state = True
    #     else:
    #         if(self.Civilite == 'VE'):
    #             state = False
    #             self.PieceManquantes.append('Acte de deccès conjoint')
    #             self.PiecesTotale = self.PiecesTotale + 1 

    #     if(self.Fichiers_joint.Certificat_celibat):
    #         nbPieces = nbPieces + 1
    #         state = True
    #     else:
    #         if(self.Civilite == 'CE'):
    #             state = False
    #             self.PieceManquantes.append('Certificat de célibat')
    #             self.PiecesTotale = self.PiecesTotale + 1 

    #     if(self.Fichiers_joint.Attestation_travail):
    #         nbPieces = nbPieces + 1
    #         state = True
    #     else:
    #         self.PieceManquantes.append('Attestation de travail')
    #         state = False

    #     if(self.Fichiers_joint.Attestation_presence_effective_cfc):
    #         nbPieces = nbPieces + 1
    #         state = True
    #     else:
    #         if(self.Type_paiement == 'CFC'):
    #             state = False
    #             self.PieceManquantes.append('Attestion de présence effective au cfc')
    #             self.PicesManquantesCfc.append('Attestion de présence effective au cfc')
    #             self.PiecesTotale = self.PiecesTotale + 1 

    #     if(self.Fichiers_joint.Bulletin_paie1_cfc):
    #         nbPieces = nbPieces + 1
    #     else:
    #         if(self.Type_paiement == 'CFC'):
    #             state = False
    #             self.PieceManquantes.append('Bulletin de paie 1 cfc')
    #             self.PicesManquantesCfc.append('Bulletin de paie 1 cfc')
    #             self.PiecesTotale = self.PiecesTotale + 1  

    #     if(self.Fichiers_joint.Bulletin_paie2_cfc):
    #         nbPieces = nbPieces + 1
    #         state = True
    #     else:
    #         if(self.Type_paiement == 'CFC'):
    #             state = False
    #             self.PieceManquantes.append('Bulletin de paie 2 cfc')
    #             self.PicesManquantesCfc.append('Bulletin de paie 2 cfc')
    #             self.PiecesTotale = self.PiecesTotale + 1 

    #     if(self.Fichiers_joint.Bulletin_paie3_cfc):
    #         nbPieces = nbPieces + 1
    #         state = True
    #     else:
    #         if(self.Type_paiement == 'CFC'):
    #             state = False
    #             self.PieceManquantes.append('Bulletin de paie 3 cfc')
    #             self.PicesManquantesCfc.append('Bulletin de paie 3 cfc')
    #             self.PiecesTotale = self.PiecesTotale + 1 

    #     if(self.Fichiers_joint.Recu_paiement_frais_dossier):
    #         nbPieces = nbPieces + 1
    #     else:
    #         state = False
    #         self.PieceManquantes.append('Reçu de paiement des fraix de dossier')
    #         self.PiecesTotale = self.PiecesTotale + 1 
            
    #     if(self.Fichiers_joint.Engagement_sur_honneur_occup_pers):
    #         nbPieces = nbPieces + 1
    #         state = True
    #     else:
    #         state = False
    #         self.PieceManquantes.append('Engagement sur honneur')
    #         self.PiecesTotale = self.PiecesTotale + 1 

    #     if(self.Fichiers_joint.Engagement_sur_honneur_payer_apport_perso_cfc):
    #         nbPieces = nbPieces + 1
    #         state = True
    #     else:
    #         if(self.Type_paiement == 'CASH'):
    #             state = False
    #             self.PieceManquantes.append('Engamement su honneur de paiement par apport personnel')
                
    #             self.PiecesTotale = self.PiecesTotale + 1 

    #     if(self.Fichiers_joint.Engagement_sur_honneur_payer_comptant_cfc):
    #         nbPieces = nbPieces + 1
    #     else:
    #         if(self.Type_paiement == 'CFC'):
    #             state = False
    #             self.PieceManquantes.append('Engamement su honneur de paiement CFC')
    #             self.PicesManquantesCfc.append('Engamement su honneur de paiement CFC')
    #             self.PiecesTotale = self.PiecesTotale + 1 

    #     return nbPieces

    def getState(self):
        # if(self.getPieceNumber == self.PiecesTotale):
        #     return 'Complet'
        return  'Incomplet'

    def getTotalPieces(self):
        return self.PiecesTotale


class Conjoint(models.Model):
    Nom_conjoint = models.CharField(max_length=80, null=True, blank = True)
    Prenom_conjoint = models.CharField(max_length=80 , null=True , blank = True)
    Date_naiss_conjoint = models.DateField()
    
    Lieu_naiss_conjoint = models.ForeignKey("Ville", related_name = 'lieunaiss' , on_delete=models.SET_NULL, null = True, blank = True)
    Ville_origine_conjoint = models.ForeignKey("Ville", related_name = 'vc_origine' , on_delete=models.SET_NULL, null = True, blank = True)
    Profession_conjoint = models.ForeignKey("Profession", related_name = 'c_profession' , on_delete=models.SET_NULL, null = True, blank = True)
    Nom_adresse_employeur = models.ForeignKey("Employeur", related_name = 'employeur_conjoint', on_delete=models.CASCADE)
    
    Numero_identite_conjoint = models.IntegerField(null=True, blank = True)
    Numero_compte_bancaire_conjoint = models.IntegerField(null=True, blank = True)
    
    Nom_banque_conjoint = models.ForeignKey("Banque", on_delete=models.SET_NULL, null = True, blank = True)
    Revenu = models.ForeignKey('Revenu_mensuel', on_delete=models.CASCADE)
    demande = models.ForeignKey("Demandeur", related_name = 'demande_conjoint', on_delete=models.CASCADE)
    Cni = models.ImageField(upload_to='Cni_conjoint', blank=True, null=True)

    def __str__(self):
        return '{}  -  {}'.format(self.Nom_conjoint, self.Prenom_conjoint)


class Enfant_legitime(models.Model):
    #Sexe
    MASCULIN = 'M'
    FEMININ = 'F' 
    SEXE_CHOIX = [
        (MASCULIN, 'Homme'),
        (FEMININ, 'Femme'),
    ]
    Nom = models.CharField(max_length=80, null=True, blank = True)
    Prenom = models.CharField(max_length=80 , null=True , blank = True)
    Sexe = models.CharField(max_length=1,  null=True , blank = True, choices=SEXE_CHOIX, default=MASCULIN)
    Date_naiss = models.DateField(null=True , blank = True)
    Lieu_naiss = models.ForeignKey("Ville", related_name = 'lieunaiss_enf' , on_delete=models.SET_NULL, null = True, blank = True)
    Niveau_scolaire_ou_profession = models.CharField(max_length=50 , null=True , blank = True)
    parent = models.ForeignKey("Demandeur", related_name = 'demande_parent', on_delete=models.CASCADE)

    def __str__(self):
        return '{} {}'.format(self.Nom, self.Prenom)

class Engagement_Financier(models.Model): # ok
    Banque = models.ForeignKey("Banque", on_delete=models.SET_NULL, null = True)
    Montant = models.IntegerField(null=False)
    date_de_fin = models.DateField(null=False)
    demande = models.ForeignKey("Demandeur", related_name = 'demande_engagement_financier', on_delete=models.CASCADE)
    
class Revenu_mensuel(models.Model): # ok
    #Nature des revenus
    SALAIRE = 'S'
    AUTRES = 'A'
    NATURE_REVENUS_CHOIX = [
        (SALAIRE, 'Salaire'),
        (AUTRES, 'Autres'),
    ]
    Nature = models.CharField(max_length=1, choices=NATURE_REVENUS_CHOIX, default=SALAIRE, blank = True)
    Montant = models.IntegerField(null=False, blank = True)

    def __str__(self):
        text = '{}  -  {}'.format(self.Nature, self.Montant)
        return text
    
class Engagement_Client(models.Model): #ok
    Type_logement = models.CharField(max_length=80, null=False)
    Prix_vente = models.IntegerField(null=False)
    Depot_garantie_disponible = models.BooleanField(default=True)
    demande = models.ForeignKey("Demandeur", related_name = 'demande_engagement_client', on_delete=models.CASCADE)

   
class Pieces_Jointes(models.Model): #ok
    Demande_logement = models.ImageField(null = True, blank = True,  upload_to='Demande_logement')
    Cni_demandeur = models.ImageField(null = True, blank = True,  upload_to='Cni_demandeur')
    Acte_naissance = models.ImageField(null = True, blank = True,  upload_to='Acte_naissance')
    # Acte_mariage = models.ImageField(null = True, blank = True,  upload_to='Acte_mariage')
    # Acte_deces_conjoint = models.ImageField(null = True, blank = True,  upload_to='Acte_deces_conjoint')
    Certificat_celibat = models.ImageField(null = True, blank = True,  upload_to='Certificat_celibat')
    Attestation_travail = models.ImageField(null = True, blank = True,  upload_to='Attestation_travail')
    Attestation_presence_effective_cfc = models.ImageField(null = True, blank = True,  upload_to='Attestation_presence_effective_cfc')
    Bulletin_paie1_cfc = models.ImageField(null = True, blank = True,  upload_to='Bulletin_paie_cfc')
    Bulletin_paie2_cfc = models.ImageField(null = True, blank = True,  upload_to='Bulletin_paie_cfc')
    Bulletin_paie3_cfc = models.ImageField(null = True, blank = True,  upload_to='Bulletin_paie_cfc')
    Recu_paiement_frais_dossier = models.ImageField(null = True, blank = True,  upload_to='Recu_paiement_frais_dossier')
    Engagement_sur_honneur_occup_pers = models.ImageField(null = True, blank = True,  upload_to='Engagement_sur_honneur_occup_pers')
    Engagement_sur_honneur_payer_apport_perso_cfc = models.ImageField(null = True, blank = True,  upload_to='Engagement_sur_honneur_payer_apport_perso_cfc')
    Engagement_sur_honneur_payer_comptant_cfc = models.ImageField(null = True, blank = True,  upload_to='Engagement_sur_honneur_payer_comptant_cfc')
    demande = models.ForeignKey("Demandeur", related_name = 'demande_pieces_jointes', on_delete=models.CASCADE)


class Decision_comite_attribution(models.Model):  #  perfect
    Demandeur = models.OneToOneField('Demandeur', related_name = "demandeur_decision", on_delete=models.CASCADE, null = True)
    avis_attribution = models.BooleanField('Avis d\'attribution',default=True)
    Numero_logement_attribue = models.OneToOneField('Appartement', on_delete=models.CASCADE, null = True , blank = True)
    Commentaire = models.TextField(null = True, blank = True)
    Pieces = models.ImageField( upload_to='Decision', null = True, blank = True)
    

# last 
class Logement_social(models.Model):
    #Choix Villes possibles
    Ville1 = "Dla"
    Ville2 = 'Yde'
    Ville = [
        (Ville1, 'Douala'),
        (Ville2, 'Yaoundé'),
    ]

    
    #Choix Quartiers Possibles
    Quartier1 = 'Mbanga Bakoko'
    Quartier2 = 'Olembé'
    Quartier = [
        (Quartier1,'Mbanga Bakoko'),
        (Quartier2, 'Olembé'),
    ]
    # help_text=("Choisissez une ville")
    Ville = models.CharField(max_length=20, choices=Ville)
    Quartier = models.CharField(max_length=20, choices=Quartier)





    def get_nombre_immeuble(self):
        nb = 0
        nb = Immeuble.objects.filter(bloc = self.id).count()
        return nb
    
    def __str__(self):
        return self.Ville + " - " + self.Quartier
    def get_full_name(self):
        return self.Ville + " - " + self.Quartier
    

    def get_ocupations(self):
        total = Appartement.objects.filter(immeuble__bloc = self).count()
        occupe = Appartement.objects.filter(immeuble__bloc = self).filter(Vide = False).count()
        percent_total = 100 * total

        if total == 0:
            return 0.0
        else:
            percent = (occupe * 100 ) / total
            percent = str(round(float(percent),2))
          
            # for item in percent:
            #     if item == ',':
            #         item = '.'

            return percent

class Immeuble(models.Model):
    Lettre = models.CharField(max_length=1)
    bloc = models.ForeignKey('Logement_social', null = True, blank = False, on_delete=models.CASCADE )
    def __str__(self):
        log = self.bloc
        return  str(log) + ' - ' + self.Lettre

    def get_num_appartement(self):
        return  Appartement.objects.filter(immeuble_id = self.id).count()
    
    def get_ocupation(self):
        nb = Appartement.objects.filter(immeuble_id = self.id).count()
        appart_occupe = Appartement.objects.filter(immeuble_id = self.id).filter(Vide = False).count()
        

        if nb == 0:
            return 0.0
        else:
            return round(float((appart_occupe * 100 )) / nb,2)
        


class Appartement(models.Model):
    Numero = models.IntegerField( unique=True)
    Descrip_logement = models.TextField()
    immeuble = models.ForeignKey('Immeuble', null = True, blank = False, on_delete=models.CASCADE)
    demandeur = models.ForeignKey('Demandeur', null = True, blank = True, on_delete=models.SET_NULL)
    Vide = models.BooleanField(default = True)
    
    is_empy = True
    def __str__(self):
        return str(self.Numero)

    def get_if_empty(self):
        if self.Vide:
            return True
        return False




class Ville(models.Model):
    Nom_ville = models.CharField(max_length=50)
    def __str__(self):
        return self.Nom_ville

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Ville'
        verbose_name_plural = 'Villes'  
    

class Profession(models.Model):
    Nom_profession = models.CharField(max_length=50)
    def __str__(self):
        return self.Nom_profession

class Banque(models.Model):
    Nom_banque = models.CharField(max_length=50)
    def __str__(self):
        return self.Nom_banque

class Employeur(models.Model):
    Nom_employeur = models.CharField(max_length=50)
    def __str__(self):
            return self.Nom_employeur


class Accord_cfc(models.Model):
    demande = models.OneToOneField("Demandeur", related_name = 'demande', on_delete=models.CASCADE, null = True)
    confirmation_de_conformilte = models.BooleanField()
    commentaire = models.TextField(null = True, blank = True)
    Justificatif = models.ImageField(upload_to='demandeok',null = True, blank = True)

class Utilisateur(AbstractUser):

    role_choices = (
        ('Gestionnaire','Gestionnaire'),
        ('Agent CFC','Agent CFC'),
        ('Supperviseur','Supperviseur'),
        ('Administrateur','Administrateur'),
    )

    role = models.CharField( max_length=50, choices = role_choices)
    # Avatar = models.ImageField(upload_to='avatars', null = True)

