from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

class member(models.Model):
    jmeno=models.CharField(max_length=30, default="john")
    surname=models.CharField(max_length=40, default="Smith")
    birthday = models.DateField(default=now())
    ATOM_id=models.CharField(max_length=18, blank=True)
    GDPR=models.BooleanField(default=True)
    healthProblems=models.CharField(default="Dítě nemá žádná zdravotní omezení ani speciální požadavky na stravu či zacházení")
    objects = models.Manager()
    def __str__(self):
            return self.jmeno +" "+ self.surname

class Account(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)#pro prihlaseni
    users = models.ManyToManyField(User, related_name='access_users',default=[user]) # Many users can be associated with one account
    #Kontaktni údaje na Rodice - nutne
    addres1=models.CharField(default="")
    city1=models.CharField(default="")
    psc1=models.CharField(default="")
    mobile1=models.CharField(max_length=13, default="")
    #kontaktni udaje na 2. rodice nebo jinou poverenou osobu - cislo a mail nutne
    addres2=models.CharField(default="", blank=True)
    city2=models.CharField(default="", blank=True)
    psc2=models.CharField(default="", blank=True)
    mobile2=models.CharField(max_length=13, default="")
    #dalsi udaje vazane k ucu
    wallet=models.FloatField(default=(0.0))
    position=models.IntegerField(default=0)
    member=models.ManyToManyField(member, related_name=("members"), blank=True)
    objects = models.Manager()
    def __str__(self):
        return self.user.__str__()

class EmailConfirmation(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create(cls, email,sender):
        token = sender+"=>"+get_random_string(length=16)
        return cls.objects.create(email=email, token=token)

    def send_confirmation_email(self):
        subject = 'Registrace do systému Litomíků'
        message = render_to_string('confirmation_email.txt', {'token': self.token})
        from_email = 'turistakLitomici@gmail.com'
        send_mail(subject, message, from_email, [self.email])