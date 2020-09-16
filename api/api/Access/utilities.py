from flask_mail import Message
from datetime import datetime, date, timedelta

from utils.cold_start import Cold_Start
from api import mail

from models.consumer import *

import random, string

def send_email(consumer, type):
    # confirm email
    if type == 0:
        letters = string.ascii_lowercase
        email_token = ''.join(random.choice(letters) for i in range(10))
        consumer.email_token = email_token
        db.session.commit()
        mail_obj = 'Confirm your email - PocketNews Network'   
        text = "<h3>Welcome "+consumer.username+" to PocketNews!!</h3>"
        text = text + "<p>Please click on the <a href = http://localhost:8081/emailCheck/"+str(email_token)+">link</a> for confirm your email!</p>"
        text = text + "<p>Do not reply to this email</p>"
    elif type == 1:
        mail_obj = 'Reset password - PocketNews Network'  
        text = "<h3>Hi "+consumer.username+",</h3>"
        text = text + '<br>'
        text = text + "<p>You recently requested to reset your password for your PocketNews account."
        text = text + " Click the <a href=http://localhost:8081/changePassword/"+str(consumer.id)+">link </a> to reset it. <br>"
        text = text + "If you did not request a password reset, please ignore this email.</p>"

    text = text + "<br>"
    text = text + "<p>We will see on PocketNews!!!</p>"
    text = text + "<br>"
    text = text +  "<small>PocketNews Developers</small>"
    msg = Message(mail_obj,
                sender='pocketNews@demo.com',
                recipients=[consumer.email])
    msg.html = text
    try:
        if not('test_front' in consumer.email) and not('test_back' in consumer.email):
            mail.send(msg)
    except:
        pass