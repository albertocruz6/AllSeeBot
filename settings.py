import asyncio
from datetime import datetime
from utils.twitter.twitter_api import get_api_handler
from utils.external_tools.database_api import get_db_connection

# setting and initial values
def init_setup(logger):
	global tw_api	
	tw_api = get_api_handler(logger)
	global db_conn
	db_conn = get_db_connection(logger)
	