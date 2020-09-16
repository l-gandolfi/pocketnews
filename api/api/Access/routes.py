from flask import jsonify, request, Blueprint
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from sqlalchemy import func, desc
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_cors import CORS
from flask_mail import Message
from datetime import datetime, date, timedelta

from utils.cold_start import Cold_Start
from api import app, db, mail
from utils.errors import unauthorized, forbidden, invalid_route

from models.consumer import *
from models.interested_in import *
from models.like import *
from models.news import *
from models.recommended import *
from models.topic import *

import random, string
import requests

from api.Access.utilities import *

access = Blueprint('access', __name__)

@access.route("/register", methods=['POST'])
def register():    
    response_object = {'status': 'success', 'reason': ''}

    registration_data = request.get_json()
    name = registration_data['name']
    surname = registration_data['surname']
    email = registration_data['email']
    username = registration_data['username']
    hashed_password = generate_password_hash(registration_data['password']).decode('utf-8')

    username = username.strip()

    consumer_username = Consumer.query.filter(Consumer.username.ilike(username)).first()
    consumer_email = Consumer.query.filter_by(email=email).first()
    if consumer_username is not None:
        response_object['status'] = 'fail'
        response_object['reason'] = 'username'
        
    elif consumer_email is not None:
        response_object['status'] = 'fail'
        response_object['reason'] = 'email' 
        
    else:
        consumer = Consumer(name=name, surname=surname, email=email, username=username, password=hashed_password, email_checked=False, reset_done=False)
        db.session.add(consumer)
        db.session.commit()
        response_object['user_id'] = consumer.id
        
        send_email(consumer, 0)

    return jsonify(response_object)

@access.route("/login", methods=['POST'])
def login():    
    response_object = {'status': 'success', 'reason': ''}
    login_data = request.get_json()
    email = login_data['email']
    password = login_data['password']
    consumer = Consumer.query.filter_by(email=email).first()

    if not consumer:
        response_object = {'status': 'fail', 'reason': 'Wrong email or password'}
    elif check_password_hash(consumer.password, password):
        email_checked = consumer.email_checked
        if not email_checked:
            response_object['status'] = 'warning'
            response_object['reason'] = 'Email no checked'
            response_object['user_id'] = consumer.id
        else:
            # JWT token creation, needs expiration limit and payload (user_id)
            expiry = timedelta(days=5)
            access_token = create_access_token(identity=str(consumer.id), expires_delta=expiry)
            response_object['data'] = {'access_token': access_token,
                                        'logged_in_as': f"{consumer.email}"}
            if len(consumer.interested) == 0:
                response_object['topic'] = 0
            else:
                response_object['topic'] = 1
    else:
        response_object = {'status': 'fail', 'reason': 'Wrong email or password'}
    
    return jsonify(response_object)

@access.route("/resend_email", methods=['GET', 'POST'])
def resend_email():

    response_object = {'status': 'success', 'reason': ''}

    if request.method == 'POST':
        data = request.get_json()
        email = data['email']
        user_id = data['user_id']
        consumer_email = Consumer.query.filter_by(email=email).first()
        consumer = Consumer.query.filter_by(id=user_id).first()
        if not consumer.email_checked:
            if consumer_email == consumer or consumer_email is None:
                consumer.email = email
                consumer.email_checked = False
                db.session.commit()
                send_email(consumer, 0)
            else:
                response_object = {'status': 'fail', 'reason': 'Email already used!'}
        else:
            response_object = {'status': 'warning', 'reason': 'Email already checked!'}

        return jsonify(response_object)


@access.route("/mail_checked", methods=['POST'])
def mail_checked():

    data = request.get_json()
    user_id = data['user_id']
    op_id = int(data['op_id'])
    if op_id == 0:
        consumer = Consumer.query.filter_by(email_token=user_id).first()
    else:
        consumer = Consumer.query.filter_by(id=user_id).first()

    if consumer:
        if consumer.email_checked:
            response_object = {'status': '11', 'message': 'Email already checked'}
            if len(consumer.interested) > 0:
                response_object = {'status': '10', 'message': 'Email already checked and topic selected'}
            else:
                response_object = {'status': '13', 'message': 'No topic selected'}
        else:
            if op_id == 0:
                consumer.email_checked = True
                db.session.commit()
                response_object = {'status': '9', 'message': 'Done'}
            elif op_id == 1:
                response_object = {'status': '12', 'message': 'Email doesn\'t checked'}
    else:
        response_object = {'status': '14', 'message': 'Consumer changed email during check email phase'}
            
    return jsonify(response_object)

@access.route("/reset_psw", methods=['POST'])
def reset_psw():

    response_object = {'status': 'success', 'reason': ''}
    data = request.get_json()
    op_id = data['op_id']

    # send the reset password mail
    if op_id == 0:
        email = data['email']
        consumer = Consumer.query.filter_by(email=email).first()
        if consumer is None:
            response_object['status'] = 'fail'
            response_object['reason'] = 'No user with that email'
        else:
            response_object['user'] = consumer.username
            consumer.reset_psw_date = datetime.now()
            consumer.reset_done = False
            send_email(consumer, 1)
            db.session.commit()

    # set a new password
    elif op_id == 1:
        user_id = data['user_id']
        consumer = Consumer.query.filter_by(id=user_id).first()
        hashed_password = generate_password_hash(data['password']).decode('utf-8')
        if not consumer.reset_done:
            consumer.password = hashed_password
            consumer.reset_done = True
            db.session.commit()
            response_object = {'status': 'success', 'reason': ''}
        else:
            response_object = {'status': 'fail', 'reason': 'change already done'}

    # check about validity of reset token
    elif op_id == 2:
        user_id = data['user_id']
        consumer = Consumer.query.filter_by(id=user_id).first()
        request_date = consumer.reset_psw_date
        if (datetime.now() - request_date).seconds > 120 or consumer.reset_done:
            response_object = {'status': 'fail', 'reason': 'request expired'}
        else:
            response_object = {'status': 'success', 'reason': ''}

    return jsonify(response_object)


@access.route("/topics", methods=['GET', 'POST'])
@jwt_required
def topics():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        # post_data is a list of dict, containing keys: topic and id
        # We are interested in the topic id
        # Get the user by current token
        user_id = get_jwt_identity()
        u = Consumer.query.filter_by(id=user_id).first()
        if len(u.interested) == 0:
            for topic in post_data.get('topics'):
                # Get the topic by id
                t = Topic.query.filter_by(id=topic.get('id')).first()
                # Update the relationship
                t.subscribe.append(u)
                # Add to db and commit
                db.session.add(u)
                db.session.commit()
            # Assign news to handle the cold start problem
            cs = Cold_Start(u, post_data.get('topics'))
            cs.assign()
            
    elif request.method == 'GET':
        # Query the db and get all topic objects
        topics = Topic.query.all()
        # Create a list of dict
        TOPICS = []
        # Iterate topic objects in topics
        for topic in topics:
            # Save the topic name and an aux boolean value
            TOPICS.append({
                'topic': topic.topic,
                'id': topic.id,
                'clicked': False
            })
        response_object['topics'] = TOPICS
        user_id = get_jwt_identity()
        u = Consumer.query.filter_by(id=user_id).first()
        if len(u.interested) > 0:
            response_object['topic_sel'] = 1
        else:
            response_object['topic_sel'] = 0
        
    return jsonify(response_object)
