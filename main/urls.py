from django.urls import path
from . import views


from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", views.index, name="index"),
    path('home/', views.home, name = 'home'),
    path('Ajouter_un_demandeur',views.formdemandeur, name='demandeur_add'),
    path('Demandeur/<demandeur_id>', views.ViewDemandeur, name = 'ViewDemandeur'),
    path('DeleteDemandeur/<demandeur_id>', views.DeleteDemandeur, name = 'deletedemandeur'),
    path('ModifierDemandeur/<demandeur_id>', views.updateDemandeur, name = 'updateDemandeur'),
    path('DemandeurResults', views.DemandeurResults, name = 'DemandeurResults'),
    path('confirmation_de_suppression/<demandeur_id>', views.VerifyeDeleting, name = "confirmer_suppression"), 

    path('Appartement',views.Appartements, name  = "Appartement"),
    path('DeleteAppartement/<appartent_id>',views.DeleteAppartement, name  = "DeleteAppartement"),
    path('EditApparatement/<appartent_id>',views.EditApparatement, name  = "EditApparatement"),

    path('Immeubles',views.Immeubles, name  = "Immeuble"),
    path('DeleteImmeuble/<immeuble_id>',views.DeleteImmeuble, name  = "DeleteImmeuble"),
    path('EditImmeuble/<immeuble_id>',views.EditImmeuble, name  = "EditImmeuble"),


    path('Logements',views.Logements, name  = "Logement"),
    path('DeleteLogement/<logement_id>',views.DeleteLogement, name  = "DeleteLogement"),
    path('EditLogement/<logement_id>',views.EditLogement, name  = "EditLogement"),
    path("Logements_details/<logement_id>", views.Logements_details, name="Logements_details"),
    

    path('Decision',views.Decision, name  = "Decision"),
    path("Decision_add/", views.Decision_add, name="Decision_add"),
    path('DeleteDecision/<Decision_id>',views.DeleteDecision, name  = "DeleteDecision"),
    path('EditDecision/<Decision_id>',views.EditDecision, name  = "EditDecision"),
    path("decision_form/", views.decision_form, name="decision_form"),
    path("get_appart/<id>", views.get_appart, name="get_appart"),
    path("get_demandeur/<id>", views.get_demandeur, name="get_demandeur"),
    
    path('Download_demandeur_pdf/<demandeur_id>', views.Download_demandeur_pdf, name = 'Download_demandeur_pdf'),
    path('addVille', views.addVille, name = 'addVille'),
    path('addprofession', views.addprofession, name = 'addprofession'),
    path('addbanque', views.addbanque, name = 'addbanque'),
    path('addempoyeur', views.addempoyeur, name = 'addempoyeur'),

    path('demandeurPdf/<demandeur_slug>', views.demandeurPdf, name = "generer"),

    path("dash", views.dash, name="dash"),


    path('profile', views.profile, name = 'profile'),
    path("get_immeuble/<id>", views.get_immeuble, name="get_immeuble"),

    # Gestion des mot de passes

    path("reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
