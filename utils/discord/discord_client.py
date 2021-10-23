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
		self.user_search_stack = []
	

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
			elif msg.startswith("${0}".format(self.lst_commands[2])):
				if len(msg_arr) < 2:
					await message.channel.send("Please insert twitter username(s) to be queued!")
				else:
					for i in range(1,len(msg_arr)):
						self.user_search_stack.append(msg_arr[i])
					await message.channel.send("{0}!".format(self.lst_commands))
	
	# Loop to fetch tweets of users lists
	@tasks.loop(seconds=60.0)
	async def update_fetch(self):
		if self.user_search_stack:
			user = self.user_search_stack.pop()
			print("Searching for {0} in twitter".format(user))
		print("Testing async task!")