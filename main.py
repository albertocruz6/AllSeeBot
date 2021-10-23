import discord
import os
from twitterFunctions.twitter_api import *


# Discord client  
client = discord.Client()
tw_handler = get_api_handler()
if tw_handler is None:
	print("Invalid tw bot account found!")
else:
	 tw_handler.update_status("AllSeeBot ONLINE!");

# Client events all exist on the Discord API 
@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return


	msg = message.content
	if msg.startswith("$hello"):
		await message.channel.send("Hello!")

def main():
	client.run(os.getenv('BOT_TOKEN'))
	print("Hello there! -> Bot is ONLINE")

if __name__ == "__main__":
	main()