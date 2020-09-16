import random
import string
from datetime import date, datetime, timedelta

import requests

from api import app, db, mail
from flask import Blueprint, jsonify, request
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from flask_mail import Message
from models.consumer import *
from models.interested_in import *
from models.like import Like
from models.news import *
from models.recommended import *
from models.topic import *
from sqlalchemy import desc, func
from utils.cold_start import Cold_Start
from utils.errors import forbidden, invalid_route, unauthorized

social = Blueprint('social', __name__)

@social.route('/news/recommended/<id>')
@jwt_required
def get_similar_news(id):
    response_object = {}
    response_object["status"]="success"
    news = db.session.query(News).filter_by(id = id).first()

    # Query the recommender system on docker recommender:5002
    url = "http://recommender:5002/recommend/news/"+id
    res = requests.get(url)
    data = res.json()
    data = data.get('data')
    
    # Filter the current id and query news object from db
    similar_news = []
    for row in data:
        if row.get('news_id') != id:
            similar_news.append(db.session.query(News).filter_by(id = row.get('news_id')).first())
    similar_news_json = [n.to_json() for n in similar_news]
    response_object["data"] = similar_news_json[1:]
   
    return jsonify(response_object)

@social.route("/news/<id>")
@jwt_required
def get_single_news(id):
    response_object = {'status': 'success'}
    # Retrieve single news
    news = db.session.query(News).filter_by(id = id).first()
    response_object["news"] = news.to_json()
    return jsonify(response_object)

@social.route("/account/me")
@jwt_required
def get_personal_profile():
    response_object = {'status': 'success'}
    # Retrieve account personal info according to session ID
    user_id = get_jwt_identity()
    user = Consumer.query.filter_by(id=user_id).first()
    response_object["data"] = user.to_json()
    return jsonify(response_object)

@social.route("/social/favorite", methods=["POST"])
@jwt_required
def get_favorite():
    response_object = {'status': 'success', 'users': []}
    post_data = request.get_json()
    favorite_by = Like.query.filter_by(news_id=post_data['news_id'], initial=False).all()
    if favorite_by != []:
        response_object["users"] = [element.consumer_id for element in favorite_by]
    return jsonify(response_object)

@social.route("/social/like", methods=["POST"])
@jwt_required
def like_news():  
    response_object = {'status': 'success'}
    user_id = get_jwt_identity()
    post_data = request.get_json()
    like = Like(consumer_id=user_id, news_id=post_data['news_id'], initial=False)
    db.session.add(like)
    db.session.commit() 
    return jsonify(response_object)

@social.route("/social/dislike", methods=["POST"])
@jwt_required
def dislike_news():
    response_object = {'status': 'success'}
    user_id = get_jwt_identity()    
    post_data = request.get_json()
    news_liked = Like.query.filter(Like.consumer_id == user_id).filter(
            Like.news_id == post_data['news_id']
        ).first()
    db.session.delete(news_liked)
    db.session.commit()

    return jsonify(response_object)	

@social.route('/social/likes', methods=["POST"])
@jwt_required
def get_likes():
    # User performing request
    user_id = get_jwt_identity()
    response_object = {"status": "success", "data": []}
    post_data = request.get_json()
    # User's information required (it could be myself or someone else)
    user = Consumer.query.filter_by(username=post_data['user']).first()
    news_liked = Like.query.filter(Like.consumer_id == user.id).filter(
            Like.initial == False
        ).all()
    LIKES = []
    for news in news_liked:
        n = News.query.filter_by(id=news.news_id).first().to_json()
        LIKES.append(n)

    if LIKES != []:
        response_object['data'] = LIKES
    
    return jsonify(response_object)
		
