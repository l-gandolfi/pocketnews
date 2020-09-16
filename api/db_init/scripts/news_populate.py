from db_func import Functions
import os.path as path
import psycopg2
import numpy as np
import pandas as pd

#Connection to SQLite Database
PATH = path.abspath('./') + '/db_init/tweets_data/'
f = Functions(PATH)

# Importing tweets.csv to extract unique topics
df = pd.read_csv(PATH + 'tweets.csv')

# Extracting all tweet Authors
authors = list(df.user)

#Retrieving TWEETS from Database SQLite
data = f.readAllTweets()

try:
        connect_str = "dbname='news_db' user='pgadmin' host='db' " + \
                    "password='pgadmin'"
        # Use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # Create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()

        for i in range(0,len(data)):
            # Data to be inserted into NEWS
            news_id = data[i][0]
            #print(data[i][1].decode('utf-8').encode("unicode-escape").decode("unicode-escape"))
            text = data[i][1].decode("utf-8")
            embedding = data[i][3].tolist()
            date = data[i][4]
            topic_name = data[i][2].decode(encoding='UTF-8').strip('""')
            author = authors[i]

            # Alcuni tweet avevano topic con valore a NaN, non verranno inseriti
            if(topic_name != 'NaN'): 
                # Selecting correct TOPIC_ID for NEWS_TOPIC from TOPIC table (FOREIGN KEY)
                query = ("""SELECT id FROM topic WHERE topic = %s;""")
                cursor.execute(query, (topic_name, ))
                res = cursor.fetchone()
                topic_id = res[0]

                # Inserting TOPICS into DB
                cursor.execute("""INSERT INTO news (id, text, date, embedding, author, topic_id) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;""", (news_id, text, date, embedding, author, topic_id))
                
        conn.commit()
        cursor.close()
        conn.close()

except Exception as e:
        print("ERROR DETECTED WHILE INSERTING NEWS")
        print(e)
