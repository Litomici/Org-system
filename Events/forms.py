from django.forms import DateTimeInput, ModelForm
from django import forms
from .models import Event

class EventCreationForm(ModelForm):
    class Meta:
        model = Event
        fields = ['event_type','name', 'destination', 'meeting', 'ending', 'departure', 'arrival', 'notes']
        labels={
            "event_type":('Druh akce'),
            "name": ('Název akce'),
            "destination": ('Místo konání'),
            "meeting": ('Datum a čas srazu'),
            "ending": ('Datum a čas příjezdu'),
            "departure": ('Místo srazu'),
            "arrival": ('Místo vyzvednutí rodiči'),
            "notes": ('Co s sebou a další poznámky'),
        }
        widgets={
            'event_type': forms.Select(choices=Event.EVENT_TYPES),
            "name": forms.TextInput(attrs={'class':'form-control form-control-lg'}),
            "destination": forms.TextInput(attrs={'class':'col-sm-4 col-form-label'}),
            "meeting": DateTimeInput(attrs={'type': 'datetime-local', 'format': '%Y-%m-%dT%H:%M'}),
            'ending': DateTimeInput(attrs={'type': 'datetime-local', 'format': '%Y-%m-%dT%H:%M'}),
            "departure": forms.TextInput(attrs={'class':'col-sm-4 col-form-label'}),
            "arrival": forms.TextInput(attrs= {'class': 'col-sm-4 col-form-label'}),
            "notes": forms.TextInput(attrs={'class':'form-control'}),
        }
