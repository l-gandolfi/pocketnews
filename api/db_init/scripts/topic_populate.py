import json
import os.path as path

import numpy as np
import pandas as pd

import psycopg2
from db_func import Functions

# Importing tweets.csv to extract unique topics
PATH = path.abspath('./') + '/db_init/tweets_data/'
df = pd.read_csv(PATH + 'tweets.csv')  

# Extracting unique TOPICS
topics = set(df.topic)
# Removing NaN element
topics = {topic for topic in topics if pd.notna(topic)}
# Set to List conversion
topics = list(topics)
topics.sort()

try:
        connect_str = "dbname='news_db' user='pgadmin' host='db' " + \
                    "password='pgadmin'"
        # Use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # Create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()

        # Inserting TOPICS into DB       
        for i in range(0,len(topics)):
            cursor.execute("""INSERT INTO topic (id, topic) VALUES(%s, %s) ON CONFLICT (id) DO NOTHING;""", (i, topics[i]))     

        conn.commit()
        cursor.close()
        conn.close()

except Exception as e:
        print("ERROR DETECTED WHILE INSERTING TOPICS")
        print(e)
