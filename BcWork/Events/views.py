from math import e
from Litomici_memeber_system.settings import EMAIL_HOST
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render,redirect
from .models import Event
from Accounts.models import *
from Accounts.tools import *
from.forms import *
from django.contrib import messages
from django.db.models import F
from datetime import timedelta
from Litomici_memeber_system import messages as MSG
def eventActions(request):
    if isUserLoggedWithPermission(request,1):
        dic={
            "role": getUsersAccount(request).position,
            "eventAction":0,
        }
        return render(request, "tags/mains/eventAction.html", dic)
    else:
        if isUserLogged(request):
            messages.error(request, MSG.permDenied)
        else:
            messages.error(request,MSG.timeOut)
        return HttpResponseRedirect(reverse('account:logged'))  
def eventActionEdit(request):
    if isUserLoggedWithPermission(request,1):
         
        if request.method == "POST":
            form = EventEditForm(request.POST)
            request.POST.get('eventId')
            
            if form.is_valid():
                tmp = get_object_or_404(Event, id=int(request.POST.get('eventId')))
                for field_name in [field.name for field in Event._meta.fields]:
                        form_field_name = field_name
                        if form_field_name=='id_organizedBy':
                            continue
                        elif form_field_name=='ending':
                            form_value = form.cleaned_data.get(form_field_name)
                            if not form_value:
                                meeting_value=form.cleaned_data.get("meeting")
                                ending_value = meeting_value + timedelta(hours=2)
                                tmp.ending = ending_value
                        elif form_field_name in form.cleaned_data:
                            form_value = form.cleaned_data.get(form_field_name)
                            if getattr(tmp, field_name) != form_value:
                                setattr(tmp, field_name, form_value)
                tmp.save()
                form =EventEditForm()
                for field_name, field in form.fields.items():
                    if field_name != 'csrfmiddlewaretoken':
                        form.fields[field_name].widget.attrs['readonly'] = True
                    dic={
                    "form":form,
                    "role": getUsersAccount(request).position,
                    "events": Event.objects.all().order_by(F('meeting').asc(nulls_last=True)),
                    "eventAction":2,
                    }
                    messages.success(request,MSG.eventEditSuccess)
                    return render(request, "tags/mains/eventAction.html", dic)
                    
                else:
                    form =EventEditForm()
                    for field_name, field in form.fields.items():
                        if field_name != 'csrfmiddlewaretoken':
                            form.fields[field_name].widget.attrs['readonly'] = True
                    dic={
                    "form":form,
                    "role": getUsersAccount(request).position,
                    "events": Event.objects.all().order_by(F('meeting').asc(nulls_last=True)),
                    "eventAction":2,
                }
            else:
                messages.error(request,MSG.ActionFormsInvalid(form.errors.items()))
                form =EventEditForm()
                for field_name, field in form.fields.items():
                    if field_name != 'csrfmiddlewaretoken':
                        form.fields[field_name].widget.attrs['readonly'] = True
                dic={
                "form":form,
                "role": getUsersAccount(request).position,
                "events": Event.objects.all().order_by(F('meeting').asc(nulls_last=True)),
                "eventAction":2,
                }
        else:
            form =EventEditForm()
            for field_name, field in form.fields.items():
                if field_name != 'csrfmiddlewaretoken':
                    form.fields[field_name].widget.attrs['readonly'] = True
            
            dic={
            "form":form,
            "role": getUsersAccount(request).position,
            "events": Event.objects.all().order_by(F('meeting').asc(nulls_last=True)),
            "eventAction":2,
            }
        return render(request, "tags/mains/eventAction.html", dic)
    else:
        if isUserLogged(request):
            messages.error(request, MSG.permDenied)
        else:
            messages.error(request,MSG.timeOut)
        return HttpResponseRedirect(reverse('account:logged'))
def eventActionsCreate(request):
    if isUserLoggedWithPermission(request,1):
        if request.method == "POST":
            form = EventCreationForm(request.POST)
            if form.is_valid():
                tmp = form.save(commit=False)
                tmp.organizedBy = request.user.username
                ending_value = form.cleaned_data['ending']
                meeting_value = form.cleaned_data['meeting']
                if not ending_value:
                    ending_value = meeting_value + timedelta(hours=2)
                    tmp.ending = ending_value
                tmp.save()
                if tmp is not None:
                    form = EventCreationForm()
                    dic={
                        "form":form,
                        "role": getUsersAccount(request).position,
                        "eventAction":1,
                    }
                    messages.success(request,MSG.eventCreateSuccess)
                    return eventActions(request)  
                else:
                    form = EventCreationForm()
                    dic={
                        "form":form,
                        "role": getUsersAccount(request).position,
                        "eventAction":1,
                    }
                    messages.error(request,MSG.eventCreateFail)
                    return render(request, "tags/mains/addEvent.html", dic)
            else:
                messages.error(request,MSG.ActionFormsInvalid(form.errors.items()))
                form = EventCreationForm()
                dic={
                        "form":form,
                        "role": getUsersAccount(request).position,
                        "eventAction":1,
                    }
                return render(request, "tags/mains/addEvent.html", dic)
        else:
            form = EventCreationForm(initial={"organizedBy":request.user})
            dic={
            "form":form,
            "role": getUsersAccount(request).position,
            "eventAction":1,
        }
        return render(request, "tags/mains/eventAction.html", dic)
    else:
        if isUserLogged(request):
            messages.error(request, MSG.permDenied)
        else:
            messages.error(request,MSG.timeOut)
        return HttpResponseRedirect(reverse('account:logged'))
