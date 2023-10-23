from django.shortcuts import render
from django.shortcuts import redirect, render
from django.http import HttpResponse,request
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from orgSystem import settings
from .models import Account
from datetime import datetime
# Create your views here.
def userIn(request):
    if request.user.is_authenticated:
        account = Account.objects.get(user=request.user)
        dic={
            "role": account.position,#0=user;1=leader;2=econom;3=admin
            "fname": request.user.first_name,
            "lname": request.user.last_name,
            "email": request.user.email,
            "lastlog":request.user.last_login,
            "kid1": account.kid1,
            "kid2": account.kid2,
            "kid3": account.kid3,
            "kid4": account.kid4,
    }    
        return render(request,"account.html",dic)
    messages.success(request,"uživateli doba pro přihlášení vypršela. Přihlas se znovu.")
    return render(request,"index.html")
def signIn(request):
    if request.method=="POST":
        uname = request.POST.get("mail")
        passwd = request.POST.get("pass")
        user = authenticate(username=uname,password=passwd)
        if user is not None:
            login(request,user)
            return userIn(request)
        else:
            messages.error(request,"Špatný email nebo heslo")
            return redirect("login")
    return render(request, "index.html")
def sign_out(request):
    logout(request)
    messages.success(request,"You has been successfully logged out")
    return redirect(request,"index.html")
def signUp(request):
        ## vytezovani requestu
    if request.method == "POST":
        username = request.POST.get("mail")
        # Optional -> username = request.POST["username"]
        fname = request.POST.get("name")
        lname = request.POST.get("surname")
        email = request.POST.get("mail")
        pass1 = request.POST.get("pass")
        pass2 = request.POST.get("pass")
        
        ## Podminky pro uspesne vytvoreni uctu
        if User.objects.filter(username=username):# ID User = email
            messages.error(request, "Tento email již někdo používá! Zkuste jiný nebo nás kontaktujte")
            return redirect('signUp')
        if pass1 != pass2: # Hesla se shodují
            messages.error(request, "Hesla se neshodují!! Zkuste to znovu")
            return redirect('signUp')
        if not ("@" in username and "." in username): # ověření, že je to email
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('signUp')
        ## vytvareni zapis do databaze
        my_user = User.objects.create_user(username,email,pass1)
        my_user.first_name=fname
        my_user.last_name=lname
        my_user.save()
        user_extension = Account(user=my_user)
        user_extension.save()
        messages.success(request,"Váš účet byl úspěšně založen")
        # ## Welcome Email
        # subject = "Registrace do Litomíků proběhla úspěšně"
        # message = ""
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [my_user.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=True)
        return redirect("login")
    return render(request,"register.html")
def resetPassword(request):
    return render(request,"resetPass.html")
def nothingToShow(request):
    return render(request,"blindPath.html")

