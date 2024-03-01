from email import message
from django.utils import timezone
from django.http import Http404, HttpResponse
from Litomici_memeber_system.settings import EMAIL_HOST_USER
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
from Litomici_memeber_system import messages as MSG
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
                    messages.success(request,MSG.contacUsSuccess)
                except Exception as e:
                    messages.error(request,MSG.contactUsSendFail)
                    form = EmailForm()
                    return render(request, 'tags/mains/contacts.html', {'form': form,"done":1,'role':account.position,})
                return HttpResponseRedirect('sendMsg')
            else:
                errs=form.errors.items()
                messages.error(request,MSG.contactUsFailValid(errs))
                form = EmailForm()
                return render(request, 'tags/mains/contacts.html', {'form': form,"done":2,'role':account.position,})    
        else:
            form = EmailForm()
        return render(request, 'tags/mains/contacts.html', {'form': form,"done":3,'role':account.position,})
    else:
        messages.error(request,MSG.timeOut)
        return redirect("account:login")
#member operations
def showMembers(request):
    if isUserLoggedWithPermission(request,1):
        account = getUsersAccount(request)
        allMembers=member.objects.all()
        member2pass=[]
        for m in allMembers:
            if Account.objects.filter(member=m).first():
                
                member2pass.append(
                    {
                        "name":f"{m.jmeno} {m.surname}",
                        "born":m.birthday,
                        "phone":Account.objects.filter(member=m).first().mobile1,
                        "id":m
                    })
            else:
                member2pass.append(
                    {
                        "name":f"{m.jmeno} {m.surname}",
                        "born":m.birthday,
                        "phone": "není uvedeno",
                        "id":m
                    })
        dic={
            "role": account.position,#0=user;1=leader;2=econom;3=admin
            "members":member2pass
        }
        
        return render(request,"tags/mains/allMembers.html",dic)
    else:
        if isUserLogged(request):
            messages.error(request, MSG.permDenied)
        else:
            messages.error(request,MSG.timeOut)
        return redirect("account:login")
def memberDetail(request,member_id):
    if isUserLoggedWithPermission(request,1):
        print(member_id)
        return HttpResponse()
    else:
        if isUserLogged(request):
            messages.error(request, MSG.permDenied)
        else:
            messages.error(request,MSG.timeOut)
        return userIn(request)
    return
def removeMember(request):
    if isUserLogged(request):
        account = getUsersAccount(request)
        membersInAccount = account.members.all()

        if request.method == 'POST':
            selected_member_id = request.POST.get('member_id')
            if selected_member_id:
                selected_member = member.objects.get(pk=selected_member_id)
                if selected_member.ATOM_id == (request.POST.get("Atom")):
                    account.members.remove(selected_member)
                    account.save()
                    messages.success(request,MSG.memberRemovedSuccess)
                    return redirect('account:profile')  # Redirect to the member list view or another appropriate view
                else:
                    messages.error(request,MSG.memberRemovedFail)
                    context = {
                    'available_members': membersInAccount,
                    'role':account.position,
                    }
                    return render(request, 'tags/mains/removeMember.html', context)
            else:
                messages.error(request,MSG.memberRemovedNoSelect)
        context = {
            'available_members': membersInAccount,
            'role':account.position,
        }
        return render(request, 'tags/mains/removeMember.html', context)
    else:
        messages.error(request,MSG.timeOut)
        return redirect('account:login')
def add_member_to_account(request):
    if isUserLogged(request):
 # Get the currently logged-in account
        account = getUsersAccount(request)
    # Get members associated with the current account
        members_in_account = account.members.all()
    # Get all members and find those not in the current account
        all_members = member.objects.all()
        aviable_members = all_members.exclude(pk__in=members_in_account)
        if request.method == 'POST':
            selected_member_id = request.POST.get('member_id')
            if selected_member_id:
                selected_member = member.objects.get(pk=selected_member_id)
                born_date = request.POST.get('born')
                print("input "+born_date)
                print(selected_member.birthday)
                if selected_member.birthday.__str__() == born_date:
                    print("Match")
                    account.members.add(selected_member)
                    account.save()
                    messages.success(request,MSG.addMemberSuccess)
                    return redirect('account:profile')  # Redirect to the member list view or another appropriate view
                else:
                    print("nomatch")
                    # messages.error(request,MSG.timeOut)
                    messages.error(request,MSG.addMemberFail)                
            else:
                print("fail")
                messages.error(request,MSG.addMemberFail)
        context = {
            'available_members': aviable_members,
            'role':account.position,
        }
        return render(request, 'tags/mains/addMember.html', context)
    else: 
        messages.error(request,MSG.timeOut)
        return redirect('account:login')
