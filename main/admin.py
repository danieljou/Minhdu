from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(Demandeur)
admin.site.register(Ville)
admin.site.register(Decision_comite_attribution)
admin.site.register(Appartement)