from math import e
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

def eventActions(request):
    if isUserLoggedWithPermission(request,1):
        dic={
            "role": getUsersAccount(request).position,
            "eventAction":0,
        }
        return render(request, "tags/mains/eventAction.html", dic)
    else:
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
                        if form_field_name in form.cleaned_data:
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
                    messages.success(request,"Změny úspěšně uloženy ")
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
                messages.error(request,"Ups! Něco se pokazilo změny nebyly uloženy\n")
                for er in form.errors.items():
                    messages.error(request,er.__str__())
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
                    messages.success(request,"Akce úspěšně vytvořena")
                    return render(request, "tags/mains/addEvent.html", dic)
                    
                else:
                    form = EventCreationForm()
                    dic={
                        "form":form,
                        "role": getUsersAccount(request).position,
                        "eventAction":1,
                    }
                    messages.error(request,"Ups! Něco se pokazilo a akce nebyla vytvořena")
                    return render(request, "tags/mains/addEvent.html", dic)
            else:
                messages.error(request,"Ups! Něco se pokazilo a akce nebyla vytvořena")
                form = EventCreationForm()
                dic={
                        "form":form,
                        "role": getUsersAccount(request).position,
                        "eventAction":1,
                    }
                return render(request, "tags/mains/addEvent.html", dic)
        else:
            form = EventCreationForm()
            dic={
            "form":form,
            "role": getUsersAccount(request).position,
            "eventAction":1,
        }
        return render(request, "tags/mains/eventAction.html", dic)
    else:
        return HttpResponseRedirect(reverse('account:logged'))
def eventActionAttendace(request):
    if isUserLoggedWithPermission(request,1):
            #udělat form na stránce, kde za každého přihlášeného se přidá jedno <li> a v něm check s id=checkboxid        
        dic={
        "role": getUsersAccount(request).position,
        "events": Event.objects.all().order_by(F('meeting').asc(nulls_last=True)),
        "eventAction":3,
        }
        return render(request, "tags/mains/eventAction.html", dic)
    else:
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
        return HttpResponseRedirect(reverse('account:logged'))
    return HttpResponse


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
            dic={
            "role":getUsersAccount(request).position,
            "event":event,
            "accountMembers":getUsersAccount(request).member,
        }
            return render(request,"tags/mains/listEvent.html",dic)
        # Render the template with the event data
        return render(request,"tags/mains/listEvent.html",dic)
    else:
        return HttpResponseRedirect(reverse('account:logged'))

    