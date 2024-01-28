from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView,PasswordResetDoneView,PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView
from Litomici_memeber_system import settings as STS

app_name = 'account'
urlpatterns = [
    #sending an email
    path("sendMsg",views.sendMessage,name="sendMSG"),#simple message from user
    path("AddNewUser",views.addUserToAccount,name="addNewUser"),#adding new user to account # type: ignore
    path("setPassword/<str:token>/",views.invitedUser,name="setPasswd"),
    #account operations
    path("account",views.userIn, name="logged"),
    path("profileInfo",views.userData, name="profile"),
    path("removeMember",views.removeMember,name="removeMemeber"),
    path("addMember",views.add_member_to_account,name="addMember"),
    #creating new entity
    path("register",views.signUp, name="signUp"),
    path('newAccount',views.NewAccount, name='newAccount'),
    path("addEvent",views.userData, name="addEvent"),
    path("createMemeber",views.newMember,name="newMember"),
    #loging
    path("login",views.signIn, name="login"),
    path("logout",LogoutView.as_view(next_page=STS.LOGOUT_REDIRECT_URL), name="logout"),
    #password reset 
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_sent/',PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm '),
    path('reset_complete',PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    #errors
    path("",views.signIn, name="404"),
    #development only 
    # path("test",views.tester,name="test"),
    # path("testF",views.testF,name="testF"),
    

]
