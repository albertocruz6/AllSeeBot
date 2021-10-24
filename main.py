import os
import logging

import settings
from utils.discord.search_bot_client import SearchBot


def main():
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)
	log_file_handler = logging.FileHandler('allSeeBot.log')
	logger.addHandler(log_file_handler)
	try:
		settings.init_setup()
		client = SearchBot()
		logger.warning('Started BOTS')
		client.run(os.getenv('BOT_TOKEN'))
	finally:
		logger.warning('Bot will be turned off...')

if __name__ == "__main__":
	main()