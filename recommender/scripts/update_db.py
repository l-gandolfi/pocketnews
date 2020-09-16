from scripts.rs import RecommenderSystem
import datetime
import psycopg2

'''
Method to connect to postegresql. Useful to avoid repeating code.
'''
def connect():
    conn = ''
    try:
        connect_str = "dbname='news_db' user='pgadmin' host='db' password='pgadmin'"
        conn = psycopg2.connect(connect_str)
    except:
        print("Error during db connection.")
    return conn

'''
This method is called when a new user is detected. It generates his recommendations and store them.
'''
def add_recommendations_new_user(user, conn, cursor):
    rs = RecommenderSystem(user)
    similarities = rs.standard_exec()
    # similarities is a dict composed by id:simvalue
    # iterate for each news
    for key in similarities:
        # Insert
        try:
            cursor.execute("""INSERT INTO recommended_to (consumer_id, news_id, date, score) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING;""", (user[0], key, datetime.date.today(), similarities.get(key)))
        except Exception as e:
            print('Error inserting recommendations')
            print(e)
        else:
            print('.. ADDED a news recommendation to DB - User: '+ user[4])
    conn.commit()
    

'''
This method is called when an user has already his recommendations stored.
It updates the list just deleting old data.
'''
def update_recommendations(user, conn, cursor):
    # Delete old recommendations
    cursor.execute("""DELETE FROM recommended_to WHERE consumer_id = %s;""", (user[0],))
    # Re-compute
    add_recommendations_new_user(user, conn, cursor)

'''
Simple aux method to check if recommendations are already stored.
'''
def rec_exists(cursor, user_id):
    cursor.execute("SELECT consumer_id FROM recommended_to WHERE consumer_id = %s", (user_id,))
    return cursor.fetchone() is not None

def standard_update():
    # Connect
    conn = connect()
    
    if conn == '':
        print("Unable to connect..")
    else:
        # Create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        # Define the query
        query = ("""SELECT * FROM consumer""")
        # Execute the query
        cursor.execute(query)
        users = cursor.fetchall()
        for user in users:
            user_id = user[0]
            recommendations_exist = rec_exists(cursor, user_id)
            if recommendations_exist:
                # Table already populated, Update according to new likes
                update_recommendations(user, conn, cursor)
            else:
                # It's a new User, Compute for the first time
                add_recommendations_new_user(user, conn, cursor)

        cursor.close()
        conn.close()
