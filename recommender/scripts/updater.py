from scripts import update_db
from apscheduler.schedulers.background import BackgroundScheduler

def update_job():
    print('Updating recommendations..')
    update_db.standard_update()
    print('Done!')

print('Starting scheduler in background..')
scheduler = BackgroundScheduler()
job = scheduler.add_job(update_job, 'interval', minutes=5)

try:
    scheduler.start()
except Error as e:
    print(e)
