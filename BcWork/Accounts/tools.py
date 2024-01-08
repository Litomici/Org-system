from .models import *
import csv
from django.contrib.auth.models import User
def has_account(user):
    """
        if user is already used return true
    """
    try:
        # Check if the user is associated with any account
        return Account.objects.filter(users=user).exists()
    except Account.DoesNotExist:
        return False
def is_username_available(username):
    try:
        # Try to get a user with the given username
        user = User.objects.get(username=username)
        return False  # Username already exists
    except User.DoesNotExist:
        return True  # Username is available
def add_spaces(input_string):
    reversed_string = input_string[::-1]  # Reverse the string
    spaced_string = ' '.join(reversed_string[i:i+3] for i in range(0, len(reversed_string), 3))

    # Reverse the spaced string back to its original order
    result_string = spaced_string[::-1]
    return result_string
def isUserLogged(request):
    if request.user.is_authenticated:
        if has_account(request.user):
            return True
        else:
            return False
    return False

def isUserLoggedWithPermission(request,perm):
    if request.user.is_authenticated:
        if has_account(request.user):
            try:
                account = Account.objects.filter(user=request.user)
                if account.exists() and account.position>=perm:
                    return True
                else:
                    return False
            except:
                return False
    return False
def membersAtomCheck():
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

