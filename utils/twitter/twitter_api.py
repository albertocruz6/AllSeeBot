import tweepy
import os

# File to define python funcitonalities 
def get_tw_api_handler(logger):
	try:
	    auth = tweepy.OAuthHandler(os.getenv("TW_KEY"),  os.getenv("TW_SECRET"))
	    auth.set_access_token(os.getenv("TW_C_KEY"), os.getenv("TW_C_SECRET"))
	    api = tweepy.API(auth)
	    logger.info("Connected to twitter api!...")
	    return api
	except Exception as e:
		logger.error(e)
		return None # If environmental variables fail