def newMember(request):
    if isUserLogged(request):
        account = getUsersAccount(request)
        if request.method == 'POST':
            form = NewMemeberForm(request.POST)
            print(form.errors.as_text())
            if form.is_valid():
                newMember=form.save()
                request.user.account.members.add(newMember)
                if not membersAtomCheck():
                    account = getUsersAccount(request)
                    account.wallet+=(-1200)
                messages.success(request, MSG.createMemberSuccess)
                return redirect('account:profile')  # Replace 'success_page' with the desired success page name or URL
            else:
                messages.error(request, MSG.newMemberValidFail(form.errors.items()))
                form = NewMemeberForm()
                return render(request, 'tags/mains/newMember.html', {'form': form,"role":account.position})
        else:
            form = NewMemeberForm() 
        return render(request, 'tags/mains/newMember.html', {'form': form,"role":account.position})
    else:
        messages.error(request,MSG.timeOut)
        return redirect("account:login")    
#Creating account
def signUp(request):#prvni krok registrace
    if request.user.is_authenticated and not has_account(request.user):
        messages.success(request,MSG.regStep1Success)
        return redirect('account:newAccount')  # Change 'next_step_registration' to your actual URL
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
                messages.success(request,MSG.regStep1Success)
                return redirect('account:newAccount')  # Change 'next_step_registration' to your actual URL
            else:
                messages.error(request,MSG.regStep1PostValidFail)
        else:
            messages.error(request,MSG.newMemberValidFail(form.errors.items()))
            form=UserRegistrationForm()
            return render(request, "tags/mains/registerUser.html", {'form': form})
    else:
        form = UserRegistrationForm()       
    # labels settup
        form.fields['password2'].help_text = ''
        form.fields['username'].help_text = ''
        form.fields['password1'].label = 'Heslo'
        form.fields['password1'].help_text = 'Heslo musí mít alespoň 8 znaků\n Musí mít písmeno i číslo\nNesmí nesmí být již používané'
        form.fields['password2'].label = 'Potvrzení Hesla'
    return render(request, "tags/mains/registerUser.html", {'form': form})
def NewAccount(request):#druhý krok registrace
    
    if not request.user.is_authenticated:#přihlášení už je propadlé
        messages.error(request,MSG.timeOut)
        return redirect("account:login")
    if has_account(request.user):#uživatel je přihlášen 
        return HttpResponseRedirect("logged")
    if request.method == "POST":
        form = NewAccountForm(request.POST)
        tmp=form.is_valid()
        if form.is_valid():
            tmpr = form.save()#commit=False
            tmpr.user = request.user  # Assign the logged-in user
            tmpr.users.add(request.user)
            tmpr.save()
            if tmp is not None:
                messages.success(request,MSG.regStep2Success)
                # Redirect to the next step of registration (adjust the URL accordingly)
                return HttpResponseRedirect("account")
            else:
                form = NewAccountForm(initial={'user': request.user})
                messages.error(request,MSG.regStep2PostValidFail)
                return render(request, "tags/mains/accountRegister.html", {'form': form,"username":request.user.username})
        else:
            messages.error(request,MSG.newMemberValidFail(form.errors.items()))
            form = NewAccountForm(initial={'user': request.user})
            return render(request, "tags/mains/accountRegister.html", {'form': form,"username":request.user.username})
    else:
        form = NewAccountForm(initial={'user': request.user})
        return render(request, "tags/mains/accountRegister.html", {'form': form,"username":request.user.username})
    
def addUserToAccount(request):
    if isUserLogged(request):
        account = getUsersAccount(request)
        if request.method == 'POST':
            form = AddUserForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['newUserEmail']
                if not is_username_available(email):
                    form = AddUserForm()
                    messages.error(request,MSG.addUserAllrdyUsed(email))
                    return render(request, 'tags/mains/userInvite.html', {'form': form,'role':account.position,})
            # Generate and send confirmation link
                try:
                    email_confirmation = EmailConfirmation.create(email=email,sender=request.user.username)
                    print("povedlo se")
                    email_confirmation.send_confirmation_email()
                    print("povedlo se 2")
                    messages.error(request,MSG.addUserSuccess(email))
                    return render(request, 'tags/mains/userInvite.html', {'form': form,'role':account.position,})
                except Exception as e:
                    form = AddUserForm()
                    print("Exception:", e)
                    messages.error(request,MSG.addUserfail(email))
                    return render(request, 'tags/mains/userInvite.html', {'form': form,'role':account.position,})
        else:            
            form = AddUserForm()      
            return render(request, 'tags/mains/userInvite.html', {'form': form,'role':account.position,})
    else:
        messages.error(request,MSG.timeOut)
        return ('account:login')
