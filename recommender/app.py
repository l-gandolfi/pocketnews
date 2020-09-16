from flask import Flask, jsonify
from flask_cors import CORS
from scripts import updater
from scripts.rs import RecommenderSystem
import psycopg2

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# Connect to postegresql
def connect():
    conn = ''
    try:
        connect_str = "dbname='news_db' user='pgadmin' host='db' password='pgadmin'"
        conn = psycopg2.connect(connect_str)
    except:
        print("Error in Flask-Recommender during db connection.")
    return conn

@app.route('/recommend/news/<news_id>', methods=['GET'])
def get_news_recommendations(news_id):
    conn = connect()
    if conn == '':
        response_object = {'status': 'fail'}
    else:
        response_object = {'status': 'success'}
        cursor = conn.cursor()
        query = ("""SELECT * FROM news WHERE id=%s;""")
        cursor.execute(query, (news_id, ))
        news = cursor.fetchone()
        # Instantiate class RecommenderSystem
        rs = RecommenderSystem(news)
        # We want to compute the alternative version 
        # i.e. the one which computes similarity of single news with other news about the same topic
        news_ids = rs.alternative_exec()
        NEWS = []
        for element in news_ids:
            NEWS.append({'news_id':element})
        response_object['data'] = NEWS
    return jsonify(response_object)


@app.route('/recommend/users/<user_id>', methods=['GET'])
def get_user_recommendations(user_id):
    conn = connect()
    if conn == '':
        response_object = {'status': 'fail'}
    else:
        response_object = {'status': 'success'}
        cursor = conn.cursor()
        query = ("""SELECT * FROM consumer WHERE id=%s;""")
        cursor.execute(query, (user_id, ))
        user = cursor.fetchone()
        # Instantiate class RecommenderSystem
        rs = RecommenderSystem(user)
        # We want to get only similar users to the current one
        similar_users_ids = rs.users_recommendation()
        CONSUMERS = []
        for element in similar_users_ids:
            CONSUMERS.append({'user_id':element})
        response_object['data'] = CONSUMERS
    return jsonify(response_object)           

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002, threaded=True)

    
