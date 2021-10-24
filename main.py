import os
import logging
from datetime import datetime

import settings
from utils.discord.search_bot_client import AllSeeBot


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
		client = AllSeeBot()
		logger.warning('Started BOTS')
		client.run(os.getenv('BOT_TOKEN'))
	finally:
		settings.tw_api.update_status("AllSeeBot Offline! :') - {0}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
		logger.warning('Bot will be turned off...')

if __name__ == "__main__":
	main()