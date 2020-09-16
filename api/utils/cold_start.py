import numpy as np

from api import db
from models.like import Like
from models.news import News
from sqlalchemy import desc


class Cold_Start:
    """ 
    ####################################################################
    Class to handle the cold start problem.
    Here we present a first simple version, which will be updated later.
    ####################################################################
    """

    def __init__(self, user, topics=None):
        # Initialize Consumer object
        self.user = user
        # Iniialize Topics json
        self.topics = topics

    def assign(self, update_topics=None):
        # Condition to check:
        # First case. Registration: topic to add
        # will be passed as argument during
        # Cold Start object creation
        # Second case. Topic Settings: topic to add
        # will be passed as argument of assign call
        if update_topics != None:
            self.topics = update_topics

        # Iterate topics and assign news
        for topic in self.topics:
            # Get the topic by id
            # t = Topic.query.filter_by(id=topic.get('id')).first()
            # Get news by that topic
            topic_id = topic.get("id")
            news = (
                News.query.filter_by(topic_id=topic_id)
                .order_by(desc(News.date))
                .limit(3)
            )

            # For each news get the id and store in Like class
            for item in news:
                like = Like(consumer_id=self.user.id, news_id=item.id, initial=True)
                db.session.add(like)
                db.session.commit()

    def remove(self, remove_topics_id):
        # Query to extract all news marked as intial = True
        # by a specific user
        # This news need to be removed since user removed
        # their topic from preferences and this
        # news were just "placeholders"
        news_liked = Like.query.filter(Like.consumer_id == self.user.id).filter(
            Like.initial == True
        ).all()

        # For each liked in news_liked
        for like in news_liked:
            # Query to extract news object
            news = News.query.filter_by(id=like.news_id).first()
            # If news topic belongs to remove_topics
            # it means that it must be removed
            if news.topic_id in remove_topics_id:
                db.session.delete(like)
                db.session.commit()