def eventActionAttendace(request):#tady jsem chybí errory
    if isUserLoggedWithPermission(request,1):
            #udělat form na stránce, kde za každého přihlášeného se přidá jedno <li> a v něm check s id=checkboxid        
        dic={
        "role": getUsersAccount(request).position,
        "events": Event.objects.all().order_by(F('meeting').asc(nulls_last=True)),
        "eventAction":3,
        }
        return render(request, "tags/mains/eventAction.html", dic)
    else:
        if isUserLogged(request):
            messages.error(request, MSG.permDenied)
        else:
            messages.error(request,MSG.timeOut)
        return HttpResponseRedirect(reverse('account:logged'))
def eventActionCancle(request):
    if isUserLoggedWithPermission(request,1):
            #udělat form na stránce, kde za každého přihlášeného se přidá jedno <li> a v něm check s id=checkboxid        
        dic={
        "role": getUsersAccount(request).position,
        "events": Event.objects.all().order_by(F('meeting').asc(nulls_last=True)),
        "eventAction":4,
        }
        return render(request, "tags/mains/eventAction.html", dic)
    else:
        if isUserLogged(request):
            messages.error(request, MSG.permDenied)
        else:
            messages.error(request,MSG.timeOut)
        return HttpResponseRedirect(reverse('account:logged'))
def cancelingOfEvent(request,event_id):
    if isUserLoggedWithPermission(request,1):
        user=getUsersAccount(request)
        event = get_object_or_404(Event, id=event_id)
        if request.method == 'POST':
            form = EventCancelForm(request.POST)
            if form.is_valid():
                event_id = form.cleaned_data['event_id']
                reason = form.cleaned_data['reason']
                sendmail = form.cleaned_data['sendMail']
                event = get_object_or_404(Event, id=event_id)
                if sendmail:
                    #send mail
                    recipients = getMailsFromEvent(event)
                    # Zpráva, kterou chcete odeslat
                    subject = f"Akce {event.name} se ruší"
                    message = f"Litomíci zdraví litomíky,\n Je nám to moc líto, ale musíme zrušit {event.name}({event.meeting.date}) z důvodu {reason}. Doufáme, že s námi zůstanete i nadále.\n Těšíme se na berkou shledanou.\n vaši Litomíci"
                    sender_email = EMAIL_HOST# E-mail odesílatele
                    # Odeslání e-mailu
                    send_mail(subject, message, sender_email, recipients)
                    event.delete()
                else:
                    event.delete()
                return eventActionCancle(request)
                
            else:
                for field, errors in form.errors.items():
                    print(f"Field: {field}, Errors: {', '.join(errors)}")
            dic={
                "role": user.position,
                "form": form,
                "event":event,
            }
            return render(request,"tags/mains/cancelEvent.html",dic)
        else:
            print("page loaded")
            form = EventCancelForm(initial={'event_id': event_id})
            dic={
                "role": user.position,
                "form": form,
                "event":event,
            }
            return render(request,"tags/mains/cancelEvent.html",dic)
    else:
        if isUserLogged(request):
            messages.error(request, MSG.permDenied)
        else:
            messages.error(request,MSG.timeOut)
        return HttpResponseRedirect(reverse('account:logged'))
def eventActionAttendace2Event(request, event_id):
    if isUserLoggedWithPermission(request,1):
        event = get_object_or_404(Event, id=event_id)
        dic={
            "role":getUsersAccount(request).position,
            "event":event,
            "notsignedMembers": notSignedMembers(event),
            "tempAtt": signedMembers4Event(event)
        }
        if request.method == 'POST':
            form = request.POST.get('attendaceForm')
            if form.is_valid():
                event_id = form.cleaned_data['event_id']
                event = get_object_or_404(Event, id=event_id)
                
                # Inicializace seznamu pro členy, kteří jsou zaškrtnuti
                checked_members = []
                
                # Projdi všechny klíče POST data
                for key in request.POST.keys():
                    if key.startswith('mem') and request.POST[key] == 'on':
                        # Přidání člena na seznam (členské ID je získáno z klíče)
                        member_id = int(key[3:])  # Převedení členského ID na celé číslo
                        checked_members.append(member_id)
                
                # Přepište pole attendance
                event.attendance.set(checked_members)
                event.save()
            dic={
            "role":getUsersAccount(request).position,
            "event":event,
        }
            return render(request,"tags/mains/AttendenceOfEvent.html",dic)
        # Render the template with the event data
        return render(request,"tags/mains/AttendenceOfEvent.html",dic)
    else:
        if isUserLogged(request):
            messages.error(request, MSG.permDenied)
        else:
            messages.error(request,MSG.timeOut)
        return HttpResponseRedirect(reverse('account:logged'))


