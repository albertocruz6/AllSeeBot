import discord
from discord.ext import tasks

from datetime import datetime
from utils.twitter.twitter_api import *
from utils.external_tools.timer_tool import Timer

# Discord Client class
class MyClient(discord.Client):
	async def on_ready(self):
		now = datetime.now()  
		print("Bot is initialized!")
		print('We have logged in as {0.user}'.format(self))
		
		# Twitter Authentication
		self.tw_handler = get_api_handler()
		if self.tw_handler is None:
			print("Invalid tw bot account found! Fetching will not initiate")
		else:
			self.tw_handler.update_status("AllSeeBot ONLINE! - " + now.strftime("%d/%m/%Y %H:%M:%S"));
			print("Logged into AllSeeBot TW account at time " + now.strftime("%d/%m/%Y %H:%M:%S"))
			self.update_fetch.start()

		self.lst_commands = ["greet", "commands", "search"]
	

	async def on_message(self,message):
		if message.author == self.user:
			return
		msg = message.content
		if msg.startswith("$"): # command prefix will be $
			msg_arr = msg.split(" ")
			if msg.startswith("${0}".format(self.lst_commands[0])):
				await message.channel.send("Hello @{0.author}!".format(message))
			elif msg.startswith("${0}".format(self.lst_commands[1])):
				await message.channel.send("{0}!".format(self.lst_commands))
	
	# Loop to fetch tweets of users lists
	@tasks.loop(seconds=60.0)
	async def update_fetch(self):
		print("Testing async task!")