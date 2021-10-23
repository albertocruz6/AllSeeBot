import discord
import os
from twitterFunctions.twitter_api import *
from datetime import datetime
from tools.timer_tool import Timer

# Discord client
now = datetime.now()  
client = discord.Client()
tw_handler = get_api_handler()
if tw_handler is None:
	print("Invalid tw bot account found!")
else:
	 tw_handler.update_status("AllSeeBot ONLINE! - " + now.strftime("%d/%m/%Y %H:%M:%S"));
	 print("Logged into AllSeeBot TW account at time " + now.strftime("%d/%m/%Y %H:%M:%S") )

# Client events all exist on the Discord API 
@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	msg = message.content
	if msg.startswith("$greet"):
		await message.channel.send("Hello {0.author}!".format(message))

def main():
	client.run(os.getenv('BOT_TOKEN'))
	print("Hello there! -> Bot is ONLINE")

if __name__ == "__main__":
	main()