def listAll(request,event_id=None):
    if isUserLogged(request):
        if request.method=="POST" and event_id:
            event = get_object_or_404(Event, id=event_id)
            for member in getUsersAccount(request).member.all():
                checkbox_id = f'mem{member.ATOM_id}'
                if checkbox_id in request.POST:
                    tmp=request.POST[checkbox_id]
                    if tmp == 'on' and member not in event.assigned.all():
                        event.assigned.add(member)

                    elif tmp !="on"and member in event.assigned.all():
                        event.assigned.remove(member)
                else: 
                    if member in event.assigned.all():
                        event.assigned.remove(member)
            # Save the changes to the database
            event.save()
            
    # Get members associated with the current account
        sorted_events = get_upcoming_events()
        #  = sorted(allEvents, key=lambda event: event.meeting)
        dic={
            "events": sorted_events,
            "role": getUsersAccount(request).position,
            "accountMembers":getUsersAccount(request).member,
            }
        return render(request,"tags/mains/listAllEvents.html",dic)
    else:
        messages.error(request,MSG.timeOut)
        return HttpResponseRedirect(reverse('account:logged'))
def listCamps(request):
    if isUserLogged(request):
        camptype_events = Event.objects.filter(event_type='tabor_vyprava')
    # Get members associated with the current account
        dic={
            'camps': camptype_events,
            'role': getUsersAccount(request).position,
            }
        return render(request,"tags/mains/camps.html",dic)
    else:
        messages.error(request,MSG.timeOut)
        return HttpResponseRedirect(reverse('account:logged'))
def details(request, event_id):
    if isUserLogged(request):
        event = get_object_or_404(Event, id=event_id)
        dic={
            "role":getUsersAccount(request).position,
            "event":event,
            "accountMembers":getUsersAccount(request).member,
        }
        if request.method == 'POST':
            for member in getUsersAccount(request).member.all():
                checkbox_id = f'mem{member.ATOM_id}'
                if checkbox_id in request.POST:
                    tmp=request.POST[checkbox_id]
                    # Checkbox is checked
                    if tmp == 'on' and member not in event.assigned.all():
                        event.assigned.add(member)

                    elif tmp !="on"and member in event.assigned.all():
                        event.assigned.remove(member)
                else: 
                    if member in event.assigned.all():
                        event.assigned.remove(member)
            # Save the changes to the database
            event.save()
            messages.success(request,MSG.eventEditSuccess)
            dic={
            "role":getUsersAccount(request).position,
            "event":event,
            "accountMembers":getUsersAccount(request).member,
        }
            return render(request,"tags/mains/listEvent.html",dic)
        # Render the template with the event data
        return render(request,"tags/mains/listEvent.html",dic)
    else:
        messages.error(request,MSG.timeOut)
        return HttpResponseRedirect(reverse('account:logged'))
def campReg(request,event_id):
    if isUserLogged(request):
        event = get_object_or_404(Event, id=event_id)
        acc=getUsersAccount(request)
        dic={
            "role":acc.position,
            "event":event,
            "accountMembers":acc.member,
            "mails":acc.users.all(),
            
        }
        if request.method == 'POST':
            signIn=False
            signOut=False
            for member in getUsersAccount(request).member.all():
                checkbox_id = f'mem{member.ATOM_id}'
                if checkbox_id in request.POST:
                    tmp=request.POST[checkbox_id]
                    
                    
                    # Checkbox is checked
                    if tmp == 'on' and member not in event.assigned.all():
                        event.assigned.add(member)
                        signIn=True

                    elif tmp !="on"and member in event.assigned.all():
                        event.assigned.remove(member)
                        signOut=True
                else: 
                    if member in event.assigned.all():
                        event.assigned.remove(member)
                        signOut=True

            # Save the changes to the database
            subject = 'camp reg'
            message = 'Dobrý den děti se hlásí na tábor'
            from_email = EMAIL_HOST
            recipient_list = [request.POST["mail"]]
            attachments = ['extraFiles/bezinfekcnost.pdf']

            send_email_with_attachments(subject, message, from_email, recipient_list, attachments)
            event.save()
            dic={
            "role":getUsersAccount(request).position,
            "event":event,
            "accountMembers":getUsersAccount(request).member,
            "mails":acc.users.all(),
        }
        return render(request,"tags/mains/campRegistration.html",dic)  
    else:
        messages.error(request,MSG.timeOut)
        return HttpResponseRedirect(reverse('account:logged'))
    