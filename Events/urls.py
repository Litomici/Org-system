from django.urls import path,include
from . import views
from django.contrib.auth.views import LogoutView,PasswordResetDoneView,PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView



urlpatterns = [
    path("create",views.create,name="create"),
    path("listAll/<int:event_id>/",views.listAll,name="listAll_id_add"),
    path("listAll",views.listAll,name="listAll"),
    path('details/<int:event_id>/',views.details,name="details"),
    path("listCamps",views.listCamps,name="listCamps"),
    path("eventTool",views.eventActions,name="tool"),
]
