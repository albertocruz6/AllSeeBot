import os
import logging
from datetime import datetime

import settings
from utils.discord.search_bot_client import AllSeeBot
from utils.external_tools.helper_functions import send_log_reports


def main():
	# Logging setup
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.INFO)
	formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s', "%Y-%m-%d %H:%M:%S")
	log_file_handler = logging.FileHandler('allSeeBot.log')
	log_file_handler.setFormatter(formatter)
	logger.addHandler(log_file_handler)
	# Booting sequence
	try:
		settings.init_setup(logger)
		client = AllSeeBot()
		logger.info('Started All See Bot...')
		client.run(os.getenv('BOT_TOKEN'))
	finally:
		if settings.tw_api is not None:
			settings.tw_api.update_status("AllSeeBot Offline! :') - {0}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))
		logger.warning('Bot will be turned off...')
		send_log_reports(logger)

if __name__ == "__main__":
	main()