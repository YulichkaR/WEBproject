from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import compressGood, compressGoodImage
import os

def get_port():
    return os.environ.get('DJANGO_RUNSERVER_PORT')

def start():
	scheduler = BackgroundScheduler()

	if(str(get_port()) == '8000'):
		scheduler.add_job(compressGood, 'interval', seconds=15)
		scheduler.add_job(compressGoodImage, 'interval', seconds=25)
	if(str(get_port()) == '8001'):
		scheduler.add_job(compressGood, 'interval', seconds=16)
		scheduler.add_job(compressGoodImage, 'interval', seconds=26)
	
	scheduler.start()