def invitedUser(request, token):
    email_confirmation = get_object_or_404(EmailConfirmation, token=token)
    sender=token.split("=>")[0]
    user= User.objects.get(username=sender)
    account= getAccountByUser(user)
    #kontrola expirace
    time_difference = timezone.now() - email_confirmation.created_at
    if time_difference.total_seconds() > 1800:  # 600 seconds = 10 minutes=>1800s=30min
        # Link has expired, delete the instance and raise Http404
        email_confirmation.delete()
        raise Http404(MSG.linkExpired)
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
                messages.success(request, MSG.addNewUserSuccess)
                email_confirmation.delete()  # Remove the email confirmation record
                return redirect('account:login')  # Redirect to login page or wherever you want
            else:
                messages.error(request,MSG.addNewUserPassFail)
        else:
            messages.error(request,MSG.newMemberValidFail(form.errors.items()))
    else:
        form = SetPasswordForm()

    return render(request, 'tags/mains/invitedUserPassword.html', {'form': form, 'email': email})
# Logging
def userIn(request):
    if request.user.is_authenticated and not has_account(request.user):
                messages.success(request,MSG.regStep1Success)
                return redirect('account:newAccount')  # Change 'next_step_registration' to your actual URL
    if isUserLogged(request):
        account = getUsersAccount(request)
        dic={
            "role": account.position,#0=user;1=leader;2=econom;3=admin
            "email": request.user.username,
            "lastlog":request.user.last_login,
        }    
        return render(request,"tags/mains/welcomeUserScreen.html",dic)
    messages.success(request,MSG.timeOut)
    return render(request,"index.html")
def signIn(request):
    if isUserLogged(request):
        return redirect("account:logged")
    if request.user.is_authenticated and not has_account(request.user):
                messages.success(request,MSG.regStep1Success)
                return redirect('account:newAccount')  # Change 'next_step_registration' to your actual URL
    if request.method=="POST":
        uname = request.POST.get("mail")
        passwd = request.POST.get("pass")
        user = authenticate(username=uname,password=passwd)
        if user is not None:
            login(request,user)
            if request.user.is_authenticated and not has_account(request.user):
                messages.success(request,MSG.regStep1Success)
                return redirect('account:newAccount')  # Change 'next_step_registration' to your actual URL
            return redirect("account:logged")
        else:
            messages.error(request,MSG.loginFail)
            return redirect("account:login")
    return render(request, "index.html")
def sign_out(request):
    logout(request)
    messages.success(request,MSG.logOut)
    return signIn(request)
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
        members=account.members.all()
        if members:
            dic["members"]=members
        return render(request,"tags/mains/profile.html",dic)
    messages.error(request,MSG.timeOut)
    return redirect("account:login")
def changeData(request):
    if isUserLogged(request):
        account = getUsersAccount(request)
        if request.method == 'POST':
            form = changeDataForm(request.POST)
            if form.is_valid():
                state1 = form.cleaned_data["state1"]
                state2=form.cleaned_data["state2"]
                account.mobile1 = form.cleaned_data['mobile1']
                account.mobile2 = form.cleaned_data['mobile2']
                account.addres1=form.cleaned_data['addres1']
                account.addres2=form.cleaned_data['addres2']
                account.psc1=form.cleaned_data['psc1']
                account.psc2=form.cleaned_data['psc2']
               
                
                if state1 !="Česko":
                    tmp=form.cleaned_data['city1']+"("+state1+")"
                    account.city1=tmp
                else:
                    account.city1=form.cleaned_data['city1']
                if state2 !="Česko":
                    tmp=form.cleaned_data['city2']+"("+state2+")"
                    account.city2=tmp
                else:
                    account.city2=form.cleaned_data['city2']
                account.city2=form.cleaned_data['city2']
                account.mobile1
                account.save()
                messages.success(request,MSG.dataChangeSuccess)
                return redirect("account:profile")
            else:
                messages.error(request,MSG.newMemberValidFail(form.errors.items()))
        form = changeDataForm()
        form.fields['mobile1'].initial=account.mobile1
        form.fields['mobile2'].initial=account.mobile2
        form.fields['city1'].initial=account.city1
        form.fields['city2'].initial=account.city2
        form.fields['psc1'].initial=account.psc1
        form.fields['psc2'].initial=account.psc2
        form.fields['addres1'].initial=account.addres1
        form.fields['addres2'].initial=account.addres2
        dic={
        "role": account.position,#0=user;1=leader;2=econom;3=admin
        "form": form,
    }
        return render(request,"tags/mains/accountDataChange.html",dic)   
    else:
        messages.error(request,MSG.timeOut)
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