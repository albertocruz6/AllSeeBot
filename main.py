import os

from utils.discord.discord_client import MyClient


def main():
	try:
		client = MyClient()
		print("Hello there! -> Bot is initializing....")
		client.run(os.getenv('BOT_TOKEN'))
	finally:
		print("\nBot will be turned off...\n")

if __name__ == "__main__":
	main()