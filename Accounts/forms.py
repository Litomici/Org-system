from tkinter.tix import Form
from django.forms import DateTimeInput, ModelForm
from django import forms
from .models import Account,member
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class NewMemeberForm(ModelForm):
    class Meta:
        model = member
        fields = ['jmeno', 'surname', 'birthday','GDPR', 'healthProblems']
        labels={
            "jmeno": ('Jméno:'),
            "surname": ('Příjmení:'),
            "birthday":('Datum narození '),
            "GDPR": ('Souhlasím s tím, aby byly pořizovány a uchovávány fotografie a osobní údaje člena.'),
            "healthProblems": ('Zdravotní problémy a jiná důležitá omezení:'),
        }
        widgets={
            "jmeno": forms.TextInput(attrs={'class':'form-control form-control-lg','pattern': '^[A-Za-zÀ-ÖØ-öø-ÿĀ-žſ]+$'}),
            "surname": forms.TextInput(attrs={'class':'form-control form-control-lg','pattern': '^[A-Za-zÀ-ÖØ-öø-ÿĀ-žſ]+$'}),
            "birthday": forms.DateInput(attrs={'type': 'date'}),
            "GDPR": forms.CheckboxInput(attrs={'class':'form-check-input','id':'checkbox'}),
            "healthProblems": forms.Textarea(attrs= {"class":"form-control", "id":"exampleFormControlTextarea1","rows":"3"}),
        }
class NewAccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['user','mobile1', 'addres1', 'city1', 'psc1','mobile2']
        labels={
            "user":(""),
            "mobile1": ('Telefon na rodiče nebo zákonného zástupce'),
            "addres1": ('Adresa bydliště'),
            "city1": ('Město'),
            "psc1": ('PSČ'),
            "mobile2":('Telefon na druhého rodiče nebo jiného člena rodiny pro případ nouze')
        }
        widgets={
            "user":"",
            "mobile1": forms.TextInput(attrs={'class':'form-control form-control-lg'}),
            "addres1": forms.TextInput(attrs={'class':'form-control form-control-lg'}),
            "city1": forms.TextInput(attrs= {'class': 'col-sm-4 col-form-label'}),
            "psc1": forms.TextInput(attrs= {'class': 'col-sm-4 col-form-label'}),
            "mobile2":forms.TextInput(attrs= {'class': 'col-sm-4 col-form-label'})
        }
        
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields=["username","password1","password2"]
        widgets={
            "username": forms.TextInput(),
            "password1": forms.PasswordInput(),
            "password2": forms.PasswordInput(),
        }
        labels={
            "username": ('Emailová adresa'),
            "password1": ("Heslo"),
            "password2": ('Potvrzení hesla'),
        }
        help_texts = {
            "password1": "Heslo musí být 8 znaků dlouhé. Nesmí obsahovat pouze čísla nebo být seznamu snadno prolomitelných hesel.",
        }
class EmailForm(forms.Form):
    subject = forms.CharField(max_length=100)
    text = forms.CharField(widget=forms.Textarea)
    
class AddUserForm(forms.Form):
    newUserEmail = forms.EmailField(
        label="Email, kterému chcete umožnit přístup.",
        required=True,
        widget=forms.TextInput(attrs={'class': 'your-custom-class'})
    )
class SetPasswordForm(forms.Form):
    password1 = forms.CharField(
        label="Heslo",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Potvrzení hesla",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    