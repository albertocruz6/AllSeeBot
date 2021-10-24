import tweepy
import os

# File to define python funcitonalities 
def get_api_handler():
	try:
	    auth = tweepy.OAuthHandler(os.getenv("TW_KEY"),  os.getenv("TW_SECRET"))
	    auth.set_access_token(os.getenv("TW_C_KEY"), os.getenv("TW_C_SECRET"))
	    return tweepy.API(auth)
	except Exception as e:
		return None # If environmental variables fail


