from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView,PasswordResetDoneView,PasswordResetView,PasswordResetCompleteView,PasswordResetConfirmView
from Litomici_memeber_system import settings as STS

app_name = 'account'
urlpatterns = [
    #administration
    path("ShowMembers&Accounts",views.showMembers, name="showMembers"), # type: ignore
    path("MemberDetail/<str:member_id>",views.memberDetail,name="memberDetail"), # type: ignore
    path("Payment",views.seeMoney,name="payment"),
    path("Economy",views.unpayed_payments,name="economy"),
    path("BankTransactions",views.bank_transactions,name="bankTransactions"),
    path("Payed",views.payed_payments,name="payed"),
    path("Payments",views.payments,name="payments"),
    path("Notify2pay/<str:account_id>",views.notify2pay,name="notify2pay"),
    path("AddMoney2pay/<str:account_id>",views.addMoney2pay,name="need2pay"),
    path("ManualPayment",views.manual_payment,name="manualP"),
    #sending an email
    path("SendMsg",views.sendMessage,name="sendMSG"),#simple message from user
    path("AddNewUser",views.addUserToAccount,name="addNewUser"),#adding new user to account # type: ignore
    path("SetPassword/<str:token>/",views.invitedUser,name="setPasswd"),
    #account operations
    path("Account",views.userIn, name="logged"),
    path("ProfileInfo",views.userData, name="profile"),
    path("RemoveMember",views.removeMember,name="removeMemeber"),
    path("AddMember",views.add_member_to_account,name="addMember"),
    path("ChangeData", views.changeData, name="changeData"),
    #creating new entity
    path("Register",views.signUp, name="signUp"),
    path('NewAccount',views.NewAccount, name='newAccount'),
    path("AddEvent",views.userData, name="addEvent"),
    path("CreateMemeber",views.newMember,name="newMember"),
    #loging
    path("Login",views.signIn, name="login"),
    path("Logout",LogoutView.as_view(next_page=STS.LOGOUT_REDIRECT_URL), name="logout"),
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
