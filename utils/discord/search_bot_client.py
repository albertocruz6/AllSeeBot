import discord
from discord.ext import tasks
import tweepy
import csv
import logging
import smtplib
import os
from email.message import EmailMessage

import settings
from datetime import datetime
from utils.external_tools.timer_tool import Timer

# Discord Client class
class SearchBot(discord.Client):
	async def on_ready(self):
		now = datetime.now()  

		# Logger setup
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel(logging.INFO)
		formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
		log_file_handler = logging.FileHandler('searchbot.log')
		log_file_handler.setFormatter(formatter)
		self.logger.addHandler(log_file_handler)

		self.logger.info("Bot is initialized!")
		self.logger.info('We have logged in as {0.user}'.format(self))
		# Twitter Authentication
		self.tw_handler = settings.tw_api
		# Initial Variables
		self.lst_commands = ["greet", "commands", "searchTW", "addUSR", "help"]
		self.user_search_stack = []
		self.user_search_stack_channels = []
		self.user_track_dictionary= {901864726015209472 : None, 2196628051: None}

		# csv
		self.fileName = "utils/discord/last_tweets.csv"

		# channel to track twitter feed
		self.user_track_channel = None
		for channel in self.get_all_channels():
			if channel.name == "updatedtwitterfeed":
				self.user_track_channel = channel
				break

		# log status
		if self.tw_handler is None:
			self.logger.warning("Invalid tw bot account found! Fetching will not initiate")
		else:
			self.tw_handler.update_status("SearchBot ONLINE! - " + now.strftime("%d/%m/%Y %H:%M:%S"));
			print("Logged into SearchBot TW account at time " + now.strftime("%d/%m/%Y %H:%M:%S"))
			self.search_tw_loop.start()
			self.update_tracked_tw.start()

		self.send_log_reports.start() # every 6 hours send log report 


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
			elif msg.startswith("${0}".format(self.lst_commands[3])):
				msg_arr = msg.split("\\\\")
				if len(msg_arr) < 2:
					await message.channel.send("Please insert twitter id(s) to be queued!")
				else:
					for i in range(1,len(msg_arr)):
						try:
							self.user_track_dictionary[int(msg_arr[i])] = None
							print("Added user {0} to tracking tl".format(msg_arr[i]))
						except Exception as e:
							print(e)
							print("Didnt add user {0} to tracking tl".format(msg_arr[i]))

	
	# Loop to fetch tweets of users lists
	@tasks.loop(seconds=30.0)
	async def search_tw_loop(self):
		if self.user_search_stack:
			channel = self.user_search_stack_channels.pop(0)
			users = self.user_search_stack.pop(0)
			for i in range(3):
				if not users:
					break
				user = users.pop(0)
				self.logger.info("Searching for {0} in twitter...".format(user))
				try:
					self.logger.info("User found!")
					user_r = self.tw_handler.get_user(screen_name=user)
					# fetching the url
					if user_r.screen_name is not None:
						url = "https://twitter.com/{0}".format(user_r.screen_name)
						await channel.send("User found! UserId: {1}\n{0}".format(url, user_r.id))
						# await channel.send("User found! \n{0}".format(url))
					else:
						self.logger.info("User not found!")
						await channel.send("User not found!")
				except:
					await channel.send("{0} not found!".format(user))
			if users: # if users remain in this queue return current channel
				self.user_search_stack.append(users)
				self.user_search_stack_channels.append(channel)
				await channel.send("Queued user searches remaining {0}".format(self.user_search_stack))
		

	@tasks.loop(minutes=5.0)
	async def update_tracked_tw(self):
		self.logger.info("Tracking users tweets...")
		if self.user_track_dictionary:
			for user in self.user_track_dictionary:
				lastWrittenTweet = self.findLastTweet(user)
				if self.user_track_dictionary[user] is None:
					try:
						user_r = self.tw_handler.get_user(user_id=user)
						tweets = self.tw_handler.user_timeline(screen_name=user_r.screen_name,count = 1)
						self.user_track_dictionary[user] = tweets[0].id
						self.writeLastTweet(user, self.user_track_dictionary[user])
						if self.user_track_channel:
							await self.user_track_channel.send("https://twitter.com/twitter/statuses/{0}".format(self.user_track_dictionary[user]))
					except Exception as e: 
						print(e)
						self.logger.error(e)
						self.logger.error("Couldn find user {0}!".format(user))
				else:
					try:
						user_r = self.tw_handler.get_user(user_id=user)
						tweets = self.tw_handler.user_timeline(screen_name=user_r.screen_name,count = 1)
						if self.user_track_dictionary[user] != tweets[0].id:
							self.writeLastTweet(user, self.user_track_dictionary[user])
							self.user_track_dictionary[user] = tweets[0].id
							if self.user_track_channel:
								await self.user_track_channel.send("https://twitter.com/twitter/statuses/{0}".format(self.user_track_dictionary[user]))
						else:
							self.logger.info('User {0} already updated in tl...'.format(user_r.screen_name))
					except Exception as e: 
						print(e)
						self.logger.error(e)
						self.logger.error("Couldn find user {0}!".format(user))

	# Helper methods
	#############################################
	#############################################
	def findLastTweet(self, uid):
		with open(self.fileName) as csvFile:
			csvreader = csv.reader(csvFile, delimiter=',')
			header = []
			header = next(csvreader)
			rows = []
			for row in csvreader:
				rows.append(row)
		for row in rows:
			if str(row[0]) == str(uid):
				self.logger.info("Found user {0} in csv!".format(uid))
				return row[1]
		return None
	#############################################
	#############################################
	def writeLastTweet(self, uid, tw_id):
		with open(self.fileName) as csvFile:
			csvreader = csv.reader(csvFile, delimiter=',')
			header = []
			header = next(csvreader)
			rows = []
			for row in csvreader:
				rows.append(row)
		
		for index in range(len(rows)):
			if str(rows[index][0]) == str(uid):
				rows[index][1] = tw_id
				break
			if index == len(rows) - 1: # didn't find it in csv
				self.logger.info("Didn't find the uid {0} in csv...".format(uid))
				rows.append([uid, tw_id])		
		with open(self.fileName, 'w') as ncsvFile:
			tweet_writer = csv.writer(ncsvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			tweet_writer.writerow(header)
			for row in rows:
				tweet_writer.writerow(row)
	#############################################
	#############################################
	@tasks.loop(hours=6.0)
	async def send_log_reports(self):
		try:
			msg = EmailMessage()
			msg['Subject'] = "Log report for AllSeeBot bot - {0}".format(datetime.now())
			msg['From'] = os.getenv('BOT_MAIL')
			msg['To'] = "alberto.cruz6@upr.edu"
			msg.set_content('')
			logs = ['searchbot.log', 'allSeeBot.log']
			
			# Attachments
			for log_file in logs:
				with open(log_file, 'r') as f1:
					file_data = f.read()
					file_name = f.name
				msg.add_attachment(file_data, maintype='text', subtype='plain', filename=file_name)
			with open(self.fileName 'r') as csvfile:
				msg.attach('lastTweets.csv', csvfile.getvalue(), 'text/csv')

			# send
			with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
				smtp.login(os.getenv('BOT_MAIL'), os.getenv('BOT_MAIL_PASS'))
				smtp.send_message(msg)
		except Exception as e:
			print(e)
			print("Error! Couldn't send log report...- {0}".format(datetime.now()))

