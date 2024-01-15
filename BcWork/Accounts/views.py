from email import message
from django.utils import timezone
from django.http import Http404
import Litomici_memeber_system
from .forms import EmailForm
from django.shortcuts import render
from django.shortcuts import redirect, render,get_object_or_404
from django.http import HttpResponseRedirect,request
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from Litomici_memeber_system import settings
from .models import Account,EmailConfirmation
from datetime import datetime
from .forms import *
from .tools import *
# from Events.forms import EventForm
# from Events.models import *
#send message
def sendMessage(request):
    if isUserLogged(request):
        account = getUsersAccount(request)
        if request.method == 'POST':
            form = EmailForm(request.POST)
            if form.is_valid():
                subject = form.cleaned_data['subject']
                text = form.cleaned_data['text']
                text= "dne "+ datetime.now().strftime("%d.%m.%Y %H:%M")+"\n"+text+"\n"+request.user.username
                print(subject+" "+text)
               # Change the email settings as per your configuration
                # recipient_email = settings.EMAIL_HOST_USER
                # sender_email = settings.EMAIL_HOST_USER
                try:            
                    send_mail(
                        subject,
                        text,
                        request.user.username,
                        ['turistaklitomici@gmail.com'],
                        fail_silently=False,
                    )
                
                    # Redirect after successful form submission
                    messages.error(request,"Úspěšně jste odeslali zprávu")
                except Exception as e:
                    messages.error(request,"selhalo odesílání")
                    form = EmailForm()
                    return render(request, 'tags/mains/contacts.html', {'form': form,"done":1,'role':account.position,})
                return HttpResponseRedirect('sendMsg')
            else:
                form = EmailForm()
                messages.error(request,"nepodařilo se odeslat zprávu")
                return render(request, 'tags/mains/contacts.html', {'form': form,"done":2,'role':account.position,})    
        else:
            form = EmailForm()
        return render(request, 'tags/mains/contacts.html', {'form': form,"done":3,'role':account.position,})
    else:
        messages.error(request,"Platnost přihlášení vypršela")
        return redirect("account:login")
#member operations
def removeMember(request):
    if isUserLogged(request):
        account = getUsersAccount(request)
        membersInAccount = account.member.all()

        if request.method == 'POST':
            selected_member_id = request.POST.get('member_id')
            if selected_member_id:
                selected_member = member.objects.get(pk=selected_member_id)
                if selected_member.ATOM_id == (request.POST.get("Atom")):
                    account.member.remove(selected_member)
                    account.save()
                    return redirect('account:profile')  # Redirect to the member list view or another appropriate view
                else:
                    messages.error(request,"Nesprávný osobní kód")
                    context = {
                    'available_members': membersInAccount,
                    'role':account.position,
                    }
                    return render(request, 'tags/mains/removeMember.html', context)
        context = {
            'available_members': membersInAccount,
            'role':account.position,
        }
        return render(request, 'tags/mains/removeMember.html', context)
    else:
        return redirect('account:login')
def add_member_to_account(request):
    if isUserLogged(request):
 # Get the currently logged-in account
        account = getUsersAccount(request)

    # Get members associated with the current account
        members_in_account = account.member.all()
    
    # Get all members and find those not in the current account
        all_members = member.objects.all()
        aviable_members = all_members.exclude(pk__in=members_in_account)
        if request.method == 'POST':
            selected_member_id = request.POST.get('member_id')
            if selected_member_id:
                selected_member = member.objects.get(pk=selected_member_id)
                account.member.add(selected_member)
                account.save()
                return redirect('account:profile')  # Redirect to the member list view or another appropriate view
    
        context = {
            'available_members': aviable_members,
            'role':account.position,
        }
        return render(request, 'test.html', context)
    else: return redirect('account:login')
