from django.urls import path
from . import views

urlpatterns = [
    path("list", views.index, name="users"),
    path("form/", views.add_form, name="user_form"),
    path('upadate/<user_id>', views.user_mod, name = 'user_update'),
    path('confirmation/<user_id>', views.user_confirm_delation, name = 'confirm_delete'),
    path('delete_user/<user_id>', views.delete_user, name = 'delete_user'),

]
