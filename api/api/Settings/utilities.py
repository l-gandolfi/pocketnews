from models.consumer import *


# Checking functions
def checkEmail(change_email, user_id):
    check = True
    if(change_email != ''):
        exist = Consumer.query.filter_by(email=change_email).first()
        #La mail esiste già. Un altro utente l'ha già presa
        if(exist != None):
            if(int(user_id) != exist.id):
                check = False
    return check

def checkUsername(change_username, user_id):
    check = True
    if(change_username != ''):
        exist = Consumer.query.filter_by(username=change_username).first()
        #Li user esiste già. Un altro utente l'ha già presa
        if(exist != None):
            if(int(user_id) != exist.id):
                check = False
    return check

def checkPassword(password, confirm_password):
    check = True
    #le password scelte non combaciano
    if(password != confirm_password):
        check = False
    return check