def newMember(request):
    if isUserLogged:
        if request.method == 'POST':
            form = NewMemeberForm(request.POST)
            print(form.errors.as_text())
            if form.is_valid():
                newMember=form.save()
                request.user.account.member.add(newMember)
                if not membersAtomCheck():
                    account = getUsersAccount(request)
                    account.wallet+=(-1200)
                messages.success(request, 'Člen byl úspěšny vytvořen a přidán k vašemu účtu')
                return redirect('account:profile')  # Replace 'success_page' with the desired success page name or URL
            else:
                messages.error(request, 'Člena se nepodařilo vytvořit.\n'+form.errors.as_text())
                form = NewMemeberForm()
                return render(request, 'tags/mains/newMember.html', {'form': form,"role":request.user.account.position})
        else:
            form = NewMemeberForm()
        return render(request, 'tags/mains/newMember.html', {'form': form,"role":request.user.account.position})
    else:
        return redirect("account:login")    
#Creating account
def signUp(request):#prvni krok registrace
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log in the user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to the next step of registration (adjust the URL accordingly)
                messages.success(request,"První krok Registrace byl úspěšný")
                return redirect('account:newAccount')  # Change 'next_step_registration' to your actual URL
        else:
            messages.error(request,"email není platný nebo se zadaná hesla neshodují")
            form=UserRegistrationForm()
            return render(request, "tags/mains/registerUser.html", {'form': form})
    else:
        form = UserRegistrationForm()       
    # Modify labels in the form
        form.fields['password2'].help_text = ''
        form.fields['username'].help_text = ''
        form.fields['password1'].label = 'Heslo'
        form.fields['password1'].help_text = 'Heslo musí mít alespoň 8 znaků\n Musí mít písmeno i číslo\nNesmí nesmí být již používané'
        form.fields['password2'].label = 'Potvrzení Hesla'
    return render(request, "tags/mains/registerUser.html", {'form': form})
def NewAccount(request):#druhý krok registrace
    if has_account(request.user):
        return HttpResponseRedirect("logged")
    if not request.user.is_authenticated:
        messages.success(request,"Přihlášení vypršelo. Přihlas se znovu.")
        return redirect("account:login")
    if request.method == "POST":
        form = NewAccountForm(request.POST)
        if form.is_valid():
            tmp = form.save(commit=False)
            tmp.user = request.user  # Assign the logged-in user
            tmp.users=[request.user]
            tmp.save()
            if tmp is not None:
                # Redirect to the next step of registration (adjust the URL accordingly)
                return HttpResponseRedirect("account")
            else:
                form = NewAccountForm()
                messages.success(request,"Účet se nepodařilo vytvořit. Zkus to prosím znovu")
                return render(request, "tags/mains/accountRegister.html", {'form': form})
        else:
            form = NewAccountForm()
            messages.success(request,"Údaje byly nesprávně vyplněny nebo vyplnění obsah obsahoval potentionálně nebezpečný obsah. Zkontroluj si své údaje zkus to prosím znovu")
            return render(request, "tags/mains/accountRegister.html", {'form': form})
    else:
        form = NewAccountForm()
        return render(request, "tags/mains/accountRegister.html", {'form': form})
    
def addUserToAccount(request):
    if isUserLogged(request):
        account = getUsersAccount(request)
        if request.method == 'POST':
            form = AddUserForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['newUserEmail']
                if not is_username_available(email):
                    form = AddUserForm()
                    messages.error(request,"Uživatel s emailem "+email+" již existuje a má svůj vlastní účet\n Zkontrolujte adresu zkuste to znovu.\n Nebojte se nás v případě potřeby kontaktovat.")
                    return render(request, 'tags/mains/userInvite.html', {'form': form,'role':account.position,})
            # Generate and send confirmation link
                try:
                    email_confirmation = EmailConfirmation.create(email=email,sender=request.user.username)
                    email_confirmation.send_confirmation_email()
                    messages.error(request,"Úspěšně jste odeslali pozvánku na email "+email)
                    return render(request, 'tags/mains/userInvite.html', {'form': form,'role':account.position,})
                except:
                    form = AddUserForm()
                    messages.error(request,"Nepodařilo se odeslat pozvánku na email "+email+"\nZkontrolujte adresu zkuste to znovu.")
                    return render(request, 'tags/mains/userInvite.html', {'form': form,'role':account.position,})
        else:            
            form = AddUserForm()      
            return render(request, 'tags/mains/userInvite.html', {'form': form,'role':account.position,})
    else:
        messages.error(request,"Platnost přihlášení vypršela")
        return ('account:login')
