from django.urls import path
from django.contrib.auth.views import LogoutView,PasswordResetDoneView,PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView
from orgSystem import settings as STS
from . import views

urlpatterns = [
    path("account",views.userIn, name="logged"),
    path("login",views.signIn, name="login"),
    path("register",views.signUp, name="signUp"),
    #path("reset",views.resetPassword,name="reset"),
    path("logout",LogoutView.as_view(next_page=STS.LOGOUT_REDIRECT_URL), name="logout"),
    path("",views.nothingToShow, name="404"),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_sent/',PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_complete',PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
