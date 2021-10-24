import discord
from discord.ext import tasks
import tweepy

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

		self.lst_commands = ["greet", "commands", "searchTW"]
		self.user_search_stack = []
		self.user_search_stack_channels = []

	

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
				msg_arr = msg.split("\\\\")
				if len(msg_arr) < 2:
					await message.channel.send("Please insert twitter username(s) to be queued!")
				else:
					self.user_search_stack_channels.append(message.channel)
					users = []
					for i in range(1,len(msg_arr)):
						users.append(msg_arr[i])
					self.user_search_stack.append(users)
					await message.channel.send("Queued user searches {0}".format(self.user_search_stack))
	
	# Loop to fetch tweets of users lists
	@tasks.loop(seconds=30.0)
	async def update_fetch(self):
		if self.user_search_stack:
			channel = self.user_search_stack_channels.pop()
			users = self.user_search_stack.pop()
			for i in range(3):
				if not users:
					break
				user = users.pop()
				print("Searching for {0} in twitter...".format(user))
				try:
					user_r = self.tw_handler.get_user(screen_name=user)
					# fetching the url
					if user_r.screen_name is not None:
						url = "https://twitter.com/{0}".format(user_r.screen_name)
						await channel.send("User found! \n{0}".format(url))
						# await channel.send("User found! \n{0}".format(url))
					else:
						await channel.send("User not found!")
				except:
					await channel.send("{0} not found!".format(user))
			if users: # if users remain in this queue return current channel
				self.user_search_stack.append(users)
				self.user_search_stack_channels.append(channel)
				channel.send("Queued user searches remaining {0}".format(self.user_search_stack))