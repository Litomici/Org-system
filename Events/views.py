from math import e
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render,redirect
from .models import Event
from Accounts.models import *
from Accounts.tools import isUserLoggedWithPermission, isUserLogged,getUsersAccount
from.forms import *

def eventActions(request):
    if isUserLogged(request):
        dic={
            "role": getUsersAccount(request).position,
        }
        return render(request, "tags/mains/eventAction.html", dic)
    
def create(request):
    if isUserLogged(request):
        if request.method == "POST":
            form = EventCreationForm(request.POST)
            if form.is_valid():
                tmp = form.save(commit=False)
                tmp.user = request.user  # Assign the logged-in user
                tmp.save()
                if tmp is not None:
                    # Redirect to the next step of registration (adjust the URL accordingly)
                    return HttpResponseRedirect(reverse('logged'))#redirect('next_step_registration')  # Change 'next_step_registration' to your actual URL
                else:
                    form = EventCreationForm()
                    return render(request, "tags/mains/addEvent.html", {'form': form})
            else:
                form = EventCreationForm()
                return render(request, "tags/mains/addEvent.html", {'form': form})
        else:
            form = EventCreationForm()
        return render(request, "tags/mains/addEvent.html", {'form': form})
    else:
        return HttpResponseRedirect(reverse('logged'))
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
        allEvents = Event.objects.all()
        sorted_events = sorted(allEvents, key=lambda event: event.meeting)
        dic={
            "events": sorted_events,
            "role": getUsersAccount(request).position,
            "accountMembers":getUsersAccount(request).member,
            }
        return render(request,"tags/mains/listAllEvents.html",dic)
    return HttpResponseRedirect(reverse('logged'))

def listCamps(request):
    if isUserLogged(request):
        camptype_events = Event.objects.filter(event_type='tabor_vyprava')
    # Get members associated with the current account
        dic={
            'camps': camptype_events,
            'role': getUsersAccount(request).position,
            }
        return render(request,"tags/mains/camps.html",dic)
    return HttpResponseRedirect(reverse('logged'))

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
        return HttpResponseRedirect(reverse('logged'))