@social.route('/profile')
@jwt_required
def profile():
    response_object = {'status': 'success', 'information':''}
    user_id = get_jwt_identity()
    user = Consumer.query.filter_by(id=user_id).first()
    consumer = Consumer.query.filter_by(username=request.args['username']).first()
    if consumer != None: 
        INFORMATION = {
            'first_name' : '',
            'last_name' : '',
            'email' : '',
            'username' : '',
            'city': '',
            'bio': '',
            'dob': '',
            'n_following':'',
            'n_followers':'',
            'following': [],
            'followers': [],
            'interested': [],
            'state': '',
            'display_follow': '',
            #'news_like': '',
            'publicinfo': ''
        }
        INFORMATION['first_name']= consumer.name
        INFORMATION['last_name']= consumer.surname
        INFORMATION['email']= consumer.email
        INFORMATION['username']= consumer.username
        INFORMATION['city']= consumer.city
        INFORMATION['bio']= consumer.bio
        INFORMATION['dob']= consumer.dob
        INFORMATION['n_following']= str(len(consumer.following))
        INFORMATION['n_followers']= str(len(consumer.followers))
        topics = consumer.interested
        TOPICS = []
        # Iterate topic objects in topics
        for topic in topics:
            # Save the topic name and an aux boolean value
            TOPICS.append({
                'topic': topic.topic,
            })
        INFORMATION['interested'] = TOPICS
        if (consumer in user.followers):
            INFORMATION['state'] = 'Unfollow' 
        else:
            INFORMATION['state'] = 'Follow'
        if(user == consumer):
            INFORMATION['display_follow'] = 'False'
        else:
            INFORMATION['display_follow'] = 'True'
        followers = consumer.followers
        FOLLOWERS = []
        # Iterate topic objects in topics
        for follower in followers:
            # Save the topic name and an aux boolean value
            FOLLOWERS.append({
                'username': follower.username,
            })
        INFORMATION['followers']= FOLLOWERS
        following = consumer.following
        FOLLOWING = []
        # Iterate topic objects in topics
        for follow in following:
            # Save the topic name and an aux boolean value
            FOLLOWING.append({
                'username': follow.username,
            })
        INFORMATION['following']= FOLLOWING
        '''
        liked = consumer.news_like
        LIKED = []
        # Iterate topic objects in topics
        for like in liked:
            # Save the topic name and an aux boolean value
            LIKED.append({
                'news': like.news_id
            })
        INFORMATION['news_like'] = LIKED
        '''
        INFORMATION['publicinfo']= consumer.publicinfo
        response_object['information'] = INFORMATION
    else:
        response_object = {'status': 'fail', 'information':''}

    return jsonify(response_object)

    
@social.route('/social/who-to-follow')
@jwt_required
def who_to_follow():
    # 1. Receive a GET request
    # 2. Extract user id from cookies
    # 3. Ask Recommender System to retrieve similar users
    # 4. Respond with a json containing Consumer objects
    
    user_id = get_jwt_identity()
    
    # Query the recommender system on docker recommender:5002
    url = "http://recommender:5002/recommend/users/"+user_id
    res = requests.get(url)
    data = res.json()
    data = data.get('data')
    
    # Query the database to get Consumer objects
    similar_users = []
    for row in data:
        similar_users.append(db.session.query(Consumer).filter_by(id=row.get('user_id')).first())
    similar_users = [u.to_json() for u in similar_users]
    response_object = {'status': 'success', 'data':similar_users}

    return jsonify(response_object)
    
@social.route('/social/follow', methods=["POST"])
@jwt_required
def follow():
    response_object = {"status": "success","usernames": []}
    # Getting user_id
    user_id = get_jwt_identity()
    user = Consumer.query.filter_by(id=user_id).first()
    # Getting post data containing username of new follower/unfollower
    post_data = request.get_json()
    # Query to db to retrieve follower/unfollower consunmer object
    new_follower = Consumer.query.filter_by(username = post_data.get('following')).first()
    # Checking user followers list not None
    if(user.followers != None):
        # If new follower is already into followers list
        # Remove it. (Unfollow operation)
        if(new_follower in user.followers):
            user.followers.remove(new_follower)
        # If new follower isn't already into followers list
        # Append it. (Follow operation)
        else:
            user.followers.append(new_follower)
    # Committing operation to db
    db.session.add(user)
    db.session.commit()
    # Populate response_object with followers list
    if(user.followers != None):
        for item in user.followers:
            response_object["usernames"].append(item.username)

    return jsonify(response_object)
