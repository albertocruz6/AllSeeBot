import os
import logging

import settings
from utils.discord.search_bot_client import SearchBot


def main():
	# Logging setup
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)
	formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
	log_file_handler = logging.FileHandler('allSeeBot.log')
	log_file_handler.setFormatter(formatter)
	logger.addHandler(log_file_handler)
	# Booting sequence
	try:
		settings.init_setup()
		client = SearchBot()
		logger.warning('Started BOTS')
		client.run(os.getenv('BOT_TOKEN'))
	finally:
		logger.warning('Bot will be turned off...')

if __name__ == "__main__":
	main()