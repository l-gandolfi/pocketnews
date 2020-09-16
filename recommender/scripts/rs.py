'''
@Title: Recommender System engine
@Description: In the final project, this class will be called in the asynch script, in order
to update the database with recommendations and improve the system usability.
Right now, it provides a standard execution method, which can be called to obtain a list of
recommendation news and their similarity score.
it is also provided an alternative execution method, which computes recommendations about a news.
@Usage: To perform a standard execution, call a new istance of this class giving just the consumer object
as argument, then call the standard_exec method which will provide a dict of news_ids (recommended)
and their similarity score. 
To perform an alternative execution, just call a new istance giving the news object as argument, 
then call the alternative_exec method, which will provide a list of news_ids.
'''

import os.path as path
import numpy as np
import re
import itertools
import string
import statistics
import datetime
from sklearn.metrics.pairwise import cosine_similarity
import psycopg2
from collections import Counter, OrderedDict
import copy
import random

class RecommenderSystem():
    def __init__(self, consumer):
        # Save Consumer object
        self.user = consumer
    
    '''
    Method to connect to postegresql. Useful to avoid repeating code.
    '''
    def connect(self):
        conn = ''
        try:
            connect_str = "dbname='news_db' user='pgadmin' host='db' password='pgadmin'"
            conn = psycopg2.connect(connect_str)
        except:
            print("Error during db connection.")
        return conn
    
    '''
    Get a list of topic ids expressed in user preferences.
    '''
    def get_topics(self):
        conn = self.connect()
        # Create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        # Define the query
        query = ("""SELECT topic_id FROM interested_in WHERE consumer_id=%s;""")
        cursor.execute(query, (self.user[0], ))
        topics = cursor.fetchall()
        topics = [t[0] for t in topics]
        cursor.close()
        conn.close()
        return topics
    
    '''
    Get tweets embedding in User Likes, by topic.
    '''
    def get_likes_by_topic(self, topic_id):
        conn = self.connect()
        cursor = conn.cursor()  
        
        # First get news_ids by user likes
        query = ("""SELECT news_id FROM liked WHERE consumer_id=%s;""")
        cursor.execute(query, (self.user[0], ))
        news_ids = cursor.fetchall()
        news_ids = [n[0] for n in news_ids]
        
        # Finally filter news by topic id and save their embedding     
        query = ("""SELECT embedding FROM news WHERE topic_id=%s;""")
        cursor.execute(query, (topic_id, ))
        embeddings = cursor.fetchall()
        embeddings = [e[0] for e in embeddings]
        
        cursor.close()
        conn.close()
        return embeddings
    
    '''
    Get news from database.
    '''
    def get_news(self, topic_id=False):
        conn = self.connect()
        cursor = conn.cursor()
        
        if not topic_id:
            query = ("""SELECT * FROM news;""")
            cursor.execute(query)
            news = cursor.fetchall()
        else:
            query = ("""SELECT * FROM news WHERE topic_id=%s;""")
            cursor.execute(query, (topic_id, ))
            news = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        return news
    
    '''
    Riceve in input i vettori embedded e restituisce il loro vettore media
    '''
    def computeMean(self, vectors):
        return np.mean( np.array(vectors), axis=0 )
    
    '''
    Riceve in input il vettore centroide dal quale computare la similarità
    '''    
    def computeSimilarity(self, centroid, top_n=20, single_topic_id=False):
        # Retrieve embedding from db
        if not single_topic_id:
            news = self.get_news()
        else:
            news = self.get_news(single_topic_id)
        
        embeddings = [record[3] for record in news]
        ids = [record[0] for record in news]
        # Compute similarity
        similarity_dict = {}
        for vector, id in zip(embeddings, ids):
            sim = np.dot(centroid, vector)/(np.linalg.norm(centroid)*np.linalg.norm(vector))
            similarity_dict[id] = sim
        
        # Order the dict
        ordered = OrderedDict(sorted(similarity_dict.items(), key=lambda element: element[1],reverse=True))
        most_similar = dict(Counter(ordered).most_common(top_n))
        # Here you could filter the top scored if it has similarity=1
        return most_similar
        
    '''
    Rank according to date and similarity. 
    
    !!!!!!!!!!!!!!!!!!!!! NOT UPDATED !!!!!!!!!!!!!!!!!!!!!!
    
    It will be updated in a future release.
    '''
    def ranking(self, similarity_dict):
        # We are going to modify the dict so save a copy before do it
        old_similarity_dict = copy.deepcopy(similarity_dict)

        # First obtain dates of tweets -> 2018-02 becomes 1802
        date_list = []
        for k,v in similarity_dict.items():
            # k is the tweet id
            # ////// date = News.query.filter_by(id=k).first().date
            # query the db and get dates
            date_list = ""
        # Now compute a weighted mean 
        count = 0

        for k, v in similarity_dict.items():
            res = ((v) * (date_list[count]/2000))
            count=count+1
            similarity_dict[k]=res
        
        # Order the dict
        dict_ordered = {k: v for k, v in sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True)}

        # Retrieve the list of similarity after the new sorting
        top_list = []
        for k,v in dict_ordered.items():
            top_list.append(old_similarity_dict.get(k))
        return dict_ordered, top_list
    
    '''
    Method to handle the long-tail problem.
    
    !!!!!!!!!!!!!!!!!!!!! NOT UPDATED !!!!!!!!!!!!!!!!!!!!!!
    
    It will be updated in a future release.
    '''
    def long_tail(self, results_dict):
        # Obtain the 20th number from the Long-tail
        ran_value = randint(20, len(results_dict)-1)
        count = 0
        for k, v in results_dict.items():
            if(count==ran_value):
                ran_key = k
                ran_similarity = v
            count=count+1
        #tail = {ran_key: ran_similarity}
        return ran_key, ran_similarity
    
    
    '''
    Main method for standard execution. It return a dict where similarity
    scores are mapped to news ids.
    '''    
    def standard_exec(self, top_n=20):
        topics = self.get_topics()
        results = []
        for topic_id in topics:
            # embeddings of likes
            user_embeddings = self.get_likes_by_topic(topic_id)
            # get the mean
            mean_vector = self.computeMean(user_embeddings)
            # compute similarity
            similarity_results = self.computeSimilarity(mean_vector)
            # append in the big list
            results.append(similarity_results)
        # Merge results into a single dict
        results_dict = {k: v for d in results for k, v in d.items()}
        # Order by value
        results_dict = {k: v for k, v in sorted(results_dict.items(), key=lambda item: item[1], reverse=True)}
        # Obtain only top N ids
        #top_n = 20
        top_n_dict = dict(Counter(results_dict).most_common(top_n))
        '''
        The following part is now omitted, but will be provided in a future release.
        
        # Now order by considering the date
        top_n_dict, top_n_list = self.ranking(top_n_dict)
        
        self.keys = [k for k, v in top_n_dict.items()]
        
        ran_key, ran_similarity = self.long_tail(similarity_dict)
        '''
        
        return top_n_dict
        
    '''
    Execution to provide similar news according to a single news.
    In this scenario the variable self.user is a news object.
    '''
    def alternative_exec(self, top_n=20):
        # Filter topics according to the news in self.user object
        news = self.user
        embedding = news[3]
        topic_id = news[5]
        similarity_results = self.computeSimilarity(embedding, single_topic_id=topic_id)
        top_n_dict = dict(Counter(similarity_results).most_common(top_n))
        
        # We are only interested in news ids
        return list(top_n_dict.keys())
    
    
    '''
    Method to suggest users to follow according to their topics.
    In a future release will be provided a similar method which recommends users
    according to their likes.
    '''
    def users_recommendation(self, top_n=3):
        # top_n is the number of users to be retrieved
        
        user = self.user
        # 1. Get topics preferences
        topics_ids = self.get_topics()
        
        # 2. Get usernames from users interested with the same topics, ignoring the current one
        conn = self.connect()
        cursor = conn.cursor()
        query = ("""SELECT consumer_id FROM interested_in WHERE topic_id=%s AND consumer_id!=%s;""")
        candidates = dict()
        for topic in topics_ids:
            cursor.execute(query, (topic, user[0], ))
            res = []
            for row in cursor.fetchall():
                res.append(row[0])    
            candidates[topic] = res
        
        # 3. Avoid user repetitions using sets
        suggested_users = set()
        for key, values in candidates.items():
            for consumer_id in values:
                suggested_users.add(consumer_id)
        
        # 4. From these users, we have to filter users who are already followed
        query = ("""SELECT following_id FROM "Consumer_following" WHERE consumer_id=%s;""")
        cursor.execute(query, (user[0], ))
        to_filter = []
        for row in cursor.fetchall():
            to_filter.append(row[0])
        # Iterate to_filter list and remove them from suggested_users
        for user in to_filter:
            try:
                suggested_users.remove(user)
            except:
                pass
                
        # 5. Now we insert a random component to suggests different users everytime
        results = []
        if len(suggested_users) <= top_n:
            # Retrieve all users
            results = list(suggested_users)
        else:
            # Random choose top_n
            ran = set()
            while(len(ran) < top_n):
                ran.add(random.randint(0, len(suggested_users)-1))
            # When the while ends, we have top_n DIFFERENT random values
            suggested_users = list(suggested_users)

            for i in range(top_n):
                results.append(suggested_users[ran.pop()])
        
        cursor.close()
        conn.close()
        
        # Remember to handle empty results
        
        return results
            
        
