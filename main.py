import os
import logger

import settings
from utils.discord.search_bot_client import SearchBot


def main():
	logger = logging.getLogger(__name__)
	logger.selLevel(logging.INFO)
	log_file_handler = logging.fileHandler('bert_bots.log')
	logger.addHandler(log_file_handler)
	try:
		settings.init_setup()
		client = MyClient()
		logger.warning('Started BOTS')
		client.run(os.getenv('BOT_TOKEN'))
	finally:
    	logger.warning('Bot will be turned off...')

if __name__ == "__main__":
	main()