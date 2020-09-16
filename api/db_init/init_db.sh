#!/bin/sh
flask db init
flask db migrate
flask db upgrade

echo "Topic population..."
python /app/db_init/scripts/topic_populate.py
echo "Done"
echo "News population..."
python /app/db_init/scripts/news_populate.py
echo "Done"