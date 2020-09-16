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

home = Blueprint('home', __name__)

@home.route('/search', methods = ['GET', 'POST'])
def search():
    response_object = {'status': 'success', 'usernames': []}
    if request.method == 'GET':
        username = request.args['username']
        users = Consumer.query.filter(Consumer.username.ilike(f'%{username}%')).all()
        for user in users:
            response_object['usernames'].append(str(user.username))
    return jsonify(response_object)

@home.route("/feed")
@jwt_required
def get_feed():
    response_object = {'status': 'success'}
    # Get user topics of interest
    user_id = get_jwt_identity()

    if bool(Recommended.query.filter_by(consumer_id=user_id).first()):
        # if true: return news from the table, ordered by the score
        recommendations = Recommended.query.filter_by(consumer_id=user_id).order_by(desc(Recommended.score)).all()
        news_ids = [r.news_id for r in recommendations]
        news = []
        for i in news_ids:
            news.append(News.query.filter_by(id=i).first())
    else:
        # if false: avoid computing recomendations now to speed up visualization
        # Get user topics of interest
        topics = db.session.query(Interested_in).filter_by(consumer_id=user_id).all()
        topics = [topic.topic_id for topic in topics]
        # Get news corresponding to the topics in random order, limited to 10
        news = db.session.query(News).filter(News.topic_id.in_(topics)).order_by(func.random()).limit(10).all()
    
    topics = Topic.query.all()
    top_dict = {topic.id: topic.topic for topic in topics}
    res = [n.to_json() for n in news]
    for n in res:
        n["topic"] = top_dict[n["topic_id"]]
    response_object["data"] = res
    return response_object