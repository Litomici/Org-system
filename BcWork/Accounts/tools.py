from .models import *
import csv
from datetime import datetime
from django.db.models import Q
from Events.models import Event
from django.contrib.auth.models import User

def has_account(user):
    """
        if user is already bound to accocunt return true
    """
    try:
        # Check if the user is associated with any account
        return Account.objects.filter(users=user).exists()
    except Account.DoesNotExist:
        return False
def is_username_available(username):
    """ check function for username

    Args:
        username (string): username of new user

    Returns:
        bool: True if username is aviable
    """
    try:
        # Try to get a user with the given username
        user = User.objects.get(username=username)
        return False  # Username already exists
    except User.DoesNotExist:
        return True  # Username is available
def add_spaces(input_string):
    """ Phone number formater. from n-lenght nubers in string will make a fromat of +xx ... xxx xxx

    Args:
        input_string (string): string containing numbers

    Returns:
        string: pnone number with extra spaces
    """
    reversed_string = input_string[::-1]  # Reverse the string
    spaced_string = ' '.join(reversed_string[i:i+3] for i in range(0, len(reversed_string), 3))

    # Reverse the spaced string back to its original order
    result_string = spaced_string[::-1]
    return result_string
def isUserLogged(request):
    """function verify if user is logged

    Args:
        request (request): current request from templace

    Returns:
        bool: True if user is logged in
    """
    if request.user.is_authenticated:
        if has_account(request.user):
            return True
        else:
            return False
    return False

def isUserLoggedWithPermission(request,perm):
    """verify a user and his permission to access certain parts

    Args:
        request (request): current request
        perm (int): degree of safetty

    Returns:
        bool: True if user is logged and allowed to do such actions
    """
    if request.user.is_authenticated:
        print("user in")
        if has_account(request.user):
            print("user has account")
            # try:
            print("searching for account data")
            account = Account.objects.get(users=request.user)

            print(account.position)
            print("data loaded")
            
            if account.position >= perm:
                return True
            else:
                return False
            # except:
            #     print("unable to read data")
            #     return False
    return False
def membersAtomCheck():
    """
    function will check if newly created member is already register in assotiation of turistics. Also it means his fee was already paid. If true member will be given his ATOM_Id.
    Returns:
        bool: True if succesfuly find memeber in register and give him a Atom ID
    """
    try:
        with open("extraFiles/export.csv", 'r', encoding='Windows 1250') as file:
            csv_reader = csv.DictReader(file, delimiter=';')
            for row in csv_reader:
                matching_member = member.objects.filter(ATOM_id=row['id'])
                if not matching_member.exists():    
                    jmeno = row['Jméno']
                    surname = row['Příjmení']
                    # Query the Member model to check if a member with the given name and surname exists
                    matching_members = member.objects.filter(jmeno=jmeno, surname=surname, ATOM_id="")
                    if matching_members.exists():
                        tmpMEM = matching_members.first()
                    # Assuming the CSV has a column named 'id', update the 'id' in the CSV row
                        tmpMEM.ATOM_id=row['id']
                        tmpMEM.save()
    except Exception as e:
        return False
    return True
def getUsersAccount(request):
    account = get_object_or_404(Account, users=request.user)
    return account
def get_upcoming_events():
    """querry over Event table. Looking only for not outdated actions also sorts them by date.

    Returns:
        array[Event]: array of Evetns objects
    """
    current_date = datetime.now()
    upcoming_events = Event.objects.filter(
        Q(meeting__gte=current_date) | Q(ending__gte=current_date)
    ).order_by('meeting').distinct()

    return upcoming_events
def get_filtered_events(attributes):
    """filtering function for evetns by given atributes. atributes must be names of params of Event table. also sorted by meeting date

    Args:
        attributes (array[string]): array of strings representations of atributes of Event table

    Returns:
        array[Event]: array of Evetns objects
    """
    current_date = datetime.now()
    
    # Construct the dynamic filters based on the provided attributes
    dynamic_filters = Q()
    for attribute in attributes:
        filter_param = {f"{attribute}__gte": current_date}
        dynamic_filters |= Q(**filter_param)

    # Apply the filters and order by meeting datetime
    filtered_events = Event.objects.filter(dynamic_filters).order_by('meeting').distinct()

    return filtered_events
def signedMembers4Event(event):
    assigned_members = event.assigned.all()
    attending_members = event.attendance.all()

    # Získání všech členů, kteří jsou zúčastněni a přiřazeni na události
    signed_members = member.objects.filter(Q(id__in=assigned_members) & Q(id__in=attending_members))
    #signed_members = member.objects.filter(id__in=assigned_members, id__in=attending_members)

    # Vytvoření pole tuple (member, bool)
    result = [(member, member in attending_members) for member in assigned_members]


    # Přidání členů, kteří jsou buď zúčastněni nebo přiřazeni, ale ne oboje
    additional_members = member.objects.exclude(id__in=signed_members).filter(Q(id__in=assigned_members) | Q(id__in=attending_members))
    result += [(member, False) for member in additional_members]

    return result
def notSignedMembers(event):
    assigned_members = event.assigned.all()
    attending_members = event.attendance.all()

    # Získání všech členů, kteří nejsou přiřazeni ani zúčastněni na události
    not_signed_members = member.objects.exclude(id__in=assigned_members).exclude(id__in=attending_members)

    # Seřazení abecedně podle jména
    sorted_members = not_signed_members.order_by('jmeno')

    return sorted_members