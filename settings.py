import asyncio
from datetime import datetime
from utils.twitter.twitter_api import get_api_handler

# setting and initial values
def init_setup():
	global tw_api	
	tw_api = get_api_handler()
	