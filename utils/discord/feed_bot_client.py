# import discord
# from discord.ext import tasks
# import tweepy
# import csv

# from datetime import datetime
# from settings import tw_api
# from utils.external_tools.timer_tool import Timer

# # Discord Client class
# class FeedBot(discord.Client):
# 	async def on_ready(self):
# 		now = datetime.now()  
# 		print("Bot is initialized!")
# 		print('We have logged in as {0.user}'.format(self))
		
# 		# Twitter Authentication
# 		self.tw_handler = tw_api
# 		if self.tw_handler is None:
# 			print("Invalid tw bot account found! Fetching will not initiate")
# 		else:
# 			self.tw_handler.update_status("FeedBot ONLINE! - " + now.strftime("%d/%m/%Y %H:%M:%S"));
# 			print("Logged into All TW account at time " + now.strftime("%d/%m/%Y %H:%M:%S"))
# 			self.update_track_fetch.start()

# 		self.lst_commands = ["greet", "commands", "searchTW"]
# 		self.user_track_dictionary= {901864726015209472 : None, 2196628051: None}
# 		for channel in self.get_all_channels():
# 			if channel.name == "updatedtwitterfeed":
# 				self.user_track_channel = channel
# 				break


# 	async def on_message(self,message):
# 		if message.author == self.user:
# 			return
# 		msg = message.content

# 	# Loop to fetch tweets of users lists
# 	@tasks.loop(seconds=100.0)
# 	async def update_track_fetch(self):
# 		#############################################
# 		fileName = "last_tweets.csv"
# 		def findLastTweet(uid):
# 			with open(fileName) as csvFile:
# 				csvreader = csv.reader(csvFile)
# 				header = []
# 				header = next(csvreader)
# 				rows = []
# 				for row in csvreader:
# 					rows.append(row)
# 			print(header)
# 			print(rows)
# 			for row in rows:
# 				if str(row[0]) == str(uid):
# 					return row[1]
# 			return None
# 		#############################################
# 		#############################################
# 		def writeLastTweet(uid, tw_id):
# 			with open(fileName) as csvFile:
# 				csvreader = csv.reader(csvFile)
# 				header = []
# 				header = next(csvreader)
# 				rows = []
# 				for row in csvreader:
# 					rows.append(row)
			
# 			for index in range(len(rows)):
# 				if str(rows[index][0]) == str(uid):
# 					rows[index][1] = tw_id
# 					break
# 				if index == len(rows) - 1: # didn't find it in csv
# 					rows.append([uid, tw_id])

# 			with open(fileName, 'w') as ncsvFile:
# 				for head in header:
# 					ncsvFile.write(str(head)+', ')
# 				ncsvFile.write('\n')
# 				for row in rows:
# 					for x in row:
# 						ncsvFile.write(str(x)+', ')
# 					ncsvFile.write('\n')
# 		#############################################
# 		print("TRACKING USERS")
# 		if self.user_track_dictionary:
# 			for user in self.user_track_dictionary:
# 				lastWrittenTweet = findLastTweet(user)
# 				print(lastWrittenTweet)
# 				if self.user_track_dictionary[user] is None and lastWrittenTweet == "None":
# 					try:
# 						user_r = self.tw_handler.get_user(user_id=user)
# 						tweets = self.tw_handler.user_timeline(screen_name=user_r.screen_name,count = 1)
# 						self.user_tracktwitter_dictionary[user] = tweets[0].id
# 						writeLastTweet(user, self.user_track_dictionary[user])
# 						if self.user_track_channel:
# 							await self.user_track_channel.send("https://twitter.com/twitter/statuses/{0}".format(self.user_track_dictionary[user]))
# 					except:
# 						print("Couldn find user {0}!".format(user))
# 				else:
# 					try:
# 						user_r = self.tw_handler.get_user(user_id=user)
# 						tweets = self.tw_handler.user_timeline(screen_name=user_r.screen_name,count = 1)
# 						if self.user_track_dictionary[user] != tweets[0].id:
# 							writeLastTweet(user, self.user_track_dictionary[user])
# 							self.user_track_dictionary[user] = tweets[0].id
# 							if self.user_track_channel:
# 								await self.user_track_channel.send("https://twitter.com/twitter/statuses/{0}".format(self.user_track_dictionary[user]))
# 					except:
# 						print("Couldn find user {0}!".format(user))
