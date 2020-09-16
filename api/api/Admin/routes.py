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

admin = Blueprint('admin', __name__)

@admin.route("/admin/users", methods=['GET', 'POST'])
@jwt_required
def users_list():
    response_object = {'status': 'success'}
    if request.method == 'GET':
        usernames = []
        for consumer in Consumer.query.all():
            usernames.append({'username':consumer.username})
        response_object['usernames'] = usernames
    elif request.method == 'POST':
        post_data = request.get_json()
        username = post_data['username']
        consumer = Consumer.query.filter_by(username=username).first()
        response_object['name']=consumer.name
        response_object['surname']=consumer.surname
        response_object['email']=consumer.email
        topics = []
        for interest in consumer.interested:
            topics.append(interest.topic)
        response_object['topics']=topics
    return jsonify(response_object)