def invitedUser(request, token):
    email_confirmation = get_object_or_404(EmailConfirmation, token=token)
    sender=token.split("=>")[0]
    user= User.objects.get(username=sender)
    account= getUsersAccount(request)
    #kontrola expirace
    time_difference = timezone.now() - email_confirmation.created_at
    if time_difference.total_seconds() > 600:  # 600 seconds = 10 minutes
        # Link has expired, delete the instance and raise Http404
        email_confirmation.delete()
        raise Http404("Životnost odkazu vypršela.")
    email = email_confirmation.email
    #dokončení registrace
    if request.method == 'POST':
        form = SetPasswordForm(request.POST)
        if form.is_valid():
            pass1=form.cleaned_data['password1']
            pass2=form.cleaned_data['password2']
            if pass1==pass2:
                usr=User.objects.create_user(username=email, password=pass1)
                usr.save()
                account.users.add(usr)
                messages.success(request, 'Účet byl úspěšně vytvořen. Nyní se prosím přihlaš.')
                email_confirmation.delete()  # Remove the email confirmation record
                return redirect('account:login')  # Redirect to login page or wherever you want
    else:
        form = SetPasswordForm()

    return render(request, 'tags/mains/invitedUserPassword.html', {'form': form, 'email': email})
# Logging
def userIn(request):
    if isUserLogged(request):
        account = getUsersAccount(request)
        dic={
            "role": account.position,#0=user;1=leader;2=econom;3=admin
            "email": request.user.username,
            "lastlog":request.user.last_login,
        }    
        return render(request,"tags/mains/welcomeUserScreen.html",dic)
    messages.success(request,"Přihlášení vypršelo. Přihlas se znovu.")
    return render(request,"index.html")
def signIn(request):
    if isUserLogged(request):
        return redirect("account:logged")
    if request.method=="POST":
        uname = request.POST.get("mail")
        passwd = request.POST.get("pass")
        user = authenticate(username=uname,password=passwd)
        if user is not None:
            login(request,user)
            return redirect("account:logged")
        else:
            messages.error(request,"Špatná emailová adresa nebo heslo")
            return redirect("account:login")
    return render(request, "index.html")
def sign_out(request):
    logout(request)
    messages.success(request,"Uživatel byl úspěšně odlhlášen")
# account data
def userData(request):
    dic={
        
        "secondaryContact": False,
        "addr1": "",
        "mobile1": "",
        "mail": "",
        "addr2":"",
        "mobile2": "",
        "members": "",
        "wallet":"",  
    }
    if isUserLogged(request):
        account = getUsersAccount(request)
        usernames = account.users.values_list('username', flat=True)
        usernamesSTR = ', '.join(usernames)
        dic={
            "role": account.position,#0=user;1=leader;2=econom;3=admin
            "mail":usernamesSTR,
            "addr1": account.addres1 + ", "+account.city1 + " " +account.psc1,
            "mobile1": add_spaces(account.mobile1),
            "wallet":account.wallet,
            "lastlog":request.user.last_login,
        }
        if account.addres2 == "" or account.psc2 == "" or account.city2 == "":
            dic["secondaryContact"]=False
        else:
            dic["secondaryContact"]=True
            dic["addr2"]= account.addres2 + ", "+account.city2 + " " +account.psc2,
        if account.mobile2 is not None:
            dic["mobile2"]=add_spaces(account.mobile2)
        members=account.member.all
        if members:
            dic["members"]=members
        return render(request,"tags/mains/profile.html",dic)
    messages.success(request,"Přihlášení vypršelo. Přihlas se znovu.")
    return redirect("account:login")
def nothingToShow(request):
    return render(request,"blindPath.html")
# def tester(request):
#     tmp=membersAtomCheck()
#     return render(request,"tags/mains/welcomeUserScreen.html",{"email":tmp})
# def test2(request):
#     return render(request,"tags/content.html")
# def testF(request):
    return redirect("testF")