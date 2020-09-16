import random
import string
from datetime import date, datetime, timedelta

import requests

from api import app, db, mail
from api.Access.utilities import *
from api.Settings.utilities import *
from flask import Blueprint, jsonify, request
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from flask_mail import Message
from models.consumer import *
from models.interested_in import *
from models.like import *
from models.news import *
from models.recommended import *
from models.topic import *
from sqlalchemy import desc, func
from utils.cold_start import Cold_Start
from utils.errors import forbidden, invalid_route, unauthorized

settings = Blueprint("settings", __name__)


@settings.route("/settings/topics", methods=["GET", "POST"])
@jwt_required
def get_user_topic():
    response_object = {"status": "success"}

    if request.method == "GET":

        user_id = get_jwt_identity()
        user = Consumer.query.filter_by(id=user_id).first()

        # Query the db and get all topic objects
        topics = Topic.query.all()

        # List of dict containing user's topic
        # preferences {topic_name,id,clicked}
        TOPICS = []

        for topic in topics:
            # Save the topic name and an aux boolean value
            TOPICS.append(
                {"topic": topic.topic.capitalize(), "id": topic.id, "clicked": False}
            )
        
        # Getting user's topic preferences
        user_topics = user.interested
        
        for topic in user_topics:
            TOPICS[topic.id]["clicked"] = True

        response_object["topics"] = TOPICS

    elif request.method == "POST":
        post_data = request.get_json()

        # Getting User asking for a topic
        # update
        user_id = get_jwt_identity()
        user = Consumer.query.filter_by(id=user_id).first()

        # Saving old user's preferences
        old_topic_objects = user.interested

        old_topic_ids = [old_topic.id for old_topic in old_topic_objects]

        # Dict of topics to submit from the POST request
        new_topic = post_data.get("topics")

        # List of new_topic ids
        new_topic_ids = [topic.get("id") for topic in new_topic]

        # Query the db and get all topic objects from new_topic_ids
        new_topic_objects = [
            Topic.query.filter_by(id=t_id).first() for t_id in new_topic_ids
        ]

        # Updating user's preferences
        # removing topics that have been disliked
        for old_t_id in old_topic_ids:
            if old_t_id not in new_topic_ids:
                topic_to_remove = Topic.query.filter_by(id=old_t_id).first()
                user.interested.remove(topic_to_remove)

        # Updating user's preferences
        # adding topics that have been liked
        for new_t in new_topic_objects:
            if new_t not in old_topic_objects:
                user.interested.append(new_t)

        # Commiting actions performed
        db.session.add(user)
        db.session.commit()

        # Looking for new topics that need a Cold Start
        cold_start_topics = [
            topic for topic in new_topic if topic["id"] not in old_topic_ids
        ]

        # Looking for old topics that need to be removed
        # (need to drop news marked as initial= True
        # beloning to these topics. These news were just placeholders
        # waiting for real user interaction with the system
        # )
        remove_cold_start_topics_ids = [
            topic_id for topic_id in old_topic_ids if topic_id not in new_topic_ids
        ]

        # Performing Cold Start
        cs = Cold_Start(user)

        # Calling Cold Start on New topics added by the current user
        if bool(cold_start_topics):
            cs.assign(cold_start_topics)

        # Calling Cold Start on Old topics removed by the current user
        # this call will remove like marked as initial = True (aka placeholder like
        # to perform reccomendation)
        if remove_cold_start_topics_ids:
            cs.remove(remove_cold_start_topics_ids)

    return jsonify(response_object)


@settings.route("/editaccount", methods=["POST"])
@jwt_required
def get_user_information():
    response_object = {"status": "success", "reason": ""}

    post_data = request.get_json()
    user_id = get_jwt_identity()
    
    # Query the db and get Consumer object
    user = Consumer.query.filter_by(id=user_id).first()

    # Saving post_data information into local variables
    name = post_data.get("name")
    surname = post_data.get("surname")
    username = post_data.get("username")
    email = post_data.get("email")
    password = post_data.get("password")
    confirmpassword = post_data.get("confirmpassword")

    username = username.strip()

    # Check di eamil, username e password
    if checkEmail(email, user_id) & checkUsername(username, user_id):
        # Checking if Password and Confirm Password information
        # match
        if checkPassword(password, confirmpassword):
            # If fields are equals to "" it means that no changes
            # have been done, otherwise information need to be
            # updated
            if username != "":
                user.username = username
            if name != "":
                user.name = name
            if surname != "":
                user.surname = surname
            if email != "":
                user.email = email
                user.email_checked = False
                send_email(user, 0)
            if password != "":
                user.password = generate_password_hash(password).decode("utf-8")
        
        # If Password and Confirm password don't match, the response
        # will be an error
        else:
            response_object["status"] = "fail"
            response_object[
                "reason"
            ] = "Password and Confirmation Password don't match."
    # If Email or Username are already taken, the response
    # will be an error
    else:
        if((not checkUsername(username, user_id)) & (not checkEmail(email, user_id))):
            response_object["status"] = "fail"
            response_object["reason"] = "Username and Email already taken."
        elif((not checkEmail(email, user_id))):
            response_object["status"] = "fail"
            response_object["reason"] = "Email already taken."
        elif((not checkUsername(username, user_id))):
            response_object["status"] = "fail"
            response_object["reason"] = "Username already taken."
    db.session.commit()

    return jsonify(response_object)


@settings.route("/modifypublicprofile", methods=["GET", "POST"])
@jwt_required
def modifypublicprofile():
    response_object = {"status": "success", "information": ""}
    if request.method == "POST":
        post_data = request.get_json()
        user_id = get_jwt_identity()
        user = Consumer.query.filter_by(id=user_id).first()
        user.city = post_data.get("city")
        user.bio = post_data.get("bio")
        user.dob = post_data.get("dob")
        user.publicinfo = post_data.get("publicinfo")

        INFORMATION = {
            "city": user.city,
            "bio": user.bio,
            "dob": user.dob,
            "publicinfo": user.publicinfo,
        }
        response_object["information"] = INFORMATION
        db.session.commit()

    elif request.method == "GET":
        INFORMATION = {
            "city": "",
            "bio": "",
            "dob": "",
            "visiblecheck": [],
        }
        user_id = get_jwt_identity()
        user = Consumer.query.filter_by(id=user_id).first()
        if user.city != None:
            INFORMATION["city"] = user.city
        if user.city != None:
            INFORMATION["bio"] = user.bio
        if user.city != None:
            INFORMATION["dob"] = user.dob
        if user.publicinfo != None:
            if user.publicinfo[0] == "1":
                INFORMATION["visiblecheck"].append("city")
            if user.publicinfo[1] == "1":
                INFORMATION["visiblecheck"].append("bio")
            if user.publicinfo[2] == "1":
                INFORMATION["visiblecheck"].append("dob")
            if user.publicinfo[3] == "1":
                INFORMATION["visiblecheck"].append("topics")
            if user.publicinfo[4] == "1":
                INFORMATION["visiblecheck"].append("liked")

        response_object["information"] = INFORMATION

    return jsonify(response_object)
    
    
@settings.route("/settings/delete")
@jwt_required
def deleteAccount():
    response_object = {}
    post_data = request.get_json()
    # Get the id from cookies
    user_id = get_jwt_identity()
    # Get the user by id
    user = Consumer.query.filter_by(id=user_id).first()
    # Delete the user
    db.session.delete(user)
    db.session.commit()
    response_object['status'] = 'success'
    return jsonify(response_object)
